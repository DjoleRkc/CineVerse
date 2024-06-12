'''
Autori: Lana Jovanovic 0380-21
        Đorđe Pajić    0642-21
        Nikola Ostojić 0622-21
        Jovan Babović  0345-21
'''
import os
import json
from django.contrib.auth.hashers import check_password
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import login as loginDjango, logout as logoutDjango
from psi_projekat import settings
from cineverse.services import *
from .forms import *


sale = {
    'A' : 1,
    'B' : 2,
    'C' : 3,
    'D' : 4,
    'E' : 5
}

sale_reverted = {
    1: 'A',
    2: 'B',
    3: 'C',
    4: 'D',
    5: 'E'
}

@csrf_exempt
def potvrdaRezervacije(request):
    """
        Confirms a seat reservation for a user.

        Args:
            request: The HTTP request object.

        Returns:
            JsonResponse: A JSON response indicating success or error.
    """

    if not request.user.is_authenticated:
        return JsonResponse({'greska': 'Greška!'}, status=401)

    user_id = request.user.id
    idpro = request.GET.get('idpro')
    seats = request.GET.get('seats', '')
    seat_ids = seats.split(", ")
    idsala = request.GET.get('idsala')

    redKolona = []
    
    id_sedista = []
    for seat in seat_ids:
        redKolona.append( (sale[seat[0]], int(seat[1])) )
    
    for pair in redKolona:
        sediste = Sediste.objects.get(red=pair[0], kolona=pair[1], idsal=idsala)
        id_sedista.append(sediste.idsed)

    nalog_instance = Nalog.objects.get(pk=user_id)
    projekcija_instance = Projekcija.objects.get(idpro=idpro)
    
    for id_s in id_sedista:

        sediste_instance = Sediste.objects.get(idsed=id_s)
        nova_rezervacija = Rezervacija(idkor=nalog_instance, idpro=projekcija_instance, idsed=sediste_instance)
        nova_rezervacija.save()

    emailUsersAboutReservation(request.user, projekcija_instance.idfil.naziv, projekcija_instance.idsal.idsal, projekcija_instance.idter.termin, projekcija_instance.datum, seats)

    return JsonResponse({'uspeh' : 1})

    
def pregledFilmaNO(request):
    """
        Displays the details of a specific movie.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponse: The rendered template with the film details.
    """

    template = 'pregledFilma.html'
    nazivFilma = request.GET.get('parametar')
    film = Film.objects.get(naziv=nazivFilma)

    return render(request, template, {'nazivFilma': nazivFilma, 'film': film})


def ucitajOdredjeniFilm(request):
    """
        Loads the details of a specific movie.

        Args:
            request: The HTTP request object.

        Returns:
            JsonResponse: A JSON response with movie details.
    """

    parametar = request.GET.get('parametar')    
    trazeniFilm = Film.objects.get(naziv=parametar)

    ima_zanrovi = ImaZanr.objects.all()

    zanrovi = []
        
    for ima_zanr in ima_zanrovi:
        if (trazeniFilm.idfil != ima_zanr.idfil_id):
            continue
        
        genre_id = ima_zanr.idzan_id
        genre_name = Zanr.objects.get(idzan=genre_id).naziv
        
        zanrovi.append(genre_name)

    return JsonResponse({
        'naziv' : trazeniFilm.naziv,
        'slika' : trazeniFilm.slika,
        'krataksadrzaj' : trazeniFilm.krataksadrzaj,
        'ocenakorisnika' : trazeniFilm.ocenakorisnika,
        'ocenaimdb' : trazeniFilm.ocenaimdb,
        'trajanje' : trazeniFilm.trajanje,
        'zanrovi' : zanrovi
    },
    safe=False)


def ucitajFilmove(request):
    """
        Loads a list of all movie names.

        Args:
            request: The HTTP request object.

        Returns:
            JsonResponse: A JSON response with a list of film names.
    """

    filmovi = list(Film.objects.values_list('naziv', flat=True))
    return JsonResponse({'filmovi': filmovi})

def landingPage(request):
    """
       Renders the landing page.

       Args:
           request: The HTTP request object.

       Returns:
           HttpResponse: The rendered landing page template.
   """

    template = 'landingPage.html'
    return render(request, template)

