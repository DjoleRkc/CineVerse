# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.auth.models import AbstractUser
from django.db import models


class Film(models.Model):
    """
    Stores information about a film.

    Attributes:
        idfil (AutoField): The primary key for the film.
        naziv (CharField): The name of the film.
        originalninaziv (CharField): The original name of the film.
        trajanje (IntegerField): The duration of the film.
        pocetakprikazivanja (DateField): The start date of the film's screening.
        reziseri (CharField): The directors of the film.
        glumci (CharField): The actors in the film.
        krataksadrzaj (CharField): A brief summary of the film.
        radnja (CharField): The plot of the film.
        ocenaimdb (FloatField): The IMDb rating of the film.
        ocenakorisnika (FloatField): The user rating of the film.
        slika (CharField): The URL of the film's image.
        sredjennaziv (CharField, optional): The adjusted name of the film.
    """
    idfil = models.AutoField(db_column='idFil', primary_key=True)  # Field name made lowercase.
    naziv = models.CharField(max_length=45)
    originalninaziv = models.CharField(db_column='originalniNaziv', max_length=45)  # Field name made lowercase.
    trajanje = models.IntegerField()
    pocetakprikazivanja = models.DateField(db_column='pocetakPrikazivanja')  # Field name made lowercase.
    reziseri = models.CharField(max_length=100)
    glumci = models.CharField(max_length=150)
    krataksadrzaj = models.CharField(db_column='kratakSadrzaj', max_length=500)  # Field name made lowercase.
    radnja = models.CharField(max_length=1500)
    ocenaimdb = models.FloatField(db_column='ocenaIMDB')  # Field name made lowercase.
    ocenakorisnika = models.FloatField(db_column='ocenaKorisnika')  # Field name made lowercase.
    slika = models.CharField(max_length=1000)
    sredjennaziv = models.CharField(db_column='sredjenNaziv',default='', max_length=45)  # Field name made lowercase.

    class Meta:
        db_table = 'film'


class ImaZanr(models.Model):
    """
    Associates films with genres.

    Attributes:
        id (AutoField): The primary key for the association.
        idfil (OneToOneField): The film associated with the genre.
        idzan (ForeignKey): The genre associated with the film.
    """
    id = models.AutoField(primary_key=True)
    idfil = models.OneToOneField(Film, models.CASCADE, db_column='idFil')  # Field name made lowercase. The composite primary key (idFil, idZan) found, that is not supported. The first column is selected.
    idzan = models.ForeignKey('Zanr', models.CASCADE, db_column='idZan')  # Field name made lowercase.

    class Meta:
        db_table = 'ima_zanr'
        unique_together = (('idfil', 'idzan'),)

class Nalog(AbstractUser):
    """
    Extends Django's AbstractUser model to store user accounts.

    Attributes:
        uloga (CharField): The role of the user.
    """
    uloga = models.CharField(max_length=1)

    class Meta:
        db_table = 'nalog'

class Ocenjuje(models.Model):
    """
    Stores user ratings for films.

    Attributes:
        id (AutoField): The primary key for the rating.
        idkor (OneToOneField): The user who rated the film.
        idfil (ForeignKey): The film being rated.
        ocena (IntegerField): The rating given by the user.
    """
    id = models.AutoField(primary_key=True)
    idkor = models.OneToOneField(Nalog, models.CASCADE, db_column='idKor')
    idfil = models.ForeignKey(Film, models.CASCADE, db_column='idFil')
    ocena = models.IntegerField()

    class Meta:
        db_table = 'ocenjuje'
        unique_together = (('idkor', 'idfil'),)

class Predlaze(models.Model):
    """
        Stores user film suggestions.

        Attributes:
            idkor (OneToOneField): The user who suggested the film.
            nazivfilma (CharField): The name of the suggested film.
    """
    id = models.AutoField(primary_key=True)
    idkor = models.OneToOneField(Nalog, models.CASCADE, db_column='idKor')  # Field name made lowercase. The composite primary key (idKor, nazivFilma) found, that is not supported. The first column is selected.
    nazivfilma = models.CharField(db_column='nazivFilma', max_length=200)  # Field name made lowercase.
    film = models.CharField(db_column='film', max_length=200)

    class Meta:
        db_table = 'predlaze'
        unique_together = (('idkor', 'nazivfilma'),)


