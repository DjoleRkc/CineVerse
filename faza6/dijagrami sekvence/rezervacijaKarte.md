autor: Đorđe Pajić


```mermaid
sequenceDiagram
    actor User
    participant Template
    participant View
    participant Model
    participant Database

    User ->> Template: Izaberi datum iz padajućeg menija
    Template ->> View: Pošalji izabrani datum
    View ->> Model: Preuzmi dostupne filmove za izabrani datum
    Model ->> Database: Upit za filmove za izabrani datum
    Database -->> Model: Vrati filmove
    Model -->> View: Vrati filmove
    View -->> Template: Prikaz filmova

    User ->> Template: Izaberi film
    User ->> Template: Klik na dugme rezerviši
    Template ->> View: Pošalji izabrani film
    View ->> Model: Preuzmi dostupne projekcije za izabrani film
    Model ->> Database: Upit za dostupne projekcije za izabrani film
    Database -->> Model: Vrati dostupne projekcije
    Model -->> View: Vrati dostupne projekcije
    View -->> Template: Prikaz dostupnih projekcija

    
    User ->> Template: Klik na jednu od ponuđenih projekcija
    Template ->> View: Preusmeri na ekran za odabir mesta
    
    alt Manje dostupnih mesta nego što korisnik želi
        User ->> Template: Povratak na prethodnu stranu
    else
        alt Željena mesta su rasprodata
            User ->> Template: Povratak na prethodnu stranu
        else

        User ->> Template: Izaberi mesta
        User ->> Template: Klik na dugme rezerviši
        Template ->> View: Pošalji izabrana mesta
        View -->> Template: Prikaži modal sa potvrdom rezervacije
    
        User ->> Template: Klik na dugme potvrdi rezervaciju
        Template ->> View: Potvrda rezervacije
        View ->> Model: Rezerviši izabrana mesta
        Model ->> Database: Rezerviši izabrana mesta
        Database -->> Model: Vrati zauzeta mesta
        Model -->> View: Vrati zauzeta mesta
        View -->> Template: Prikaz zauzeta mesta
        Model -->> User: Pošalji email sa potvrdom
        end
    end
    
```