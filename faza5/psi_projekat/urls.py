'''
Autori: Lana Jovanovic 0380-21
        Đorđe Pajić 0642-21
'''

"""
URL configuration for psi_projekat project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path, include
from cineverse.views import *

urlpatterns = [
    path('', landingPage, name='landingPage'),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),

    # portal za Admine
    path('adminPortal/', adminIndex, name='adminIndex'),
    path('adminPortal/dodajFilm', dodajFilm, name='dodajFilm'),
    path('adminPortal/dodajProjekciju', dodajProjekciju, name='dodajProjekciju'),
    path('adminPortal/promeniProjekciju', promeniProjekciju, name='promeniProjekciju'),
    path('adminPortal/korisnickiNalozi', korisnickiNalozi, name='korisnickiNalozi'),
    path('adminPortal/korisnickiZahtevi', korisnickiZahtevi, name='korisnickiZahtevi'),
    path('adminPortal/korisnickiPredlozi', korisnickiPredlozi, name='korisnickiPredlozi'),
    path('adminPortal/prikazProjekcija', sveProjekcije, {'template': 'adminTemplates/prikazProjekcija.html', 'page': 'prikazProjekcija'}, name='prikazProjekcija'),
    path('adminPortal/projekcije', sveProjekcije, {'template': 'adminTemplates/prikazProjekcija.html', 'page': 'prikazProjekcija'}, name='sveProjekcije'),
    path('adminPortal/dohvatiProjekcije', dohvatiProjekcije),

    # Korisnicki metodi
    path('projekcije', sveProjekcije, name='sveProjekcije'),
    path('pregledFilma/<nazivFilma>', pregledFilma, name='pregledFilma'),
    path('mojProfil', mojProfil, name='mojProfil'),
    path('sviFilmovi', sviFilmovi, name="sviFilmovi"),
    path('najboljeOcenjeni', najboljeOcenjeni, name='najboljeOcenjeni'),
    path('ucitajFilmove', ucitajFilmove, name='ucitajFilmove'),
    path('ucitajOdredjeniFilm', ucitajOdredjeniFilm, name='ucitajOdredjeniFilm'),
    path('pregledFilmaNO', pregledFilmaNO, name='pregledFilmaNO'),
    path('rezervisiKartu', rezervisiKartu, name='rezervisiKartu'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
    path("ukloniIzWatchliste", ukloniIzWatchliste, name='ukloniIzWatchliste'),
    path("dohvatiProjekcije", dohvatiProjekcije, name='dohvatiProjekcije'),
    path("dodajPredlog", dodajPredlog, name='dodajPredlog'),
    path("oceniFilm", oceniFilm, name='oceniFilm'),
    path("dohvatiSlike", dohvatiSlike, name='dohvatiSlike'),
    path("potvrdaRezervacije", potvrdaRezervacije, name="potvrdaRezervacije"),
    path("fetchWatchlist", fetchWatchlist, name='fetchWatchlist'),
    path("fetchGrades", fetchGrades, name='fetchGrades'),
    path('dodajUWatchList', dodajUWatchList, name='dodajUWatchList'),
    path('forgottenPassword', forgottenPassword, name='forgottenPassword'),
    path('zaboravljenaLozinka', zaboravljenaLozinka, name='zaboravljenaLozinka'),
    path('codeVerification', codeVerify, name='codeVerify'),
    path('passwordReset', passwordReset, name='passwordReset'),
]