def sveProjekcije(request, template = 'projekcije.html', page = ''):
    """
        Displays all projections for a given date.

        Args:
            request: The HTTP request object.
            template (str): The template to render.
            page (str): The current page.

        Returns:
            HttpResponse: The rendered template with projections.
    """


    if (not request.GET):
        todaysDate = datetime.now()
        todaysDate = todaysDate.strftime('%d.%m.%Y')
    else:
        todaysDate = request.GET.get('datum')

    idFilmova = Projekcija.objects.filter(datum=todaysDate).values_list('idfil', flat=True).distinct()

    filmoviSet = set()

    filmoviSet.update(idFilmova)

    filmovi = Film.objects.filter(idfil__in=filmoviSet)
    ima_zanrovi = ImaZanr.objects.all()

    film_genre_dict = {}

    #disablovanje filmova koji su vec u watchlisti
    user_id = request.user.id
    movies = []
    if request.user.is_authenticated:
        nalogObjekat = Nalog.objects.get(pk=user_id)
        movies = Watchlist.objects.filter(idkor=nalogObjekat).values_list('idfil_id', flat=True)

    for ima_zanr in ima_zanrovi:

        if (ima_zanr.idfil_id not in filmoviSet):
            continue

        film_id = ima_zanr.idfil_id
        genre_id = ima_zanr.idzan_id
        genre_name = Zanr.objects.get(idzan=genre_id).naziv

        if film_id in film_genre_dict:
            film_genre_dict[film_id].append(genre_name)
        else:
            film_genre_dict[film_id] = [genre_name]

    mList = []
    for m in movies:
        mList.append(m)

    return render(request, template, {'filmovi': filmovi, 'film_genre_dict': film_genre_dict, 'datum' : todaysDate, 'page': page, 'watchlist': mList})

def pregledFilma(request, nazivFilma):
    """
        Displays the details of a specific movie by name.

        Args:
            request: The HTTP request object.
            nazivFilma (str): The name of the movie.

        Returns:
            HttpResponse: The rendered template with the movie details.
    """

    template = 'pregledFilma.html'
    nazivFilma = nazivFilma.replace('_', ' ')
    film = Film.objects.get(naziv=nazivFilma)

    return render(request, template, {'nazivFilma': nazivFilma, 'film': film})


def dohvatiProjekcije(request):
    """
        Fetches projections for a specific movie on a specific date.

        Args:
            request: The HTTP request object.

        Returns:
            JsonResponse: A JSON response with projection details.
    """

    idfil = request.GET.get('idfilma')

    datum = request.GET.get('datum')
    datum += "." + str(timezone.now().year)
    film = Film.objects.get(idfil=idfil)
    projekcije = Projekcija.objects.filter(idfil=film,datum=datum)
    data = [{'vreme':projekcija.idter.termin, 'sala':projekcija.idsal.idsal, 'idpro' : projekcija.idpro} for projekcija in projekcije]

    return JsonResponse({"data": data})

@csrf_exempt
@login_required
def dodajPredlog(request):
    """
       Adds a movie suggestion from a user.

       Args:
           request: The HTTP request object.

       Returns:
           JsonResponse: A JSON response indicating success or error.
   """

    if request.method == 'GET':
        korisnik = request.user
        imeFilma = request.GET.get('imeFilma')
        imeFilmaSredjeno = srediImeFilma(imeFilma)

        if Predlaze.objects.filter(idkor=korisnik, nazivfilma=imeFilmaSredjeno).exists():
            return JsonResponse({"error": "Vec predlozio"}, status=400)

        danas = date.today()
        datumi = [danas, danas + timedelta(days=1), danas + timedelta(days=2)]
        datumi = [d.strftime("%d.%m.%Y") for d in datumi]

        if Projekcija.objects.filter(idfil__sredjennaziv=imeFilmaSredjeno, datum__in=datumi).exists():
            return JsonResponse({"error": "Vec u ponudi"}, status=400)


        Predlaze.objects.create(idkor=korisnik, nazivfilma=imeFilmaSredjeno, film=imeFilma)
        return JsonResponse({"success": True})


