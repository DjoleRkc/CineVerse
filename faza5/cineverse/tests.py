import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase, RequestFactory, Client
from unittest.mock import patch, MagicMock
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.urls import reverse

from .views import *


class adminTests(StaticLiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        Projekcija.objects.all().delete()
        Film.objects.all().delete()
        Termin.objects.all().delete()
        Sala.objects.all().delete()
        self.driver.close()

    def loginAsAdmin(self):
        driver = self.driver

        driver.get(f'{self.live_server_url}/login')

        Nalog.objects.create(
            password='pbkdf2_sha256$720000$1KJQrllZTOKCv0gy5PrDYS$rvFzw/jWVcZlGCAroCwsLrd4WFep+1l8LPgJEGJn1QE=',
            is_superuser=1, username='admin', first_name='', last_name='',
            email='superuser@gmail.com', is_staff=1, is_active=1, uloga='A')

        username = driver.find_element(By.NAME, 'username')
        password = driver.find_element(By.NAME, 'password')
        login_button = driver.find_element(By.ID, 'btn-login')

        username.send_keys('admin')
        password.send_keys('superuser123')
        login_button.click()

        WebDriverWait(driver, 10).until(
            EC.url_contains('/adminPortal/')
        )

    @patch('cineverse.views.insertFilm')
    def test_dodajFilmUspesno(self, mock_insertFilm):
        driver = self.driver
        mock_insertFilm.return_value = 'Uspesno ste uneli film u bazu podataka!'
        self.loginAsAdmin()

        driver.get(f'{self.live_server_url}/adminPortal/dodajFilm')

        naziv = driver.find_element(By.NAME, 'naziv')
        godina = driver.find_element(By.NAME, 'godina')
        dugme = driver.find_element(By.ID, 'unesi')

        naziv.send_keys('Terminator 2')
        godina.send_keys('1991')
        dugme.click()
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.ID, 'modalProjections'))
        )
        modal = driver.find_element(By.ID, 'modalProjections')

        assert 'Uspesno ste uneli film u bazu podataka!' in modal.text

    @patch('cineverse.views.insertFilm')
    def test_dodajFilmNeuspesnoBezGodine(self, mock_insertFilm):
        driver = self.driver
        mock_insertFilm.return_value = 'Zadati film nije pronadjen. Pokusajte da specificirate i godinu.'
        self.loginAsAdmin()

        driver.get(f'{self.live_server_url}/adminPortal/dodajFilm')

        naziv = driver.find_element(By.NAME, 'naziv')
        dugme = driver.find_element(By.ID, 'unesi')

        naziv.send_keys('asdf')

        dugme.click()
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.ID, 'modalProjections'))
        )
        modal = driver.find_element(By.ID, 'modalProjections')

        assert 'Zadati film nije pronadjen. Pokusajte da specificirate i godinu.' in modal.text

    @patch('cineverse.views.insertFilm')
    def test_dodajFilmNeuspesnoSaGodinom(self, mock_insertFilm):
        driver = self.driver
        mock_insertFilm.return_value = 'Zadati film nije pronadjen.'
        self.loginAsAdmin()

        driver.get(f'{self.live_server_url}/adminPortal/dodajFilm')

        naziv = driver.find_element(By.NAME, 'naziv')
        godina = driver.find_element(By.NAME, 'godina')
        dugme = driver.find_element(By.ID, 'unesi')

        naziv.send_keys('asdf')
        godina.send_keys('1991')

        dugme.click()
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.ID, 'modalProjections'))
        )
        modal = driver.find_element(By.ID, 'modalProjections')

        assert 'Zadati film nije pronadjen.' in modal.text

    def test_unosProjekcijeUspesno(self):
        driver = self.driver
        self.loginAsAdmin()
        Film.objects.create(naziv='Terminator 2: Sudnji dan', originalninaziv='', trajanje=131,
                            pocetakprikazivanja='2024-06-06',
                            reziseri='', glumci='', krataksadrzaj='', radnja='', ocenaimdb=7.7, ocenakorisnika=2.5,
                            slika='', sredjennaziv='')

        Termin.objects.create(termin="19:00")
        s = Sala.objects.create()

        driver.get(f'{self.live_server_url}/adminPortal/dodajProjekciju')

        naziv = driver.find_element(By.ID, 'nazivFilmaSelect')
        datum = driver.find_element(By.NAME, 'datum')
        termin = driver.find_element(By.ID, 'terminFilmaSelect')
        sala = driver.find_element(By.ID, 'salaSelect')
        dugme = driver.find_element(By.ID, 'unesiProjekciju')
        selectNaziv = Select(naziv)
        selectNaziv.select_by_visible_text("Terminator 2: Sudnji dan")
        selectTermin = Select(termin)
        selectSala = Select(sala)
        datum.send_keys('07/02/2024')
        selectTermin.select_by_visible_text("19:00h")
        selectSala.select_by_visible_text(f"Sala {s.idsal}")
        dugme.click()

        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.ID, 'modalProjections'))
        )
        modal = driver.find_element(By.ID, 'modalProjections')

        assert 'Uspešno ste uneli projekciju u bazu podataka!' in modal.text

    def test_unosProjekcijeNeuspesno(self):
        driver = self.driver
        self.loginAsAdmin()

        f = Film.objects.create(naziv='Terminator 2: Sudnji dan', originalninaziv='', trajanje=131,
                                pocetakprikazivanja='2024-06-06',
                                reziseri='', glumci='', krataksadrzaj='', radnja='', ocenaimdb=7.7, ocenakorisnika=2.5,
                                slika='', sredjennaziv='')
        t = Termin.objects.create(termin="21:00")
        s = Sala.objects.create()
        Projekcija.objects.create(datum='08.06.2024', idfil=f, idsal=s, idter=t)

        driver.get(f'{self.live_server_url}/adminPortal/dodajProjekciju')

        naziv = driver.find_element(By.ID, 'nazivFilmaSelect')
        datum = driver.find_element(By.NAME, 'datum')
        termin = driver.find_element(By.ID, 'terminFilmaSelect')
        sala = driver.find_element(By.ID, 'salaSelect')
        dugme = driver.find_element(By.ID, 'unesiProjekciju')
        selectNaziv = Select(naziv)
        selectNaziv.select_by_visible_text("Terminator 2: Sudnji dan")
        selectTermin = Select(termin)
        selectSala = Select(sala)
        datum.send_keys('08/06/2024')
        selectTermin.select_by_visible_text("21:00h")
        selectSala.select_by_visible_text(f"Sala {s.idsal}")
        dugme.click()

        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.ID, 'modalProjections'))
        )
        modal = driver.find_element(By.ID, 'modalProjections')

        assert 'Odabrana sala je zauzeta u zadatom terminu' in modal.text

        Projekcija.objects.all().delete()
        Film.objects.all().delete()
        Termin.objects.all().delete()
        Sala.objects.all().delete()

    def test_ukloniNalog(self):
        driver = self.driver
        self.loginAsAdmin()
        Nalog.objects.create(username="test", email="test@gmail.com", password="testest123", uloga="K")

        driver.get(f'{self.live_server_url}/adminPortal/korisnickiNalozi')

        detalji = driver.find_element(By.XPATH, "//div[contains(@class, 'list-group')]")

        list_group_items = detalji.find_elements(By.XPATH, ".//div[contains(@class, 'list-group-item')]")

        for item in list_group_items:

            if "test@gmail.com" in item.text:
                dugme = item.find_element(By.XPATH, ".//button[contains(@class, 'odbijDugme')]")
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable(dugme))
                dugme.click()
                WebDriverWait(driver, 30).until(
                    EC.visibility_of_element_located((By.ID, 'confirmDeleteModal'))
                )
                modal = driver.find_element(By.ID, 'confirmDeleteModal')
                prihvatiDugme = modal.find_element(By.XPATH, ".//button[contains(@class, 'prihvatiModalDugme')]")
                prihvatiDugme.click()
                break

        time.sleep(10)
        assert "test@gmail.com" not in driver.page_source


