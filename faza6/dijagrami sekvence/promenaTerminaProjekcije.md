autor: Lana Jovanović

```mermaid
sequenceDiagram
    actor Admin
    participant Template
    participant View
    participant Model
    participant Database
    actor User

    Admin ->> Template: Izaberi datum iz padajućeg menija
    Template ->> View: Pošalji izabrani datum
    View ->> Model: Preuzmi dostupne filmove za izabrani datum
    Model ->> Database: Upit za filmove za izabrani datum
    Database -->> Model: Vrati filmove
    Model -->> View: Vrati filmove
    View -->> Template: Prikaz filmova

    Admin ->> Template: Izaberi film

    alt Admin zeli da promeni termin projekcije
        Admin ->> Template: Klik na dugme izmeni termi projekcije
        Template ->> View: Pošalji izabrani film
        View ->> Model: Preuzmi dostupne projekcije za izabrani film
        Model ->> Database: Upit za dostupne projekcije za izabrani film
        Database -->> Model: Vrati dostupne projekcije
        Model -->> View: Vrati dostupne projekcije
        View -->> Template: Prikaz dostupnih projekcija
        
        Admin->>Template: Odabir željene projekcije
        Template->>View: Pošalji izabranu projekciju
        View-->>Template: Prikaz stranice za izmenu detalja projekcije
        Admin->>Template: Unos nove sale, termina i datuma
        Template->>View: Pošalji salu, termin i datum
        View->>Model: Pošalji salu, termin i datum
        Model->>Database: Promeni salu, termin i datum projekcije
        
        alt Sala je zauzeta u zeljenom terminu
            Database-->>Model: Neuspela promena
            Model-->>View: Neuspela promena jer je sala zauzeta
            View->>Template: Prikaz da je sala zauzeta u željenom terminu
        else Sala je slobodna u zeljenom terminu
            Database-->>Model: Uspešna promena
            Model-->>View: Uspešna promena termina projekcije
            View->>Template: Prikaz da je termin projekcije uspešno promenjen
            View->>User: Pošalji email o novom terminu projekcije za koju imaju rezervaciju
        end
    end
```