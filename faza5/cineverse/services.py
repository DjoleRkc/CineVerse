#Autor: Lana Jovanovic
import re
import requests
import translators as ts
from datetime import datetime, date, timedelta

from django.core.mail import send_mail
from django.db import transaction

import localSecrets
from cineverse.models import *

emailSubjects = {
    'PRIHVACEN NALOG': 'Uspešna registracija',
    'OBRISAN NALOG': 'Vaš nalog je obrisan'
}

emailBody = {
    'PRIHVACEN NALOG': 'Poštovani, \nUspešno ste se registrovali! Vidimo se na mestu zabave!\n\nSrdačan pozdrav, CineVerse',
    'OBRISAN NALOG': 'Poštovani, \nVaš nalog na portalu CineVerse je obrisan.\n\nSrdačan pozdrav, CineVerse',
}

def insertFilm(naziv, godina):
    """
            Inserts a film into the database based on its name and release year.

            Args:
                naziv (str): The name of the film.
                godina (str): The release year of the film.

            Returns:
                None
    """

    try:
        key = localSecrets.OMDB_API_KEY
        requestBody = f'https://www.omdbapi.com/?apikey={key}&t={naziv}&type=movie'
        if(godina != ''): requestBody += f"&y={godina}"

        movieInfo = requests.get(requestBody).json()
        movieInfoStr = f"This movie's name in Serbian is: {movieInfo['Title']}. Genres are {movieInfo['Genre']}. {movieInfo['Plot']}"
        translatedMovieInfo = ts.translate_text(movieInfoStr, translator="bing", from_language="en", to_language="sr-Latn")

        colonApperance = translatedMovieInfo.find(':')
        dotApperance = translatedMovieInfo.find('.')
        dotApperance2 = translatedMovieInfo.find('.', dotApperance + 1)
        naziv = translatedMovieInfo[colonApperance+2:dotApperance]
        zanrovi = translatedMovieInfo[dotApperance + 13:dotApperance2].split(', ')
        plot = translatedMovieInfo[dotApperance2 + 2:]

        prikazivanje = datetime.strptime(movieInfo['Released'], "%d %b %Y").strftime("%Y-%m-%d")

        requestBody += '&plot=full'
        longPlot = requests.get(requestBody).json()['Plot']
        radnja = ""
        for i in range(0, len(longPlot), 500):
            chunk = longPlot[i:i + 500]
            radnja += ts.translate_text(chunk, translator="bing", from_language="en", to_language="sr-Latn")

        film = Film(naziv=naziv, originalninaziv=movieInfo['Title'], trajanje=movieInfo['Runtime'][:-4],
                    pocetakprikazivanja=prikazivanje,
                    reziseri=movieInfo['Director'], glumci=movieInfo['Actors'], krataksadrzaj=plot,
                    ocenaimdb = float(movieInfo['imdbRating']) if movieInfo['imdbRating'] != 'N/A' else 0, radnja=radnja,
                    ocenakorisnika=0, slika=movieInfo['Poster'], sredjennaziv=srediImeFilma(naziv))
        film.save()

        for naziv in zanrovi:
            zanr, _ = Zanr.objects.get_or_create(naziv=naziv)
            ImaZanr(idfil=film, idzan=zanr).save()

        return 'Uspesno ste uneli film u bazu podataka!'
    except Exception:
        return 'Zadati film nije pronadjen. Pokusajte da specificirate i godinu.' if godina == '' else 'Zadati film nije pronadjen.'

def createProjekcija(sala, nazivFilma, nazivTermina, datum):
    """
        Creates a screening for a film in a specified venue, time slot, and date.

        Args:
            sala (int): The ID of the venue (sala).
            nazivFilma (str): The name of the film.
            nazivTermina (str): The name of the time slot (termin).
            datum (str): The date of the screening.

        Returns:
            str: A message indicating the result of the operation.
    """

    try:
        film = Film.objects.get(naziv=nazivFilma)
        termin = Termin.objects.get(termin=nazivTermina)
        sala = Sala.objects.get(idsal=sala)

        try:
            Projekcija.objects.get(idsal=sala, idter=termin, datum=datum)
            return 'Odabrana sala je zauzeta u zadatom terminu'
        except Exception:
            projekcija = Projekcija(idfil=film, idsal=sala, idter=termin, datum=datum)
            projekcija.save()
            return 'Uspešno ste uneli projekciju u bazu podataka!'

    except Exception:
        return 'Došlo je do greške pri unosu podataka u bazu'