class korisnikTests(StaticLiveServerTestCase):
    def setUp(self):
        self.user = Nalog.objects.create(
            password='pbkdf2_sha256$720000$xnTxOoovx2hzpv9JR0WS8H$+0EOUI9JqgIXduGi1b2WIhifYuFcC39thGcSFCMp3yg='
            , is_superuser=0, username='lancitest', first_name='', last_name='',
            email='lanatest@gmail.com', is_staff=0, is_active=1, uloga='K')
        self.driver = webdriver.Chrome()

    def tearDown(self):
        Watchlist.objects.all().delete()
        Film.objects.all().delete()
        Ocenjuje.objects.all().delete()
        self.driver.close()
        

    def loginAsKorisnik(self):
        driver = self.driver
        driver.get(f'{self.live_server_url}/login')

        username = driver.find_element(By.NAME, 'username')
        password = driver.find_element(By.NAME, 'password')
        login_button = driver.find_element(By.ID, 'btn-login')

        username.send_keys('lancitest')
        password.send_keys('lanalana123')
        login_button.click()

    def test_prikazWatchliste(self):
        driver = self.driver
        self.loginAsKorisnik()

        f1 = Film.objects.create(naziv='Terminator 1', originalninaziv='', trajanje=131,
                                 pocetakprikazivanja='2024-06-06',
                                 reziseri='', glumci='', krataksadrzaj='', radnja='', ocenaimdb=7.7, ocenakorisnika=2.5,
                                 slika='', sredjennaziv='')
        Watchlist.objects.create(idkor=self.user, idfil=f1)

        driver.get(f'{self.live_server_url}/mojProfil')

        elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//ul[@id='watchlist-items']/li/div"))
        )
        self.assertEquals(1, len(elements))
        self.assertIn('Terminator 1', elements[0].get_attribute("outerHTML"))

    def test_prikazOcenjenihFilmova(self):
        driver = self.driver
        self.loginAsKorisnik()

        f1 = Film.objects.create(naziv='Terminator 1', originalninaziv='', trajanje=131,
                                 pocetakprikazivanja='2024-06-06',
                                 reziseri='', glumci='', krataksadrzaj='', radnja='', ocenaimdb=7.7, ocenakorisnika=2.5,
                                 slika='', sredjennaziv='')
        Ocenjuje.objects.create(idkor=self.user, idfil=f1, ocena=5)

        driver.get(f'{self.live_server_url}/mojProfil')

        elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//ul[@id='graded-items']/li/div"))
        )
        self.assertEquals(1, len(elements))
        self.assertIn('Terminator 1', elements[0].get_attribute("outerHTML"))
        self.assertIn('5/5', elements[0].get_attribute("outerHTML"))