@login_required
def rezervisiKartu(request):
    """
        Renders the ticket reservation page with seat details.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponse: The rendered ticket reservation template.
    """

    template = 'rezervisiKartu.html'

    idfilma = request.GET.get('film')

    film = Film.objects.get(idfil=idfilma)
    vreme = request.GET.get('vreme')
    sala = request.GET.get('sala')
    idpro = request.GET.get('idpro')

    rezervisana_sedista = []
    entries = Rezervacija.objects.filter(idpro=idpro)
    for entry in entries:
        rezervisana_sedista.append(entry.idsed) #vrati ceo objekat, mogu lako da uzmem row i column

    redKolona = []
    for sediste in rezervisana_sedista:
        redKolona.append(  sale_reverted[sediste.red] + str(sediste.kolona) )

    zauzetaSedisteRet = ""
    for x in redKolona:
        zauzetaSedisteRet += x[0]
        zauzetaSedisteRet += x[1]

    return render(request, template, {
        'filmIme' : film.naziv,
        'slikaFilma' : film.slika,
        'vremeFilma' : vreme,
        'sala' : sala,
        'idpro' : idpro,
        'zauzetaSedista' : zauzetaSedisteRet
    })

@login_required
def mojProfil(request):
    """
        Renders the user's profile page with their watchlist and rated movies.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponse: The rendered user profile template with watchlist and rated movies.
    """
    template = 'userProfile.html'
    korisnik = request.user
    watchlist = Watchlist.objects.filter(idkor=korisnik).values_list('idfil', flat=True)
    ocenjeniFilmovi = Ocenjuje.objects.filter(idkor=korisnik)
    watchlistFilmovi = Film.objects.filter(pk__in=watchlist)

    return render(request, template, {'watchlist': watchlistFilmovi, 'ocenjeni':ocenjeniFilmovi})


def sviTermini(request):
    """
        Displays all screening times for a specific movie.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponse: The rendered template with all screening times for the movie.
    """
    template = 'projekcije.html'
    nazivFilma = request.GET.get('nazivFilma')
    idFilm = Film.objects.get(naziv=nazivFilma)
    sviTermini = Projekcija.objects.get(idfil=idFilm).idter
    return render(request, template, {'sviTermini': sviTermini})

@csrf_exempt
@login_required
def oceniFilm(request):
    """
        Allows a user to rate a movie.

        Args:
            request: The HTTP request object.

        Returns:
            JsonResponse: A JSON response with the new average rating of the movie.
    """

    korisnik = request.user
    nazivFilma = request.POST.get('nazivFilma')
    ocena = request.POST.get('ocena')
    film = get_object_or_404(Film, naziv=nazivFilma)

    try:

        ocenaVecPostoji = Ocenjuje.objects.get(idkor=korisnik, idfil=film)
        ocenaVecPostoji.ocena = ocena
        ocenaVecPostoji.save()



    except:
        ocenjuje = Ocenjuje.objects.create(idkor=korisnik, idfil=film, ocena=ocena)

    avg_ocena = Ocenjuje.objects.filter(idfil=film).aggregate(Avg('ocena'))['ocena__avg']
    film.ocenakorisnika = avg_ocena
    film.save()

    return JsonResponse({'novaOcena': round(avg_ocena, 1)})

@csrf_exempt
@login_required
def fetchWatchlist(request):
    """
       Fetches the user's watchlist.

       Args:
           request: The HTTP request object.

       Returns:
           JsonResponse: A JSON response with the user's watchlist data.
   """

    if request.method == 'GET':
        korisnik = request.user
        watchlist = Watchlist.objects.filter(idkor=korisnik).select_related('idfil')
        watchlist_data = [{
            'idfil': item.idfil.idfil,
            'naziv': item.idfil.naziv,
            'slika': item.idfil.slika,
        } for item in watchlist]
        return JsonResponse({'watchlist': watchlist_data})
    return JsonResponse({'error': 'Metod mora biti GET'})

@login_required
def fetchGrades(request):
    """
        Fetches the movies rated by the user.

        Args:
            request: The HTTP request object.

        Returns:
            JsonResponse: A JSON response with the user's rated movies.
    """
    if request.method == 'GET':
        korisnik = request.user
        ocene = Ocenjuje.objects.filter(idkor=korisnik).select_related('idfil')
        ocene_data = [{
            'idfil': item.idfil.idfil,
            'naziv': item.idfil.naziv,
            'slika': item.idfil.slika,
            'ocena': item.ocena
        } for item in ocene]
        return JsonResponse({'gradedItems': ocene_data})
    return JsonResponse({'error': 'Metod mora biti GET'})