def updateProjekcija(sala, nazivTermina, datum, idpro):
    """
        Updates a screening for a film in a specified venue, time slot, and date.

        Args:
            sala (int): The ID of the venue (sala).
            nazivFilma (str): The name of the film.
            nazivTermina (str): The name of the time slot (termin).
            datum (str): The date of the screening.

        Returns:
            str: A message indicating the result of the operation.
    """

    try:
        termin = Termin.objects.get(termin=nazivTermina)
        sala = Sala.objects.get(idsal=sala)

        try:
            p = Projekcija.objects.get(idsal=sala, idter=termin, datum=datum)
            if p.idpro != idpro: return 'Odabrana sala je zauzeta u zadatom terminu'
            else: return 'Uspešno ste izmenili termin projekcije!'
        except Exception:
            projekcija = Projekcija.objects.get(idpro=idpro)
            projekcija.idsal = sala
            projekcija.idter = termin
            projekcija.datum = datum
            projekcija.save()
            return 'Uspešno ste izmenili termin projekcije!'

    except Exception:
        return 'Došlo je do greške pri unosu podataka u bazu'

def fromZahtevToKorisnik(korisnickoime, email):
    """
        Converts a request (zahtev) user to a regular (korisnik) user.

        Args:
            korisnickoime (str): The username of the user.
            email (str): The email address of the user.

        Returns:
            None
    """
    nalog = Nalog.objects.get(username = korisnickoime, email = email)
    nalog.uloga = 'K'
    nalog.save()

def deleteZahtev(korisnickoime, email):
    """
        Deletes a request (zahtev) user from the database.

        Args:
            korisnickoime (str): The username of the user.
            email (str): The email address of the user.

        Returns:
            None
    """
    nalog = Nalog.objects.get(username=korisnickoime, email=email)
    nalog.delete()

def deleteKorisnik(korisnickoime, email):
    """
        Deletes a regular (korisnik) user from the database.

        Args:
            korisnickoime (str): The username of the user.
            email (str): The email address of the user.

        Returns:
            None
    """
    nalog = Nalog.objects.get(username=korisnickoime, email=email)
    nalog.delete()

def emailUser(email, cause):
    """
        Sends an email to a user based on the cause.

        Args:
            email (str): The email address of the user.
            cause (str): The cause for sending the email.

        Returns:
            None
    """
    subject = emailSubjects[cause]
    message = emailBody[cause]
    from_email = localSecrets.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)

def emailUsersAboutProjections(users, film, sala, termin, datum):
    """
        Sends an email to all user that reserved a projection.

        Args:
            email (str): The email address of the user.
            cause (str): The cause for sending the email.

        Returns:
            None
    """
    subject = f'Promenjen termin projekcije filma {film}'
    message = f'Nov termin projekcije filma je u {termin}h, {datum}. Sala u kojoj će se prikazivati film je Sala {sala}.\nVidimo se na mestu zabave!\n\nSrdačan pozdrav, CineVerse'
    from_email = localSecrets.EMAIL_HOST_USER
    recipient_list = set()
    for u in users:
        recipient_list.add(u.idkor.email)
    recipient_list = list(recipient_list)
    send_mail(subject, message, from_email, recipient_list)

def emailUsersAboutReservation(user, film, sala, termin, datum, sedista):
    """
        Sends an email to all user that reserved a projection.

        Args:
            email (str): The email address of the user.
            cause (str): The cause for sending the email.

        Returns:
            None
    """
    subject = f'Uspešna rezervacija filma {film}'
    message = f'Uspešno ste rezervisali mesta {sedista} u terminu {termin}, {datum} za film {film}. Sala u kojoj će se prikazivati film je Sala {sala}.\nVidimo se na mestu zabave!\n\nSrdačan pozdrav, CineVerse'
    from_email = localSecrets.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)

def srediImeFilma(ime):
    """
        Formats the name of a film.

        Args:
            ime (str): The name of the film.

        Returns:
            str: The formatted name of the film.
    """
    return re.sub(r'[^a-zA-Z0-9]', "", ime).lower()