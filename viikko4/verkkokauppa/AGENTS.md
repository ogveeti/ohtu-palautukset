# Projektin ohjeet

Tämä on Pythonilla toteutettu verkkokaupan harjoitusprojekti. Sovelluskoodi on
hakemistossa `src` ja testit hakemistossa `src/tests`. Python-versio on vähintään
3.14, ja testit suoritetaan pytestillä.

## Työskentelytapa

- Vastaa käyttäjälle suomeksi.
- Etene käyttäjän antaman tehtävän rajauksessa. Kun käyttäjä pyytää yhtä uutta
  testiä, lisää vain kyseinen testi.
- Säilytä aiemmat testit. Älä refaktoroi testejä tai sovelluskoodia pelkän uuden
  testin lisäämisen yhteydessä.
- Pidä ratkaisut yksinkertaisina ja nykyisen koodin mukaisina. Älä lisää
  riippuvuuksia tai uusia abstraktioita ilman tehtävästä johtuvaa tarvetta.

## Koodityyli

- Käytä neljän välilyönnin sisennystä ja merkkijonoissa kaksinkertaisia lainausmerkkejä.
- Käytä suomenkielisiä, kuvaavia nimiä nykyisen koodin tapaan.
- Nimeä metodit ja muuttujat `snake_case`-tyylillä ja luokat `PascalCase`-tyylillä.
- Nimeä testit `test_`-alkuisiksi niin, että nimi kuvaa tilanteen ja odotetun
  toiminnan.
- Kirjoita tarpeelliset kommentit suomeksi.

## Kaupan testit

- Lisää Kaupan testit tiedoston `src/tests/kauppa_test.py` luokkaan `TestKauppa`,
  joka perii luokan `unittest.TestCase`.
- Käytä `unittest.mock`-kirjaston `Mock`-olioita pankille, viitegeneraattorille ja
  varastolle. Käytä tuotteina oikeita `Tuote`-olioita.
- Luo yhteiset mockit, varaston oletussaldot ja kauppa `setUp`-metodissa, jotta
  jokainen testi saa omat uudet oliot. Määritä testikohtaiset poikkeukset,
  kuten loppuneen tuotteen saldo, kyseisessä testissä.
- Aseta viitegeneraattorin palautusarvo `uusi.return_value`-määrityksellä.
  Nykyisissä testeissä käytetään arvoa `42`.
- Toteuta varaston `saldo`- ja `hae_tuote`-vastaukset `setUp`-metodin sisäisillä funktioilla
  ja kytke ne mockiin `side_effect`-määrityksillä. Anna loppuneen tuotteen saldoksi
  `0` ja saatavilla olevalle tuotteelle riittävä positiivinen saldo.
- Jäsennä testi järjestykseen: riippuvuuksien alustus, kaupan luonti, asiointi ja
  lopuksi tuloksen tarkistus.
- Aloita asiointi kutsulla `aloita_asiointi()`, lisää pyydetyt tuotteet
  `lisaa_koriin`-kutsuilla ja suorita maksu `tilimaksu`-kutsulla.
- Kun tarkistetaan maksun tietoja, käytä `assert_called_with`-metodia.
  `tilisiirto`-kutsun argumenttijärjestys on asiakas, viite, asiakkaan tili,
  kaupan tili ja summa. Käytä viitteelle `ANY`, ellei tehtävässä pyydetä
  tarkistamaan myös viitettä.
- Käytä odotettua summaa suoraan lukuna. Nykyisten testien asiakas on `"pekka"`,
  asiakkaan tili `"12345"` ja kaupan tili `"33333-44455"`.

## Tarkistaminen

Suorita testit projektin juuresta muutosten jälkeen:

```bash
.venv/bin/python -m pytest
```

Kerro lopuksi lyhyesti, mitä lisäsit ja menivätkö testit läpi. Jos testejä ei
voitu suorittaa, kerro siitä selvästi.