def sviFilmovi(request):
    """
      Displays a list of all movies with their genres.

      Args:
          request: The HTTP request object.

      Returns:
          HttpResponse: The rendered template with a list of all movies and their genres.
    """
    template = 'listaFilmova.html'

    filmovi = Film.objects.all().order_by('-ocenaimdb')

    ima_zanrovi = ImaZanr.objects.all()

    film_genre_dict = {}

    user_id = request.user.id
    movies = []
    if request.user.is_authenticated:
        nalogObjekat = Nalog.objects.get(pk=user_id)
        movies = Watchlist.objects.filter(idkor=nalogObjekat).values_list('idfil_id', flat=True)

    for ima_zanr in ima_zanrovi:
        film_id = ima_zanr.idfil_id
        genre_id = ima_zanr.idzan_id
        genre_name = Zanr.objects.get(idzan=genre_id).naziv

        if film_id in film_genre_dict:
            film_genre_dict[film_id].append(genre_name)
        else:
            film_genre_dict[film_id] = [genre_name]

    mList = []
    for m in movies:
        mList.append(m)

    return render(request, template, {'filmovi': filmovi, 'film_genre_dict': film_genre_dict, 'watchlist': mList})


def dohvatiSlike(request):
    """
        Fetches the images for the carousel.

        Args:
            request: The HTTP request object.

        Returns:
            JsonResponse: A JSON response with the list of image filenames.
    """
    dir = os.path.join(settings.BASE_DIR, 'cineverse', 'static', 'images', 'carousel')
    slike = [file for file in os.listdir(dir) if file.lower().endswith(('.png', '.jpg', '.jpeg'))]
    return JsonResponse(slike, safe=False)


