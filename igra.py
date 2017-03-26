#################
## LOGIKA IGRE ##
#################

from norm_logika import *
from pop_logika import *
from five_logika import *

def nasprotnik(igralec):
    """Vrni nasprotnika od igralca."""
    if igralec == IGRALEC_R:
        return IGRALEC_Y
    elif igralec == IGRALEC_Y:
        return IGRALEC_R
    else:
        # Do sem ne smemo priti, če pridemo, je napaka v programu.
        # V ta namen ima Python ukaz assert, s katerim lahko preverimo,
        # ali dani pogoj velja. V našem primeru, ko vemo, da do sem
        # sploh ne bi smeli priti, napišemo za pogoj False, tako da
        # bo program crknil, če bo prišel do assert.
        # To je zelo uporabno za odpravljanje napak.
        # Assert uporabimo takrat, ko bi program lahko deloval naprej kljub
        # napaki (če bo itak takoj crknil, potem assert ni potreben).
        assert False, "neveljaven nasprotnik"

class Igra():
    def __init__(self, tip=None):
        # Ustvarimo seznam trenutne pozicije
        self.polozaj = [[PRAZNO]*6 for i in range(7)]

        # Nastavimo tip igre
        if tip == 'popout':
            self.tip = pop_logika(self)
        elif tip == '5inarow':
            self.tip = five_logika(self)
        else:
            self.tip = norm_logika(self)

        # Na potezi je rdeči
        self.na_potezi = IGRALEC_R

        # Shranjujmo si zgodovino, da lahko uporabimo 'undo'
        self.zgodovina = []

        # Števec, ki nam pove, katero potezo si ogledujemo
        # Z njim lahko gremo v 'preteklost'
        self.stevec = 0

        # To je začasna rešitev, dokler ne najdem boljše
        # Je zadnje stanje, če želiš `Redo`-jati do konca
        self.zadnja = ([[PRAZNO]*6 for i in range(7)], self.na_potezi)

    def kopija(self):
        '''Vrni kopijo te igre, brez zgodovine.'''
        # Potrebujemo, da se ne rišejo poteze, ko računalnik razmišlja
        k = Igra()
        k.polozaj = [self.polozaj[i][:] for i in range(7)]
        k.na_potezi = self.na_potezi
        k.tip = self.tip
        return k

    def povleci_potezo(self, p):
        '''Povleci potezo p, če je veljavna, sicer ne naredi nič.
            Veljavna igra -> vrne stanje_igre() po potezi, sicer None.'''
        (i,j) = p # Igrana poteza
        (poteze, poteze_popout) = self.tip.veljavne_poteze() # Seznam veljavnih potez
        je_popout = False # Gre za popout potezo?
        
        if poteze_popout and j == 5 and poteze_popout[i]:
            # Imamo popout potezo
            if len(self.zgodovina) > self.stevec:
                self.zgodovina = self.zgodovina[:self.stevec]
            self.shrani_polozaj()
            # Odstranimo spodnji žeton
            del self.polozaj[i][0]
            self.polozaj[i].append(0)
            je_popout = True
        elif poteze[i] == NEVELJAVNO or self.na_potezi is None:
            # Poteza ni veljavna
            return None
        else:
            if len(self.zgodovina) > self.stevec:
                self.zgodovina = self.zgodovina[:self.stevec]
            self.shrani_polozaj()
            self.polozaj[i][poteze[i]] = self.na_potezi
        (zmagovalec, stirka) = self.tip.stanje_igre()
        # Preverimo, če je igre konec
        if zmagovalec == NI_KONEC:
            # Igra se nadaljuje, na potezi je nasprotnik
            self.na_potezi = nasprotnik(self.na_potezi)
        else:
            # Igra se je zaključila
            self.na_potezi = None
        self.zadnja = ([self.polozaj[i][:] for i in range(7)],
                       self.na_potezi)
        return (zmagovalec, stirka, (i,poteze[i]), je_popout if poteze_popout else False)

    def razveljavi(self):
        '''Razveljavi potezo in se vrne v prejšnje stanje.'''
        if self.stevec > 0:
            (self.polozaj, self.na_potezi) = self.zgodovina[self.stevec-1]
            self.stevec -= 1
            return (self.polozaj, self.na_potezi)
        else:
            return None

    def shrani_polozaj(self):
        '''Shrani trenutni položaj igre, da se lahko vanj vrnemo
            s klicem metode 'razveljavi'.'''
        p = [self.polozaj[i][:] for i in range(7)]
        self.zgodovina.append((p, self.na_potezi))
        self.stevec += 1

    def stanje_igre(self):
        '''Vrne nam trenutno stanje igre. Možnosti so:
            - (IGRALEC_R, stirka), če je igre konec in je zmagal IGRALEC_R z dano zmagovalno štirko,
            - (IGRALEC_Y, stirka), če je igre konec in je zmagal IGRALEC_Y z dano zmagovalno štirko,
            - (NEODLOCENO, None), če je igre konec in je neodločeno,
            - (NI_KONEC, None), če je igra še vedno v teku.'''
        return self.tip.stanje_igre()

    def uveljavi(self):
        '''Uveljavi zadnjo razveljavljeno potezo in se vrne v njeno stanje.'''
        if self.stevec < len(self.zgodovina)-1: # -1 začasno, dokler ne dodam zadnje poteze
            self.stevec += 1
            (self.polozaj, self.na_potezi) = self.zgodovina[self.stevec]
            return (self.polozaj, self.na_potezi)
        elif self.stevec == len(self.zgodovina)-1:
            self.stevec += 1
            (self.polozaj, self.na_potezi) = self.zadnja
            return (self.polozaj, self.na_potezi)
        else:
            return None
