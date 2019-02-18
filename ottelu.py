class Osallistuja:
    def __init__(self, lista):
        self.__nimi = lista[1]
        self.__sarja = lista[2]
        self.__tulokset = {}
        self.__kokonaispisteet = 0

    # Tässä lisätään osallistujalle tulos lajista, johon hän on osallistunut.
    def lisää_tulos(self, laji, tulos):
        if laji not in self.__tulokset:
            self.__tulokset[laji] = tulos
            # Samalla voidaan laskea kokonaispistemäärää.
            self.__kokonaispisteet += tulos
            return True
        # Tänne päädytään, jossei osallistuja ole osallistunut kyseiseen
        # lajiin. Dictissä tulokset ei siis ole tätä lajia osoittajana.
        else:
            return False

    # Peruspalautukset:
    def kerro_nimi(self):
        return self.__nimi

    def kerro_sarja(self):
        return self.__sarja

    # Tässä täytyy ottaa taas huomioon, onko osallistuja ollut mukana tässä
    # lajissa.
    def kerro_tulos(self, laji):
        if laji in self.__tulokset:
            return self.__tulokset[laji]
        else:
            return False

    def kerro_kokonaispisteet(self):
        return self.__kokonaispisteet

    def kerro_lajimäärä(self):
        return len(self.__tulokset)


class Sarja:  # Luokka sarjoille sarjatilastojen käsittelyä varten.
    # Sarjaa luodessa ei tarvita mitään argumentteja.
    def __init__(self):
        self.__osallistujat = 0
        self.__pisteet = []
        self.__lajimäärä = []

    # Sarjan tärkein toiminto. Lisätään sarjaan kuuluva osallistuja ja hänen
    # kokonaispistemäärä sekä lajimäärä.
    def lisää_osallistuja(self, pisteet, lajit):
        # Sarjoissa osallistujia ei tarvitse käsitellä kuin lukumäärinä.
        self.__osallistujat += 1
        self.__pisteet.append(pisteet)
        self.__lajimäärä.append(lajit)
        # Osallistujamäärä löytyy myös selvittämällä pistelistan tai
        # lajimäärälistan pituuden, mutta omalla muuttujalla käsittely on
        # selkeämpää.

    # Peruspalautukset:
    def kerro_osallistujamäärä(self):
        return self.__osallistujat

    def kerro_paras_pistemäärä(self):
        paras = 0
        # Käydään läpi kaikki sarjan pistemäärät ja etsitään niistä suurin.
        for i in self.__pisteet:
            if i > paras:
                paras = i
        return paras

    def kerro_pisteiden_ka(self):
        summa = 0
        # Lasketaan kaikki pisteet yhteen...
        for i in self.__pisteet:
            summa += i
        # ...ja jaetaan se osallistujamäärällä.
        keskiarvo = summa / self.__osallistujat
        # Palautuksessa tarvitaan arvoa vain yhden desimaalin tarkkuudella.
        return "{:.1f}".format(keskiarvo)

    # Sama periaate kuin edellisessä.
    def kerro_lajeja_ka(self):
        lajimäärä = 0
        for i in range(len(self.__lajimäärä)):
            lajimäärä += self.__lajimäärä[i]
        keskiarvo = lajimäärä / self.__osallistujat
        return "{:.1f}".format(keskiarvo)


def lue_osallistujat():
    # Tallennetaan osallistujat dictiin helpon käsittelyn vuoksi.
    osallistujat = {}
    try:
        osallistujatiedosto = open("osallistujat.txt", "r")
        for rivi in osallistujatiedosto:
            rivi = rivi.rstrip()
            # Erotellaan tiedot toisistaan omaan listaansa.
            lista = rivi.split(";")
            # Tiedetään tunnisteen paikka listassa.
            tunniste = lista[0]
            # Tarkistetaan onko kyseinen tunniste jo käsitelty. Dictissä on
            # osoittajana tunniste ja sen alla sitä vastaava Osallistuja-olio.
            if tunniste not in osallistujat:
                osallistujat[tunniste] = Osallistuja(lista)
            # Jos tunniste on jo käsitelty, ilmoitetaan virheestä ja
            # lopetetaan ohjelma.
            else:
                print("Virheellinen osallistujatiedosto: tunnus",
                      tunniste, "toistuu.")
                return False
        osallistujatiedosto.close()
        return osallistujat
    # Muut virhetarkastelut:
    except IOError:
        print("Virhe osallistujatiedoston lukemisessa.")
        return False
    except IndexError:
        print("Virheellinen osallistujatiedosto: rivi '", rivi,
              "' ei ole muodossa tunnus;nimi;sarja.", sep="")
        return False