class Projekcija(models.Model):
    """
    Stores information about film screenings.

    Attributes:
        idpro (AutoField): The primary key for the screening.
        idfil (ForeignKey): The film being screened.
        idsal (ForeignKey): The venue (sala) where the screening takes place.
        idter (ForeignKey): The time slot (termin) for the screening.
        datum (CharField): The date of the screening.
    """
    idpro = models.AutoField(db_column='idPro', primary_key=True)  # Field name made lowercase.
    idfil = models.ForeignKey(Film, models.CASCADE, db_column='idFil')  # Field name made lowercase.
    idsal = models.ForeignKey('Sala', models.CASCADE, db_column='idSal')  # Field name made lowercase.
    idter = models.ForeignKey('Termin', models.CASCADE, db_column='idTer')  # Field name made lowercase.
    datum = models.CharField(max_length=100)

    class Meta:
        db_table = 'projekcija'


class Rezervacija(models.Model):
    """
    Stores user reservations for film screenings.

    Attributes:
        idrez (AutoField): The primary key for the reservation.
        idkor (ForeignKey): The user making the reservation.
        idpro (ForeignKey): The screening being reserved.
        idsed (ForeignKey): The seat being reserved.
    """
    idrez = models.AutoField(db_column='idRez', primary_key=True)  # Field name made lowercase.
    idkor = models.ForeignKey(Nalog, models.CASCADE, db_column='idKor')  # Field name made lowercase.
    idpro = models.ForeignKey(Projekcija, models.CASCADE, db_column='idPro')  # Field name made lowercase.
    idsed = models.ForeignKey('Sediste', models.CASCADE, db_column='idSed')  # Field name made lowercase.

    class Meta:
        db_table = 'rezervacija'


class Sala(models.Model):
    """
    Stores information about screening venues.

    Attributes:
        idsal (AutoField): The primary key for the venue.
    """
    idsal = models.AutoField(db_column='idSal', primary_key=True)  # Field name made lowercase.

    class Meta:
        db_table = 'sala'


class Sediste(models.Model):
    """
    Stores information about seats in screening venues.

    Attributes:
        idsed (IntegerField): The primary key for the seat.
        idsal (ForeignKey): The venue where the seat is located.
        red (IntegerField): The row number of the seat.
        kolona (CharField): The column (seat number) of the seat.
    """
    idsed = models.IntegerField(db_column='idSed', primary_key=True)  # Field name made lowercase.
    idsal = models.ForeignKey(Sala, models.CASCADE, db_column='idSal')  # Field name made lowercase.
    red = models.IntegerField()
    kolona = models.CharField(max_length=1)

    class Meta:
        db_table = 'sediste'


class Termin(models.Model):
    """
    Stores information about time slots for film screenings.

    Attributes:
        idter (AutoField): The primary key for the time slot.
        termin (CharField): The time slot.
    """
    idter = models.AutoField(db_column='idTer', primary_key=True)  # Field name made lowercase.
    termin = models.CharField(max_length=5)

    class Meta:
        db_table = 'termin'


class Watchlist(models.Model):
    """
    Stores films in user watchlists.

    Attributes:
        id (AutoField): The primary key for the watchlist item.
        idkor (OneToOneField): The user owning the watchlist.
        idfil (ForeignKey): The film in the watchlist.
    """
    id = models.AutoField(primary_key=True)
    idkor = models.OneToOneField(Nalog, models.CASCADE, db_column='idKor')  # Field name made lowercase. The composite primary key (idKor, idFil) found, that is not supported. The first column is selected.
    idfil = models.ForeignKey(Film, models.CASCADE, db_column='idFil')  # Field name made lowercase.

    class Meta:
        db_table = 'watchlist'
        unique_together = (('idkor', 'idfil'),)


class Zanr(models.Model):
    """
    Stores information about film genres.

    Attributes:
        idzan (AutoField): The primary key for the genre.
        naziv (CharField): The name of the genre.
    """
    idzan = models.AutoField(db_column='idZan', primary_key=True)  # Field name made lowercase.
    naziv = models.CharField(max_length=45)

    class Meta:
        db_table = 'zanr'