@csrf_exempt
@login_required
def ukloniIzWatchliste(request):
    """
        Removes a film from the user's watchlist.

        Args:
            request: The HTTP request object.

        Returns:
            JsonResponse: A JSON response indicating success or error.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        korisnik = request.user
        idfil = data['idfil']
        filmObj = Film.objects.get(idfil=idfil)

        film = Watchlist.objects.filter(idkor=korisnik, idfil=filmObj)
        if film.exists():
            film.delete()
            return JsonResponse({'ok': True})
        else:
            return JsonResponse({'ok': False, 'error': 'Film nije u watchlisti'})

    return JsonResponse({'ok': False, 'error': 'Request method mora biti POST'}, status=400)


def adminIndex(request):
    """
        Renders the admin index page.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponse: The rendered admin index page template.
    """
    page = 'adminTemplates'
    template = 'adminTemplates/index.html'
    return render(request, template, {'page': page})

def dodajFilm(request):
    """
        Renders the page for adding a new movie and handles the form submission.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponse: The rendered template for adding a movie, with a success message if the form is submitted.
    """
    page = 'dodajFilm'
    template = 'adminTemplates/dodajFilm.html'

    if request.method == 'POST':
        naziv = request.POST['naziv']
        godina = request.POST['godina']
        modalMessage = insertFilm(naziv, godina)
        return render(request, template, {'page': page, 'modal': 'show', 'modalMessage': modalMessage, 'value': ''})

    return render(request, template,{'page': page, 'modal': 'hide', 'value': ''})

def dodajProjekciju(request):
    """
        Renders the page for adding a new projection and handles the form submission.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponse: The rendered template for adding a projection, with a success or error message.
    """

    template = 'adminTemplates/dodajProjekciju.html'

    modal = 'hide'
    modalMessage = ''
    page = "dodajProjekciju"
    termini = Termin.objects.all()
    filmovi = Film.objects.all()
    sale = Sala.objects.all()

    if request.method == 'POST':
        try:
            modal = 'show'
            datum = datetime.strptime(request.POST['datum'], "%Y-%m-%d").strftime("%d.%m.%Y")
            termin = request.POST['termin']
            sala = request.POST['sala']
            film = request.POST['film']

            modalMessage = createProjekcija(sala, film, termin, datum)

        except MultiValueDictKeyError:
            modalMessage = 'Morate popuniti sva polja'

    return render(request, template,
                  {'page': page, 'filmovi': filmovi, 'sale': sale, 'termini': termini,
                   'modal': modal, 'modalMessage': modalMessage})

def promeniProjekciju(request):
    """
        Renders the page for deleting a projection and handles the form submission.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponse: The rendered template for adding a projection, with a success or error message.
    """

    template = 'adminTemplates/promeniProjekciju.html'

    modal = 'hide'
    modalMessage = ''
    page = "dodajProjekciju"
    nazivFilma = ''
    termini = Termin.objects.all()
    sale = Sala.objects.all()

    if request.method == 'GET':
        idfilma = request.GET.get('film')
        film = Film.objects.get(idfil=idfilma)
        nazivFilma = film.naziv
        idpro = request.GET.get('idpro')
        projekcija = Projekcija.objects.get(idpro=idpro)

    else:
        modal = 'show'
        datum = datetime.strptime(request.POST['datum'], "%Y-%m-%d").strftime("%d.%m.%Y")
        termin = request.POST['termin']
        sala = request.POST['sala']
        idpro = request.POST['idpro']
        projekcija = Projekcija.objects.get(idpro=idpro)
        rezervacije = Rezervacija.objects.filter(idpro=projekcija)

        modalMessage = updateProjekcija(sala, termin, datum, idpro)
        if modalMessage == 'Uspešno ste izmenili termin projekcije!':
            emailUsersAboutProjections(rezervacije, projekcija.idfil.naziv, sala, termin, datum)

    return render(request, template,
                  {'page': page, 'nazivfilma': nazivFilma, 'sale': sale, 'termini': termini,
                   'idpro': idpro, 'modal': modal, 'modalMessage': modalMessage})

def korisnickiNalozi(request):
    """
       Renders the user accounts management page and handles account deletions.

       Args:
           request: The HTTP request object.

       Returns:
           HttpResponse: The rendered template for managing user accounts.
    """

    template = 'adminTemplates/korisnickiNalozi.html'

    if request.method == 'POST':
        korisnickoime = request.POST.get('korisnickoime')
        email = request.POST.get('email')
        deleteKorisnik(korisnickoime, email)
        emailUser(email, 'OBRISAN NALOG')

    page = "korisnickiNalozi"
    users = Nalog.objects.filter(uloga='K')

    return render(request, template, {'page': page, 'users': users })

def korisnickiZahtevi(request):
    """
        Renders the user requests management page and handles request approvals and rejections.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponse: The rendered template for managing user requests.
    """

    template = 'adminTemplates/korisnickiZahtevi.html'

    if request.method == 'POST':
        action = request.POST.get('action')
        korisnickoime = request.POST.get('korisnickoime')
        email = request.POST.get('email')

        if action == 'prihvati':
            fromZahtevToKorisnik(korisnickoime, email)
            emailUser(email, 'PRIHVACEN NALOG')

        else:
            deleteZahtev(korisnickoime, email)

    page = "korisnickiZahtevi"
    users = Nalog.objects.filter(uloga='Z')

    return render(request, template, {'page': page, 'users': users})

def korisnickiPredlozi(request):
    """
        Renders the user suggestions page.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponse: The rendered user suggestions page template.
    """
    page = "korisnickiPredlozi"
    template = 'adminTemplates/korisnickiPredlozi.html'

    if request.method == 'POST':
        film = request.POST['nazivFilma']
        nazivFilma = srediImeFilma(film)
        Predlaze.objects.filter(nazivfilma=nazivFilma).delete()
        if request.POST['akcija'] == 'prihvati':
            page = 'dodajFilm'
            template = 'adminTemplates/dodajFilm.html'
            return render(request, template, {'page': page, 'modal': 'hide', 'value': film})

    predlaze = Predlaze.objects.all()

    return render(request, template, {'page': page, 'predlaze': predlaze})

def prikazProjekcija(request):
    """
        Renders the projection display page.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponse: The rendered projection display page template.
    """
    page = "prikazProjekcija"
    template = 'adminTemplates/prikazProjekcija.html'

    return render(request, template, {'page': page})

def najboljeOcenjeni(request):
    """
        Displays a list of the highest-rated movies.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponse: The rendered template with the highest-rated movies and their genres.
    """
    template = "najboljeOcenjeni.html"
    filmovi = Film.objects.all().order_by('-ocenaimdb')
    
    ima_zanrovi = ImaZanr.objects.all()    

    film_genre_dict = {}
    
    #disablovanje filmova koji su vec u watchlisti
    user_id = request.user.id
    movies = []
    if request.user.is_authenticated:
        nalogObjekat = Nalog.objects.get(pk=user_id)
        movies = Watchlist.objects.filter(idkor=nalogObjekat).values_list('idfil_id', flat=True)


    for ima_zanr in ima_zanrovi:
        film_id = ima_zanr.idfil_id
        genre_id = ima_zanr.idzan_id
        genre_name = Zanr.objects.get(idzan=genre_id).naziv
        
        if film_id in film_genre_dict:
            film_genre_dict[film_id].append(genre_name)
        else:
            film_genre_dict[film_id] = [genre_name]
    
    mList = []
    for m in movies:
        mList.append(m)
    
    return render(request, template, {'filmovi': filmovi, 'film_genre_dict': film_genre_dict, 'watchlist': mList})

def login(request, *args, **kwargs):
    """
        Handles user login.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponse: The rendered login form template or a redirect if login is successful.
    """
    
    user = request.user
    if user.is_authenticated:
        return HttpResponse("Već ste ulogovani kao " + user.email)
    context = {'form_errors': {}, 'login_form': LoginForm()}
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.uloga == 'Z':
                    form.errors.clear()
                    form.add_error(None, 'Nalog mora biti odobren od strane admina.')
                    context['form_errors'] = form.errors
                    context['login_form'] = form
                    return render(request, 'loginForm.html', context)
                loginDjango(request, user)
                destination = kwargs.get("next")
                if destination:
                    return redirect(destination)
                try:
                    Nalog.objects.get(username=username, is_superuser=1)
                    return redirect('adminIndex')
                
                except Exception:
                    return redirect('landingPage')
            else:
                form.errors.clear()
                form.add_error(None, 'Pogrešno korisničko ime ili šifra.')
                context['form_errors'] = form.errors
                context['login_form'] = form
        else:
            form.errors.clear()
            form.add_error(None, 'Unesite validne podatke.')
            context['form_errors'] = form.errors
            context['login_form'] = form
    else:
        context['login_form'] = LoginForm()

    return render(request, 'loginForm.html', context)

def register(request):
    """
        Handles user registration.

        This view renders the registration form and processes the form submission.
        If the form is valid, it saves the new user, assigns the role 'Z', and redirects to the landing page.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponse: The rendered registration form template.
            HttpResponseRedirect: Redirects to the landing page if registration is successful.
    """

    form = RegistrationForm()

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            user = Nalog.objects.get(username=username)
            user.uloga = 'Z'
            user.save()
            return redirect('landingPage')
    
    cont = {"form": form}
    return render(request, 'registerForm.html', context=cont)


@csrf_exempt
def logout(request):
    """
        Logs out the user and redirects to the landing page.

        This view logs out the currently logged-in user and then redirects to the landing page.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponseRedirect: Redirects to the landing page after logging out.
    """
    logoutDjango(request)
    return redirect('landingPage')






@csrf_exempt
def dodajUWatchList(request):
    """
        Adds a film to the user's watchlist.

        Parameters:
        request (HttpRequest): The request object containing user information and POST data.

        Returns:
        JsonResponse: A JSON response indicating success or error.
            {'ret': 'good'} on success,
            {'ret': 'error', 'message': 'Film does not exist'} if the film is not found,
            {'ret': 'error', 'message': 'User does not exist'} if the user is not found,
            {'ret': 'error', 'message': str(e)} for any other exceptions.
    """

    user_id = request.user.id
    idFilma = request.POST.get('idFilma')
    
    try:
        filmObjekat = Film.objects.get(idfil=idFilma)
        nalogObjekat = Nalog.objects.get(pk=user_id)
        Watchlist.objects.create(idkor=nalogObjekat, idfil=filmObjekat)
        return JsonResponse({'ret': 'good'})
    except Film.DoesNotExist:
        return JsonResponse({'ret': 'error', 'message': 'Film does not exist'})
    except Nalog.DoesNotExist:
        return JsonResponse({'ret': 'error', 'message': 'User does not exist'})
    except Exception as e:
        return JsonResponse({'ret': 'error', 'message': str(e)})



@csrf_exempt
def forgottenPassword(request):
    """
        Renders the forgotten password page.

        Parameters:
        request (HttpRequest): The request object.

        Returns:
        HttpResponse: The rendered forgotten password page.
    """

    context = {}
    return render(request, 'forgottenPassword.html', context)


@csrf_exempt
def anonymous_required(view_func):
    """
        Decorator to restrict access to views for authenticated users.

        Parameters:
        view_func (function): The view function to wrap.

        Returns:
        function: The wrapped view function.
    """
    def _wrapped_view(request):
        if request.user.is_authenticated:
            return HttpResponse("You are already authenticated as " + request.user.email)
        return view_func(request)
    return _wrapped_view



@csrf_exempt
@anonymous_required
def zaboravljenaLozinka(request):
    """
       Handles forgotten password requests by sending a password reset email.

       Parameters:
       request (HttpRequest): The request object containing POST data.

       Returns:
       HttpResponse: The forgotten password page with an error message if email is invalid,
                     or redirects to code verification page on success.
    """

    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            user = Nalog.objects.filter(email=email).first()
            if user:
                token_generator = default_token_generator
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = token_generator.make_token(user)
                code = f"{uid}-{token}"
                
                send_mail(
                    'Password Reset Kod',
                    f'Vaš kod za resetovanje šifre je: {code}\n\nPozdrav, CineVerse.',
                    localSecrets.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )

                request.session['password_reset_email'] = email
                request.session['password_reset_code'] = code
                
                return redirect('codeVerify')
            else:
                return render(request, 'forgottenPassword.html', {'error': 'Nepostojeći email', 'step': 1})
        else:
            return render(request, 'forgottenPassword.html', {'error': 'Email je obavezan', 'step': 1})
    else:
        return render(request, 'forgottenPassword.html', {'step': 1})


@csrf_exempt
@anonymous_required
def codeVerify(request):
    """
        Verifies the password reset code provided by the user.

        Parameters:
        request (HttpRequest): The request object containing POST data.

        Returns:
        HttpResponse: The code verification page with an error message if the code is invalid,
                      or redirects to password reset page on success.
    """

    if request.method == 'POST':
        code = request.POST.get('code')

        if code:
            expected_code = request.session.get('password_reset_code')
            if expected_code == code:
                return redirect('passwordReset')
            else:
                return render(request, 'codeVerification.html', {'error': 'Pogrešan kod', 'step': 2})
        else:
            return render(request, 'codeVerification.html', {'error': 'Kod je obavezan', 'step': 2})
    else:
        return render(request, 'codeVerification.html', {'step': 2})
    

@csrf_exempt
@anonymous_required
def passwordReset(request):
    """
        Resets the user's password.

        Parameters:
        request (HttpRequest): The request object containing POST data.

        Returns:
        HttpResponse: The password reset page with an error message if validation fails,
                      or a success message on successful password reset.
    """

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password and confirm_password:
            email = request.session.get('password_reset_email')
            user = Nalog.objects.filter(email=email).first()

            if user:
                currPassword = user.password


                if new_password == confirm_password:
                    if check_password(new_password, currPassword):
                        return render(request, 'passwordReset.html',{'error': 'Šifra koju ste uneli je ista kao neka koju ste pre koristili!','step': 3})

                    user.set_password(new_password)
                    user.save()
                    del request.session['password_reset_email']
                    del request.session['password_reset_code']
                    return render(request, 'passwordReset.html', {'success': True, 'step': 3})
                else:
                    return render(request, 'passwordReset.html', {'error': 'Šifre nisu iste', 'step': 3})
            else:
                return render(request, 'passwordReset.html', {'error': 'Korisnik nije pronađen', 'step': 3})
        else:
            return render(request, 'passwordReset.html', {'error': 'Sva polja su obavezna', 'step': 3})
    else:
        return render(request, 'passwordReset.html', {'step': 3})