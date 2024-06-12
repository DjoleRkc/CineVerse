```mermaid
flowchart TD
    Guest[Gost] --> Registracija
    Guest --> PrikazNajboljeOcenjenih
    Guest --> PrikazFilmovaUBioskopu
    Guest --> PrikazRepertoara
    Guest --> PrikazFilma
    Guest --> PredlogStaGledati    

    subgraph Slučajevi korišćenja Gosta
        Registracija[Registracija]
        PrikazNajboljeOcenjenih[Prikaz najbolje ocenjenih]
        PrikazFilmovaUBioskopu[Prikaz filmova u bioskopu]
        PrikazRepertoara[Prikaz repertoara]
        PrikazFilma[Prikaz filma]
        PredlogStaGledati[Predlog šta gledati]
    end
```

```mermaid
flowchart TD
    User[Registrovani Korisnik] --> Prijava
    User --> Odjava
    User --> PrikazNajboljeOcenjenih
    User --> PrikazFilmovaUBioskopu
    User --> PrikazRepertoara
    User --> PrikazFilma
    User --> PredlogStaGledati
    User --> RezervacijaKarte
    User --> PredlogOProsirenjuRepertoara
    User --> DodavanjeWatchList
    User --> OcenjivanjeFilma
    User --> PrikazProfila
    
    subgraph Slučajevi korišćenja registrovanog korisnika 
        PrikazNajboljeOcenjenih[Prikaz najbolje ocenjenih]
        PrikazFilmovaUBioskopu[Prikaz filmova u bioskopu]
        PrikazRepertoara[Prikaz repertoara]
        PrikazFilma[Prikaz filma]
        PredlogStaGledati[Predlog šta gledati]
        
        RezervacijaKarte[Rezervacija karte]
        PredlogOProsirenjuRepertoara[Predlog o proširenju repertoara]
        DodavanjeWatchList[Dodavanje filma u Watchlist]
        OcenjivanjeFilma[Ocenjivanje filma]
        PrikazProfila[Prikaz Profila]
                
        Prijava[Prijava]
        Odjava[Odjava]
    end
```

```mermaid
flowchart TD
    Admin[Admininstrator] --> Prijava
    Admin --> Odjava
    Admin --> DodavanjeFilma
    Admin --> DodavanjeProjekcije
    Admin --> PromenaTerminaProjekcije
    Admin --> UpravljanjeNalozima
    Admin --> UpravljanjePredlozima
    
    subgraph Slučajevi korišćenja administratora 
        Prijava[Prijava]
        Odjava[Odjava]
        
        DodavanjeFilma[Dodavanje filma]
        DodavanjeProjekcije[Dodavanje projekcije]
        PromenaTerminaProjekcije[Promena termina projekcije]
        UpravljanjeNalozima[Upravljanje korisničkim nalozima]
        UpravljanjePredlozima[Upravljanje korisničkim predlozima]
    end
```