def lue_ottelu():  # 3. vaiheen yksinkertainen lisäfunktio :)
    try:
        ottelu = open("ottelu.txt", "r")
        lajitiedostot = []
        # Tallennetaan jokainen rivi listaan stripattuna.
        for rivi in ottelu:
            rivi = rivi.rstrip()
            lajitiedostot.append(rivi)
        ottelu.close()
    except IOError:
        print("Virhe ottelutiedoston lukemisessa.")
        return False
    return lajitiedostot


def lue_lajitiedosto(tiedosto, osallistujat):
    try:
        lajitiedosto = open(tiedosto, "r")
        # Stripataan tämä vielä erikseen täällä, niin ei tarvitse kuljetella
        # enempää muuttujia mainista funktioon. En tiedä kumpi on tehokkuuden
        # tai siisteyden kannalta parempi.
        laji, pääte = tiedosto.split(".")
        for rivi in lajitiedosto:
            tunnus, tulos = rivi.rstrip().split(";")
            # Muutetaan stringit floateiksi myöhempää käsittelyä varten.
            tulos = float(tulos)
            # Yritetään lisätä tulos osallistujalle. Mikäli palautuksena on
            # False, ilmoitetaan käyttäjälle virheestä ja lopetetaan ohjelma.
            # Itse virhetarkastelu tapahtuu luokassa.
            if not osallistujat[tunnus].lisää_tulos(laji, tulos):
                print("Virheellinen lajitiedosto ", tiedosto, ": tunnus ",
                      tunnus, " toistuu.", sep="")
                return False
        # Muistetaan sulkea tiedosto!
        lajitiedosto.close()
        return True
    # Virhetarkastelut:
    except IOError:
        print("Virhe lajitiedoston", tiedosto, "lukemisessa.")
        return False
    except ValueError:
        print("Virheellinen lajitiedosto ", tiedosto, ": rivi '",
              rivi.rstrip(), "' ei ole muodossa tunnus;pisteet.", sep="")
        return False
    except KeyError:
        print("Virheellinen lajitiedosto ", tiedosto, ": tunnus ", tunnus,
              " puuttuu osallistujatiedostosta.", sep="")
        return False


def luo_sarjat(osallistujat):  # Luodaan sarjaoliot.
    sarjat = []  # Luodaan lista kaikista sarjoista osallistujien avulla.
    for tunnus in osallistujat:
        sarja = osallistujat[tunnus].kerro_sarja()
        if sarja not in sarjat:
            sarjat.append(sarja)
    sarjaoliot = {}  # Tallennetaan sarjaoliot yhteen sarjatunnuksen kanssa.
    # Käydään juuri luotu lista läpi.
    for sarja in sarjat:
        sarjaoliot[sarja] = Sarja()  # Luodaan olio.
        # Käydään läpi kaikki sarjaan kuuluvat osallistujat ja lisätään niiden
        # pisteet ja lajimäärät olioon.
        for tunnus in osallistujat:
            osallistujan_sarja = osallistujat[tunnus].kerro_sarja()
            if osallistujan_sarja == sarja:
                pisteet = osallistujat[tunnus].kerro_kokonaispisteet()
                lajit = osallistujat[tunnus].kerro_lajimäärä()
                sarjaoliot[sarja].lisää_osallistuja(pisteet, lajit)
    return sarjaoliot