class gostTests(StaticLiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.user = Nalog.objects.create(
            password='pbkdf2_sha256$720000$xnTxOoovx2hzpv9JR0WS8H$+0EOUI9JqgIXduGi1b2WIhifYuFcC39thGcSFCMp3yg=',
            is_superuser=0, username='lancitest', first_name='', last_name='',
            email='lanatest@gmail.com', is_staff=0, is_active=1, uloga='K')

    def tearDown(self):
        Film.objects.all().delete()
        self.driver.close()

    def test_prikazPojedinacnogFilma(self):
        driver = self.driver

        f = Film.objects.create(naziv='Terminator', originalninaziv='', trajanje=131,
                                pocetakprikazivanja='2024-06-06',
                                reziseri='', glumci='', krataksadrzaj='', radnja='', ocenaimdb=7.7, ocenakorisnika=2.5,
                                slika='', sredjennaziv='')

        driver.get(f'{self.live_server_url}/najboljeOcenjeni')

        naslov = driver.find_element(By.XPATH, f"//div[@id='CARD-{f.idfil}']/div[2]/div/div/a/h5")
        naslov.click()

        imeFilma = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//h2'))
        )
        self.assertIn('Terminator', imeFilma.text)
    
    def test_najboljeOcenjeni(self):
        driver = self.driver

        film1 = Film.objects.create(
            naziv='Terminator 1', originalninaziv='Terminator 1', trajanje=120, 
            pocetakprikazivanja='2023-01-01', reziseri='Director 1', glumci='Actor 1', 
            krataksadrzaj='Description 1', radnja='Plot 1', ocenaimdb=8.0, ocenakorisnika=4.0, 
            slika='image1.jpg', sredjennaziv='terminator1'
        )
        
        film2 = Film.objects.create(
            naziv='Terminator 2', originalninaziv='Terminator 2', trajanje=130, 
            pocetakprikazivanja='2024-01-01', reziseri='Director 2', glumci='Actor 2', 
            krataksadrzaj='Description 2', radnja='Plot 2', ocenaimdb=9.0, ocenakorisnika=4.5, 
            slika='image2.jpg', sredjennaziv='terminator2'
        )

        driver.get(f'{self.live_server_url}/najboljeOcenjeni')

        first_card = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@id="cards-holder"]/div[@class="card"]'))
        )

        imdb_score = float(first_card.get_attribute('data-imdb'))

        self.assertEqual(imdb_score, 9.0)


    def test_najvisaOcenaKorisnika(self):
        driver = self.driver

        film1 = Film.objects.create(
            naziv='Terminator 1', originalninaziv='Terminator 1', trajanje=120, 
            pocetakprikazivanja='2023-01-01', reziseri='Director 1', glumci='Actor 1', 
            krataksadrzaj='Description 1', radnja='Plot 1', ocenaimdb=8.0, ocenakorisnika=4.5, 
            slika='image1.jpg', sredjennaziv='terminator1'
        )
        
        film2 = Film.objects.create(
            naziv='Terminator 2', originalninaziv='Terminator 2', trajanje=130, 
            pocetakprikazivanja='2024-01-01', reziseri='Director 2', glumci='Actor 2', 
            krataksadrzaj='Description 2', radnja='Plot 2', ocenaimdb=9.0, ocenakorisnika=4.0, 
            slika='image2.jpg', sredjennaziv='terminator2'
        )

        driver.get(f'{self.live_server_url}/najboljeOcenjeni')

        dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'myDropdown'))
        )

        dropdown.click()

        option_korisnik = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//select[@id="myDropdown"]/option[2]'))
        )
        option_korisnik.click()

        first_card = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@id="cards-holder"]/div[@class="card"]'))
        )

        ocena_korisnika = float(first_card.get_attribute('data-korisnikocena'))

        self.assertEqual(ocena_korisnika, 4.5)

    def test_login_uspeh(self):
        driver = self.driver
        driver.get(f'{self.live_server_url}/login')

        username = driver.find_element(By.NAME, 'username')
        password = driver.find_element(By.NAME, 'password')
        login_button = driver.find_element(By.ID, 'btn-login')

        username.send_keys('lancitest')
        password.send_keys('lanalana123')
        login_button.click()

        current_url = driver.current_url
        self.assertEqual(current_url, f'{self.live_server_url}/')

    def test_login_neuspeh(self):
        driver = self.driver
        driver.get(f'{self.live_server_url}/login')

        username = driver.find_element(By.NAME, 'username')
        password = driver.find_element(By.NAME, 'password')
        login_button = driver.find_element(By.ID, 'btn-login')

        username.send_keys('lancitest')
        password.send_keys('lanalana1234')
        login_button.click()
        
        modal = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//form[@id='loginForm']/div/ul/li"))
        )
        self.assertEqual("Unesite validne podatke.", modal.text)


    def test_registracija_neuspesna_los_email(self):
        driver = self.driver
        driver.get(f'{self.live_server_url}/login')
        register_button = driver.find_element(By.XPATH, "(//button[@type='button'])[3]")

        register_button.click()

        email = driver.find_element(By.NAME, 'email')
        username = driver.find_element(By.NAME, 'username')
        password1 = driver.find_element(By.NAME, 'password1')
        password2 = driver.find_element(By.NAME, 'password2')

        new_register_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        email.send_keys('losmejl@mejl')
        username.send_keys('noviaccount')
        password1.send_keys('beverli123#')
        password2.send_keys('beverli123#')
        new_register_button.click()

        modal = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//form/div/div[2]"))
        )

        self.assertEqual("Enter a valid email address.", modal.text)

    def test_registracija_neuspesna_ime_i_sifra_slicni(self):
        driver = self.driver
        driver.get(f'{self.live_server_url}/login')
        register_button = driver.find_element(By.XPATH, "(//button[@type='button'])[3]")

        register_button.click()

        email = driver.find_element(By.NAME, 'email')
        username = driver.find_element(By.NAME, 'username')
        password1 = driver.find_element(By.NAME, 'password1')
        password2 = driver.find_element(By.NAME, 'password2')

        new_register_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        email.send_keys('dobarmejl@gmail.com')
        username.send_keys('beverli123#')
        password1.send_keys('beverli123#')
        password2.send_keys('beverli123#')
        new_register_button.click()

        modal = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[4]/div[2]"))
        )

        self.assertEqual("The password is too similar to the username.", modal.text)

    def test_registracija_neuspesna_sifra_nije_jaka(self):
        driver = self.driver
        driver.get(f'{self.live_server_url}/login')
        register_button = driver.find_element(By.XPATH, "(//button[@type='button'])[3]")

        register_button.click()

        email = driver.find_element(By.NAME, 'email')
        username = driver.find_element(By.NAME, 'username')
        password1 = driver.find_element(By.NAME, 'password1')
        password2 = driver.find_element(By.NAME, 'password2')

        new_register_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        email.send_keys('dobarmejl@gmail.com')
        username.send_keys('USERNAME123')
        password1.send_keys('123#')
        password2.send_keys('123#')
        new_register_button.click()

        modal = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[4]/div[2]"))
        )

        self.assertEqual("Lozinka mora sadržati najmanje 8 karaktera!", modal.text)

    def test_registracija_neuspesna_sifre_nisu_iste(self):
        driver = self.driver
        driver.get(f'{self.live_server_url}/login')
        register_button = driver.find_element(By.XPATH, "(//button[@type='button'])[3]")

        register_button.click()

        email = driver.find_element(By.NAME, 'email')
        username = driver.find_element(By.NAME, 'username')
        password1 = driver.find_element(By.NAME, 'password1')
        password2 = driver.find_element(By.NAME, 'password2')

        new_register_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        email.send_keys('dobarmejl@gmail.com')
        username.send_keys('USERNAME123')
        password1.send_keys('abababab123#')
        password2.send_keys('abababab123!')
        new_register_button.click()

        modal = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[4]/div[2]"))
        )

        self.assertEqual("Lozinke se ne poklapaju!", modal.text)

    def test_registracija_username_vec_postoji(self):
        Nalog.objects.create(
            password='nebitno',
            is_superuser=0, username='ristovic', first_name='', last_name='', email='ristovic@gmail.com', is_staff=0,
            is_active=1, uloga='K')

        driver = self.driver
        driver.get(f'{self.live_server_url}/login')
        register_button = driver.find_element(By.XPATH, "(//button[@type='button'])[3]")

        register_button.click()

        email = driver.find_element(By.NAME, 'email')
        username = driver.find_element(By.NAME, 'username')
        password1 = driver.find_element(By.NAME, 'password1')
        password2 = driver.find_element(By.NAME, 'password2')

        new_register_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        email.send_keys('NEMOGUVISE@gmail.com')
        username.send_keys('ristovic')
        password1.send_keys('abababab123#')
        password2.send_keys('abababab123#')
        new_register_button.click()

        modal = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[2]/div[2]"))
        )

        self.assertEqual("Korisničko ime već postoji!", modal.text)

    def test_registracija_email_vec_postoji(self):
        Nalog.objects.create(
            password='nebitno',
            is_superuser=0, username='ristovic', first_name='', last_name='', email='ristovic@gmail.com', is_staff=0,
            is_active=1, uloga='K')

        driver = self.driver
        driver.get(f'{self.live_server_url}/login')
        register_button = driver.find_element(By.XPATH, "(//button[@type='button'])[3]")

        register_button.click()

        email = driver.find_element(By.NAME, 'email')
        username = driver.find_element(By.NAME, 'username')
        password1 = driver.find_element(By.NAME, 'password1')
        password2 = driver.find_element(By.NAME, 'password2')

        new_register_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        email.send_keys('ristovic@gmail.com')
        username.send_keys('OCUDAPOPIZDIMVISE')
        password1.send_keys('AMANZAMAN123#')
        password2.send_keys('AMANZAMAN123#')
        new_register_button.click()

        modal = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//form/div/div[2]"))
        )

        self.assertEqual("Email već postoji!", modal.text)


class viewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Nalog.objects.create(
            password='pbkdf2_sha256$720000$xnTxOoovx2hzpv9JR0WS8H$+0EOUI9JqgIXduGi1b2WIhifYuFcC39thGcSFCMp3yg=',
            is_superuser=0, username='lancitest', first_name='', last_name='', email='lanatest@gmail.com', is_staff=0,
            is_active=1, uloga='K')
    
        self.admin = Nalog.objects.create(
            password='pbkdf2_sha256$720000$1KJQrllZTOKCv0gy5PrDYS$rvFzw/jWVcZlGCAroCwsLrd4WFep+1l8LPgJEGJn1QE=',
            is_superuser=1, username='admin', first_name='', last_name='', email='superuser@gmail.com', is_staff=1,
            is_active=1, uloga='A')

    def tearDown(self):
        Film.objects.all().delete()
        Ocenjuje.objects.all().delete()
        Watchlist.objects.all().delete()
        Predlaze.objects.all().delete()
        Termin.objects.all().delete()
        Sala.objects.all().delete()
        Projekcija.objects.all().delete()

    @patch('cineverse.models.Predlaze.objects.create')
    def test_uspesno_dodavanje_predloga(self, mock_create):
        # GIVEN
        self.client.login(username='lancitest', password='lanalana123')
        mock_create.return_value = MagicMock(Predlaze)
        expected_output = JsonResponse({"success": True})

        # WHEN
        response = self.client.get('/dodajPredlog', {'imeFilma': 'Terminator'})

        # THEN
        self.assertEquals(expected_output.status_code, response.status_code)
        self.assertJSONEqual(expected_output.content, response.content.decode('utf-8'))

    @patch('cineverse.models.Projekcija.objects.filter')
    def test_predlog_vec_u_ponudi(self, mock_filter):
        # GIVEN
        self.client.login(username='lancitest', password='lanalana123')
        mock_queryset = MagicMock()
        mock_queryset.exists.return_value = True
        mock_filter.return_value = mock_queryset
        expected_output = JsonResponse({"error": "Vec u ponudi"}, status=400)

        # WHEN
        response = self.client.get('/dodajPredlog', {'imeFilma': 'Terminator'})

        # THEN
        self.assertEquals(expected_output.status_code, response.status_code)
        self.assertJSONEqual(expected_output.content, response.content.decode('utf-8'))

    @patch('cineverse.models.Predlaze.objects.filter')
    def test_predlog_vec_predlozio(self, mock_filter):
        # GIVEN
        self.client.login(username='lancitest', password='lanalana123')
        mock_queryset = MagicMock()
        mock_queryset.exists.return_value = True
        mock_filter.return_value = mock_queryset
        expected_output = JsonResponse({"error": "Vec predlozio"}, status=400)

        # WHEN
        response = self.client.get('/dodajPredlog', {'imeFilma': 'Terminator'})

        # THEN
        self.assertEquals(expected_output.status_code, response.status_code)
        self.assertJSONEqual(expected_output.content, response.content.decode('utf-8'))

    def test_uspesno_obrisan_film_iz_watchliste(self):
        # GIVEN
        self.client.login(username='lancitest', password='lanalana123')
        f = Film.objects.create(naziv='Terminator', originalninaziv='', trajanje=131,
                                pocetakprikazivanja='2024-06-06',
                                reziseri='', glumci='', krataksadrzaj='', radnja='', ocenaimdb=7.7, ocenakorisnika=2.5,
                                slika='', sredjennaziv='')
        Watchlist.objects.create(idkor=self.user, idfil=f)
        expected_output = JsonResponse({'ok': True})

        # WHEN
        response = self.client.post('/ukloniIzWatchliste', data=json.dumps({'idfil': f.idfil}),
                                    content_type='application/json')

        # THEN
        self.assertEqual(expected_output.status_code, response.status_code)
        self.assertJSONEqual(expected_output.content, response.content.decode('utf-8'))
        self.assertFalse(Watchlist.objects.filter(idkor=self.user, idfil=f).exists())

    def test_film_nije_u_watchlisti_ukloni(self):
        # GIVEN
        self.client.login(username='lancitest', password='lanalana123')
        f = Film.objects.create(naziv='Terminator', originalninaziv='', trajanje=131,
                                pocetakprikazivanja='2024-06-06',
                                reziseri='', glumci='', krataksadrzaj='', radnja='', ocenaimdb=7.7, ocenakorisnika=2.5,
                                slika='', sredjennaziv='')
        expected_output = JsonResponse({'ok': False, 'error': 'Film nije u watchlisti'})

        # WHEN
        response = self.client.post('/ukloniIzWatchliste', data=json.dumps({'idfil': f.idfil}),
                                    content_type='application/json')

        # THEN
        self.assertEqual(expected_output.status_code, response.status_code)
        self.assertJSONEqual(expected_output.content, response.content.decode('utf-8'))

    def test_ukloni_iz_watchliste_nije_post(self):
        # GIVEN
        self.client.login(username='lancitest', password='lanalana123')
        expected_output = JsonResponse({'ok': False, 'error': 'Request method mora biti POST'}, status=400)

        # WHEN
        response = self.client.get('/ukloniIzWatchliste')

        # THEN
        self.assertEqual(expected_output.status_code, response.status_code)
        self.assertJSONEqual(expected_output.content, response.content.decode('utf-8'))

    def test_uspesan_prikaz_mog_profila(self):
        # GIVEN
        self.client.login(username='lancitest', password='lanalana123')
        f = Film.objects.create(naziv='Terminator', originalninaziv='', trajanje=131,
                                pocetakprikazivanja='2024-06-06',
                                reziseri='', glumci='', krataksadrzaj='', radnja='', ocenaimdb=7.7, ocenakorisnika=2.5,
                                slika='', sredjennaziv='')
        Watchlist.objects.create(idkor=self.user, idfil=f)
        o = Ocenjuje.objects.create(idkor=self.user, idfil=f, ocena=5)

        # WHEN
        response = self.client.get('/mojProfil')

        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'userProfile.html')
        self.assertIn('watchlist', response.context)
        self.assertIn('ocenjeni', response.context)
        self.assertEqual(list(response.context['watchlist']), [f])
        self.assertEqual(list(response.context['ocenjeni']), [o])

    def test_oceni_film(self):
        # GIVEN
        self.client.login(username='lancitest', password='lanalana123')
        expected_output = JsonResponse({'novaOcena': 5}, status=200)
        f = Film.objects.create(naziv='Terminator', originalninaziv='', trajanje=131,
                                pocetakprikazivanja='2024-06-06',
                                reziseri='', glumci='', krataksadrzaj='', radnja='', ocenaimdb=7.7, ocenakorisnika=2.5,
                                slika='', sredjennaziv='')

        # WHEN
        response = self.client.post('/oceniFilm', {'ocena': 5, 'nazivFilma': 'Terminator'})

        # THEN
        self.assertEquals(expected_output.status_code, response.status_code)
        self.assertJSONEqual(expected_output.content, response.content.decode('utf-8'))

    def test_promeni_ocenu(self):
        # GIVEN
        self.client.login(username='lancitest', password='lanalana123')
        expected_output = JsonResponse({'novaOcena': 3}, status=200)
        f = Film.objects.create(naziv='Terminator', originalninaziv='', trajanje=131,
                                pocetakprikazivanja='2024-06-06',
                                reziseri='', glumci='', krataksadrzaj='', radnja='', ocenaimdb=7.7, ocenakorisnika=2.5,
                                slika='', sredjennaziv='')
        Ocenjuje.objects.create(idkor=self.user, idfil=f, ocena=5)

        # WHEN
        response = self.client.post('/oceniFilm', {'ocena': 3, 'nazivFilma': 'Terminator'})

        # THEN
        self.assertEquals(expected_output.status_code, response.status_code)
        self.assertJSONEqual(expected_output.content, response.content.decode('utf-8'))

    def test_pregledi_flma_NO(self):
        # GIVEN
        self.client.login(username='lancitest', password='lanalana123')
        f = Film.objects.create(naziv='Terminator', originalninaziv='', trajanje=131,
                                pocetakprikazivanja='2024-06-06',
                                reziseri='', glumci='', krataksadrzaj='', radnja='', ocenaimdb=7.7, ocenakorisnika=2.5,
                                slika='', sredjennaziv='')

        # WHEN
        response = self.client.get('/pregledFilmaNO', {'parametar': 'Terminator'})

        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pregledFilma.html')
        self.assertIn('film', response.context)
        self.assertEqual(response.context['film'], f)
        self.assertIn('nazivFilma', response.context)
        self.assertEqual(response.context['nazivFilma'], f.naziv)

    def test_pregled_filma(self):
        # GIVEN
        self.client.login(username='lancitest', password='lanalana123')
        f = Film.objects.create(naziv='Terminator', originalninaziv='', trajanje=131,
                                pocetakprikazivanja='2024-06-06',
                                reziseri='', glumci='', krataksadrzaj='', radnja='', ocenaimdb=7.7, ocenakorisnika=2.5,
                                slika='', sredjennaziv='')

        # WHEN
        response = self.client.get('/pregledFilma/Terminator')

        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pregledFilma.html')
        self.assertIn('film', response.context)
        self.assertEqual(response.context['film'], f)
        self.assertIn('nazivFilma', response.context)
        self.assertEqual(response.context['nazivFilma'], f.naziv)

    def test_fetch_grades(self):
        # GIVEN
        self.client.login(username='lancitest', password='lanalana123')
        f = Film.objects.create(naziv='Terminator', originalninaziv='', trajanje=131,
                                pocetakprikazivanja='2024-06-06',
                                reziseri='', glumci='', krataksadrzaj='', radnja='', ocenaimdb=7.7, ocenakorisnika=2.5,
                                slika='', sredjennaziv='')
        o = Ocenjuje.objects.create(idkor=self.user, idfil=f, ocena=5)
        expected_output = JsonResponse(
            {'gradedItems': [{'idfil': f.idfil, 'naziv': f.naziv, 'slika': f.slika, 'ocena': o.ocena}]})

        # WHEN
        response = self.client.get('/fetchGrades')

        # THEN
        self.assertEquals(expected_output.status_code, response.status_code)
        self.assertJSONEqual(expected_output.content, response.content.decode('utf-8'))

    def test_fetch_watchlist(self):
        # GIVEN
        self.client.login(username='lancitest', password='lanalana123')
        f = Film.objects.create(naziv='Terminator', originalninaziv='', trajanje=131,
                                pocetakprikazivanja='2024-06-06',
                                reziseri='', glumci='', krataksadrzaj='', radnja='', ocenaimdb=7.7, ocenakorisnika=2.5,
                                slika='', sredjennaziv='')
        o = Watchlist.objects.create(idkor=self.user, idfil=f)
        expected_output = JsonResponse({'watchlist': [{'idfil': f.idfil, 'naziv': f.naziv, 'slika': f.slika}]})

        # WHEN
        response = self.client.get('/fetchWatchlist')

        # THEN
        self.assertEquals(expected_output.status_code, response.status_code)
        self.assertJSONEqual(expected_output.content, response.content.decode('utf-8'))

    @patch('cineverse.views.insertFilm')
    def test_uspesnoDodatFilm(self, mock_insertFilm):
        # GIVEN
        self.client.login(username='admin', password='superuser123')
        mock_insertFilm.return_value = 'Uspesno ste uneli film u bazu podataka!'

        # WHEN
        response = self.client.post('/adminPortal/dodajFilm', {'naziv': 'Terminator 2', 'godina': 1991})

        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adminTemplates/dodajFilm.html')
        self.assertEqual(response.context['modalMessage'], mock_insertFilm.return_value)

    @patch('cineverse.views.insertFilm')
    def test_neuspesnoDodatFilmBezGodine(self, mock_insertFilm):
        # GIVEN
        self.client.login(username='admin', password='superuser123')
        mock_insertFilm.return_value = 'Zadati film nije pronadjen. Pokusajte da specificirate i godinu.'

        # WHEN
        response = self.client.post('/adminPortal/dodajFilm', {'naziv': 'Terminator 2', 'godina': ""})

        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adminTemplates/dodajFilm.html')
        self.assertEqual(response.context['modalMessage'], mock_insertFilm.return_value)

    @patch('cineverse.views.insertFilm')
    def test_neuspesnoDodatFilmSaGodinom(self, mock_insertFilm):
        # GIVEN
        self.client.login(username='admin', password='superuser123')
        mock_insertFilm.return_value = 'Zadati film nije pronadjen.'

        # WHEN
        response = self.client.post('/adminPortal/dodajFilm', {'naziv': 'Terminator 2', 'godina': 1991})

        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adminTemplates/dodajFilm.html')
        self.assertEqual(response.context['modalMessage'], mock_insertFilm.return_value)

    def test_uspesnoDodataProjekcija(self):
        # GIVEN
        self.client.login(username='admin', password='superuser123')

        Film.objects.create(naziv='Terminator 2: Sudnji dan', originalninaziv='', trajanje=131,
                            pocetakprikazivanja='2024-01-01',
                            reziseri='', glumci='', krataksadrzaj='', radnja='', ocenaimdb=7.7, ocenakorisnika=2.5,
                            slika='', sredjennaziv='')

        Termin.objects.create(termin="19:00")
        s = Sala.objects.create()

        # WHEN
        response = self.client.post('/adminPortal/dodajProjekciju',
                                    {'datum': '2024-01-17', 'sala': s.idsal, 'termin': '19:00',
                                     'film': "Terminator 2: Sudnji dan"})

        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adminTemplates/dodajProjekciju.html')
        self.assertEqual(response.context['modalMessage'], 'Uspešno ste uneli projekciju u bazu podataka!')

    def test_neuspesnoDodataProjekcija(self):
        # GIVEN
        self.client.login(username='admin', password='superuser123')

        f = Film.objects.create(naziv='Terminator 2: Sudnji dan', originalninaziv='', trajanje=131,
                                pocetakprikazivanja='2024-01-01',
                                reziseri='', glumci='', krataksadrzaj='', radnja='', ocenaimdb=7.7, ocenakorisnika=2.5,
                                slika='', sredjennaziv='')

        t = Termin.objects.create(termin="19:00")
        s = Sala.objects.create()
        Projekcija.objects.create(idfil=f, idter=t, idsal=s, datum='17.01.2024')

        # WHEN
        response = self.client.post('/adminPortal/dodajProjekciju',
                                    {'datum': '2024-01-17', 'sala': s.idsal, 'termin': '19:00',
                                     'film': "Terminator 2: Sudnji dan"})

        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adminTemplates/dodajProjekciju.html')
        self.assertEqual(response.context['modalMessage'], 'Odabrana sala je zauzeta u zadatom terminu')

    @patch("cineverse.views.deleteKorisnik")
    @patch("cineverse.views.emailUser")
    def test_uspesnoBrisanjeNaloga(self, mock_emailUser, mock_deleteKorisnik):
        # GIVEN
        self.client.login(username='admin', password='superuser123')

        n1 = Nalog.objects.create(username='test1', password='test123', uloga='K', email='test@gmail.com')
        n2 = Nalog.objects.create(username='test2', password='test123', uloga='K', email='test2@gmail.com')

        # WHEN
        response = self.client.get('/adminPortal/korisnickiNalozi')

        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adminTemplates/korisnickiNalozi.html')
        self.assertEqual(len(response.context['users']), 3)

        # WHEN
        response = self.client.post('/adminPortal/korisnickiNalozi', {'korisnickoime':'test1', 'email':'test@gmail.com'})

        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adminTemplates/korisnickiNalozi.html')
        mock_deleteKorisnik.assert_called_once()
        mock_emailUser.assert_called_once()

    @patch("cineverse.views.fromZahtevToKorisnik")
    @patch("cineverse.views.emailUser")
    def test_uspesnoPrihvatanjeZahteva(self, mock_emailUser, mock_fromZahtevToKorisnik):
        # GIVEN
        self.client.login(username='admin', password='superuser123')

        n1 = Nalog.objects.create(username='test1', password='test123', uloga='Z', email='test@gmail.com')
        n2 = Nalog.objects.create(username='test2', password='test123', uloga='Z', email='test2@gmail.com')

        # WHEN
        response = self.client.get('/adminPortal/korisnickiZahtevi')

        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adminTemplates/korisnickiZahtevi.html')
        self.assertEqual(len(response.context['users']), 2)

        # WHEN
        response = self.client.post('/adminPortal/korisnickiZahtevi',
                                    {'korisnickoime': 'test1', 'email': 'test@gmail.com', 'action':'prihvati'})

        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adminTemplates/korisnickiZahtevi.html')
        mock_emailUser.assert_called_once()
        mock_fromZahtevToKorisnik.assert_called_once()

    @patch("cineverse.views.deleteZahtev")
    def test_uspesnoOdbijanjeZahteva(self, mock_deleteZahtev):
        # GIVEN
        self.client.login(username='admin', password='superuser123')

        n1 = Nalog.objects.create(username='test1', password='test123', uloga='Z', email='test@gmail.com')
        n2 = Nalog.objects.create(username='test2', password='test123', uloga='Z', email='test2@gmail.com')

        # WHEN
        response = self.client.get('/adminPortal/korisnickiZahtevi')

        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adminTemplates/korisnickiZahtevi.html')
        self.assertEqual(len(response.context['users']), 2)

        # WHEN
        response = self.client.post('/adminPortal/korisnickiZahtevi',
                                    {'korisnickoime': 'test1', 'email': 'test@gmail.com', 'action': 'odbij'})

        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adminTemplates/korisnickiZahtevi.html')
        mock_deleteZahtev.assert_called_once()

    @patch('cineverse.models.Predlaze.objects.filter')
    @patch('cineverse.models.Predlaze.objects.all')
    def test_uspesnoPrihvatanjePredloga(self, mock_all, mock_filter):
        # GIVEN
        self.client.login(username='admin', password='superuser123')
        mock_queryset = MagicMock()
        mock_queryset.exists.return_value = True
        mock_queryset.delete.return_value = None
        mock_filter.return_value = mock_queryset
        mock_all.return_value = []

        # WHEN
        response = self.client.get('/adminPortal/korisnickiPredlozi')

        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adminTemplates/korisnickiPredlozi.html')

        # WHEN
        response = self.client.post('/adminPortal/korisnickiPredlozi',
                                    {'nazivFilma': 'Terminator 2', 'akcija': 'prihvati'})

        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adminTemplates/dodajFilm.html')
        self.assertEqual(response.context['value'], 'Terminator 2')

    @patch('cineverse.models.Predlaze.objects.filter')
    @patch('cineverse.models.Predlaze.objects.all')
    def test_uspesnoOdbijanjePredloga(self, mock_all, mock_filter):
        # GIVEN
        self.client.login(username='admin', password='superuser123')
        mock_queryset = MagicMock()
        mock_queryset.exists.return_value = True
        mock_queryset.delete.return_value = None
        mock_filter.return_value = mock_queryset
        mock_all.return_value = []

        # WHEN
        response = self.client.get('/adminPortal/korisnickiPredlozi')

        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adminTemplates/korisnickiPredlozi.html')

        # WHEN
        response = self.client.post('/adminPortal/korisnickiPredlozi',
                                    {'nazivFilma': 'Terminator 2', 'akcija': 'odbij'})

        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adminTemplates/korisnickiPredlozi.html')

    @patch('cineverse.views.emailUsersAboutProjections')
    def test_uspesnaPromenaProjekcije(self, mock_emailUsers):
        # GIVEN
        self.client.login(username='admin', password='superuser123')
        f = Film.objects.create(naziv='Terminator 2', originalninaziv='', trajanje=131,
                                pocetakprikazivanja='2024-06-06',
                                reziseri='', glumci='', krataksadrzaj='', radnja='', ocenaimdb=7.7, ocenakorisnika=2.5,
                                slika='', sredjennaziv='')
        t = Termin.objects.create(termin="21:00")
        s = Sala.objects.create()
        p = Projekcija.objects.create(datum='08.06.2024', idfil=f, idsal=s, idter=t)

        # WHEN
        response = self.client.get(f'/adminPortal/promeniProjekciju?film={f.idfil}&vreme=21%3A00&sala={s.idsal}&idpro={p.idpro}')

        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adminTemplates/promeniProjekciju.html')
        self.assertEqual(response.context['nazivfilma'], f.naziv)

        # WHEN
        response = self.client.post('/adminPortal/promeniProjekciju',
                                    {'datum': '2024-06-09', 'termin': t.termin, 'sala': s.idsal, 'idpro': p.idpro})

        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adminTemplates/promeniProjekciju.html')
        self.assertEqual(response.context['modalMessage'], 'Uspešno ste izmenili termin projekcije!')
        mock_emailUsers.assert_called_once()

    @patch('cineverse.views.emailUsersAboutProjections')
    def test_neuspesnaPromenaProjekcije(self, mock_emailUsers):
        # GIVEN
        self.client.login(username='admin', password='superuser123')
        f = Film.objects.create(naziv='Terminator 2', originalninaziv='', trajanje=131,
                                pocetakprikazivanja='2024-06-06',
                                reziseri='', glumci='', krataksadrzaj='', radnja='', ocenaimdb=7.7, ocenakorisnika=2.5,
                                slika='', sredjennaziv='')
        t = Termin.objects.create(termin="21:00")
        s = Sala.objects.create()
        p = Projekcija.objects.create(datum='08.06.2024', idfil=f, idsal=s, idter=t)
        Projekcija.objects.create(datum='09.06.2024', idfil=f, idsal=s, idter=t)

        # WHEN
        response = self.client.get(
            f'/adminPortal/promeniProjekciju?film={f.idfil}&vreme=21%3A00&sala={s.idsal}&idpro={p.idpro}')

        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adminTemplates/promeniProjekciju.html')
        self.assertEqual(response.context['nazivfilma'], f.naziv)

        # WHEN
        response = self.client.post('/adminPortal/promeniProjekciju',
                                    {'datum': '2024-06-09', 'termin': t.termin, 'sala': s.idsal, 'idpro': p.idpro})

        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adminTemplates/promeniProjekciju.html')
        self.assertEqual(response.context['modalMessage'], 'Odabrana sala je zauzeta u zadatom terminu')

    def test_trenutnoUBioskopu(self):
        response = self.client.get(reverse('sviFilmovi'))
        self.assertEqual(response.status_code, 200)

    def test_sveProjekcije(self):
        response = self.client.get(reverse('sveProjekcije'))
        self.assertEqual(response.status_code, 200)


    def test_najboljeOcenjeni(self):
        response = self.client.get(reverse('najboljeOcenjeni'))
        self.assertEqual(response.status_code, 200)

    def test_ocenjeniPoKorisniku(self):

        response = self.client.get(reverse('najboljeOcenjeni'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('najboljeOcenjeni'), {'dropdown_value': 'Korisnika'})  
        self.assertEqual(response.status_code, 200)

    def test_personalizovanPredlog(self):
        f = Film.objects.create(naziv='Terminator 2', originalninaziv='', trajanje=131,
                                pocetakprikazivanja='2024-06-06',
                                reziseri='', glumci='', krataksadrzaj='', radnja='', ocenaimdb=7.7, ocenakorisnika=2.5,
                                slika='', sredjennaziv='')

        url = reverse('landingPage')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        response = self.client.post(url, {'filmInput': 'Godfather', 'zanrInput': 'Tragedija'})

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, '<div class="modal-content" id="MODAL">')

    #login provere
    def test_login_uspesan(self): #web-driver
        login_response = self.client.post("/login/", {'username' : self.user.username, 'password' : "lanalana123"})
        self.assertRedirects(login_response, '/')
        
    def test_login_neuspesan(self): #web-driver
        login_response = self.client.post("/login/", {'username' : self.user.username, 'password' : "NULACA"})
        self.assertTemplateUsed(login_response, 'loginForm.html')

    #register provere
    def test_registracija_uspesna(self): #SELENIUM
        register_response = self.client.post("/register/", {'email' : "nikolatest@gmail.com" , 'username' : "nikola", 'password1' : "beverli123#", 'password2' : "beverli123#"})
        self.assertRedirects(register_response, '/')

    def test_registracija_neuspesna_los_email(self): #web-driver
        register_response = self.client.post("/register/", {'email' : "losmail" , 'username' : "nikola", 'password1' : "beverli123#", 'password2' : "beverli123#"})
        self.assertTemplateUsed(register_response, 'registerForm.html')

    def test_registracija_neuspesna_ime_i_sifra_slicni(self): #web-driver
        register_response = self.client.post("/register/", {'email' : "nikolatest@gmail.com" , 'username' : "nikola", 'password1' : "nikola123#", 'password2' : "nikola123#"})
        self.assertTemplateUsed(register_response, 'registerForm.html')

    def test_registracija_neuspesna_sifra_nije_jaka(self): #web-driver
        register_response = self.client.post("/register/", {'email' : "nikolatest@gmail.com" , 'username' : "nikola", 'password1' : "beverli", 'password2' : "beverli"})
        self.assertTemplateUsed(register_response, 'registerForm.html')

    def test_registracija_neuspesna_sifre_nisu_iste(self): #web-driver
        register_response = self.client.post("/register/", {'email' : "nikolatest@gmail.com" , 'username' : "nikola", 'password1' : "beverli123#", 'password2' : "beverli123!"})
        self.assertTemplateUsed(register_response, 'registerForm.html')

    def test_registracija_username_vec_postoji(self): #web-driver
        Nalog.objects.create(
            password='nebitno',
            is_superuser=0, username='ristovic', first_name='', last_name='', email='ristovic@gmail.com', is_staff=0,
            is_active=1, uloga='K')

        register_response = self.client.post("/register/", {'email' : "nikolatest@gmail.com" , 'username' : "ristovic", 'password1' : "beverli123#", 'password2' : "beverli123#"})
        self.assertTemplateUsed(register_response, 'registerForm.html')

    def test_registracija_email_vec_postoji(self): #web-driver
        Nalog.objects.create(
            password='nebitno',
            is_superuser=0, username='ristovic', first_name='', last_name='', email='ristovic@gmail.com', is_staff=0,
            is_active=1, uloga='K')

        register_response = self.client.post("/register/", {'email' : "ristovic@gmail.com" , 'username' : "nikolica", 'password1' : "beverli123#", 'password2' : "beverli123#"})
        self.assertTemplateUsed(register_response, 'registerForm.html')


    #SELENIUM
    def test_registracija_kratka_sifra(self):
        Nalog.objects.create(
            password='nebitno',
            is_superuser=0, username='ristovic', first_name='', last_name='', email='ristovic@gmail.com', is_staff=0,
            is_active=1, uloga='K')

        register_response = self.client.post("/register/", {'email' : "nikolica@gmail.com" , 'username' : "nikolica", 'password1' : "123#", 'password2' : "123#"})
        self.assertTemplateUsed(register_response, 'registerForm.html')
    

    #watchList
    #SELENIUM iude + 1 ako je dugme izkljuceno
    def test_dodavanje_u_watch_list_uspesno(self):
        self.client.post("/login/", {'username' : self.user.username, 'password' : "lanalana123"})

        f = Film.objects.create(naziv='Terminator 2', originalninaziv='', trajanje=131,
                                pocetakprikazivanja='2024-06-06',
                                reziseri='', glumci='', krataksadrzaj='', radnja='', ocenaimdb=7.7, ocenakorisnika=2.5,
                                slika='', sredjennaziv='')


        dodaj_response_expected = JsonResponse({'ret': 'good'}, status = 200)
        dodaj_response_got = self.client.post("/dodajUWatchList", {"idFilma" : f.idfil})

        self.assertEquals(dodaj_response_expected.status_code, dodaj_response_got.status_code)
        self.assertJSONEqual(dodaj_response_expected.content, dodaj_response_got.content.decode('utf-8'))