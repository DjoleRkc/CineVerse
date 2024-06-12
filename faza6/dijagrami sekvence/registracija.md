Autor: Jovan Babović
```mermaid
sequenceDiagram
    actor Guest
    participant Template
    participant View
    participant Model
    participant Database

    Guest ->> Template: Klik na dugme "Prijava/Registracija"
    View -->> Template: Prikaz stranice za prijavljivanje
    Guest ->> Template: Klik na "Registruj se"
    View -->> Template: Prikaz forme za registraciju
    Guest ->> Template: Unos emaila, korisničkog imena, šifre i ponovljene šifre
    Template ->> View: Pošalji email, korisničko ime, šifru i ponovljenu šifru
    alt Šifra i ponovljena šifra se ne poklapaju
        View -->> Template: Prikaz poruke o nepoklapanju šifre i ponovljene šifre
    else Šifra nije dovoljno jaka
        View -->> Template: Prikaz poruke o slaboj šifri
    else else
        View ->> Model: Registruj korisnika
        Model ->> Database: Registruj korisnika
        alt Email već postoji
            Database -->> Model: Neupsešna registracija jer email već postoji
            Model -->> View: Email već postoji u bazi
            View -->> Template: Prikaz poruke o postojanju email-a
        else Korisničko ime je zauzeto
            Database -->> Model: Neupsešna registracija jer korisničko ime već postoji
            Model -->> View: Korisničko ime već postoji u bazi
            View -->> Template: Prikazuje poruku o postojanju korisničkog imena
        else Uspešna registracija
            Database -->> Model: Uspešna registracija
            Model -->> View: Uspešna registracija
            View -->> Template: Prikaz poruke o uspešnoj registraciji
        end
    end
```