def kirjoita_tulostiedosto(osallistujat, lajit):
    try:
        tulostiedosto = open("tulokset.txt", "w")
        perustiedot = "tunnus;nimi;sarja;"
        # Kerätään yhteen muuttujaan kaikki lajinimet kirjoittamista varten.
        lajisarakeotsikot = ""
        for laji in lajit:
            lajisarakeotsikot += laji + ";"
        loput = "kokonaispisteet;lajeja"
        # Kirjoitetaan ensimmäinen rivi.
        tulostiedosto.write(perustiedot + lajisarakeotsikot + loput + "\n")

        # Osallistujat aakkosjärjestykseen ja
        # käydään jokainen kerrallaan läpi.
        for tunnus in sorted(osallistujat):
            # Lisätään jo valmiiksi jokaisen str-muuttujan perään ";",
            # jotta tiedostoon kirjoittaminen on yksinkertaisempaa.
            nimi = osallistujat[tunnus].kerro_nimi() + ";"
            sarja = osallistujat[tunnus].kerro_sarja() + ";"
            # Muutetaan floatit stringeiksi.
            kokonaispisteet = \
                str(osallistujat[tunnus].kerro_kokonaispisteet()) + ";"
            lajeja = str(osallistujat[tunnus].kerro_lajimäärä()) + \
                     "/" + str(len(lajit)) + "\n"
            pisteet = ""
            # Haetaan myös pisteet kaikista lajeista.
            for laji in lajit:
                tulos = osallistujat[tunnus].kerro_tulos(laji)
                if tulos:
                    pisteet += str(tulos) + ";"
                # Jos ei osallistunut (eli tulos = False),
                # laitetaan pisteiden paikalle viiva.
                else:
                    pisteet += "-;"
            # Kirjoitetaan kerätyt tiedot tiedostoon.
            tulostiedosto.write(tunnus + ";" + nimi + sarja + pisteet +
                                kokonaispisteet + lajeja)
        tulostiedosto.close()
        # Ilmoitetaan käyttäjälle tilanteesta.
        print("Tulokset kirjoitettu tiedostoon tulokset.txt.")
        return True
    # Virhetarkastelu:
    except IOError or TypeError:
        print("Virhe sarjatilastotiedoston kirjoittamisessa.")
        return False


def kirjoita_sarjatiedosto(sarjat):
    try:
        sarjatiedosto = open("sarjatilastot.txt", "w")
        # Kopipaste otsikkorivi :)
        otsikkorivi = "sarja;osallistujamaara;paras_pistemaara;pisteiden_ka;" \
                      "lajeja_ka\n"
        sarjatiedosto.write(otsikkorivi)
        # Sitten kirjoitetaan kaikille sarjoille oma rivi. (Samalla tyylillä
        # kuin tulostiedostossakin.)
        for sarja in sorted(sarjat):
            # Muunnetaan _kaikki_ stringeiksi.
            osallistujat = str(sarjat[sarja].kerro_osallistujamäärä()) + ";"
            parhaat_pisteet = str(sarjat[sarja].kerro_paras_pistemäärä()) + ";"
            pisteet_ka = str(sarjat[sarja].kerro_pisteiden_ka()) + ";"
            lajit_ka = str(sarjat[sarja].kerro_lajeja_ka()) + "\n"
            sarjatiedosto.write(sarja + ";" + osallistujat + parhaat_pisteet +
                                pisteet_ka + lajit_ka)
        sarjatiedosto.close()
        print("Sarjatilastot kirjoitettu tiedostoon sarjatilastot.txt.")
    except IOError or TypeError:
        print("Virhe sarjatilastotiedoston kirjoittamisessa.")
        return False


def main():
    # Luetaan tiedostosta osallistujat ja tallennetaan niistä tehdyt oliot
    # dictiin, jossa osoittajana on osallistujan tunnus.
    osallistujat = lue_osallistujat()

    # Tarkistetaan joka kerta jatketaanko ohjelman suorittamista.
    if not osallistujat:
        return False

    # luetaan ottelu.txt ja tallennetaan sieltä saadut tiedostot listaan.
    if True:
        lajitiedostot = lue_ottelu()
        # lajitiedostot voi myös saada totuusarvon, mikäli tapahtuu virhe.
        if not lajitiedostot:
            return False

    if True:
        # Tallennetaan lajitiedostoista saadut lajien nimet omaan listaansa
        # myöhempää käyttöä varten.
        lajit = []
        for tiedosto in lajitiedostot:
            laji, pääte = tiedosto.split(".")
            lajit.append(laji)
            # Luetaan vuorossa oleva lajitiedosto.
            if not lue_lajitiedosto(tiedosto, osallistujat):
                return False

    if True:
        # Sarjojen luonti ei tarvitse virhetarkastelua, sillä mahdolliset
        # virheet on tarkasteltu jo aikaisemmissa funktioissa.
        sarjat = luo_sarjat(osallistujat)
        # Sitten kirjoitetaan tulostiedosto.
        if not kirjoita_tulostiedosto(osallistujat, lajit):
            return False

    if True:
        # Ja sarjatiedosto.
        kirjoita_sarjatiedosto(sarjat)


main()

# Loppu. Kiitos :)