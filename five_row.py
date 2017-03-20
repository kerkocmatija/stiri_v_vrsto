######################################################################
## Igra

IGRALEC_R = 1 # Igralec, ki ima rdeče krogce
IGRALEC_Y = 2 # Igralec, ki ima rumene krogce
PRAZNO = 0 # Prazno polje
NEODLOCENO = "neodločeno" # Igra se je končala z neodločenim izzidom
NI_KONEC = "ni konec" # Igre še ni konec
NEVELJAVNO = 99 # Ta stolpec ni veljaven

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
    # Tabela vseh možnih zmagovalnih kombinacij 4 v vrsto
    stirke_R = [
        [(0,1), (1,2), (2,3), (3,4)],
        [(0,3), (1,2), (2,1), (3,0)],
        [(3,1), (4,2), (5,3), (6,4)],
        [(3,5), (4,4), (5,3), (6,2)]
    ]
    stirke_Y = [
        [(0,2), (1,3), (2,4), (3,5)],
        [(0,4), (1,3), (2,2), (3,1)],
        [(3,0), (4,1), (5,2), (6,3)],
        [(3,4), (4,3), (5,2), (6,1)]
    ]
    for i in range(6):
        if i%2 == 0:
            stirke_R.append([(0,i), (1,i), (2,i), (3,i)])
            stirke_Y.append([(3,i), (4,i), (5,i), (6,i)])
        else:
            stirke_Y.append([(0,i), (1,i), (2,i), (3,i)])
            stirke_R.append([(3,i), (4,i), (5,i), (6,i)])
    # Dodajmo še robne diagonalne rešitve
    stirke_R 
    petke = []
    for i in range(7):
        for j in range(2): # Navpične
            petke.append([(i,j), (i,j+1), (i,j+2), (i,j+3), (i,j+4)])
        if i < 3:
            for j in range(6):
                petke.append([(i,j), (i+1,j), (i+2,j), (i+3,j), (i+4,j)])
                if j < 2:
                    petke.append([(i,j), (i+1,j+1), (i+2,j+2), (i+3,j+3), (i+4,j+4)])
                if j > 2: # Diagonalne desno dol
                    petke.append([(i,j), (i+1,j-1), (i+2,j-2), (i+3,j-3), (i+4,j-4)])
    
    def __init__(self):
        # Ustvarimo seznam trenutne pozicije
        self.polozaj = [[PRAZNO]*6 for i in range(7)]

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
        # TODO
        pass

    def povleci_potezo(self, p):
        '''Povleci potezo p, če je veljavna, sicer ne naredi nič.
            Veljavna igra -> vrne stanje_igre() po potezi, sicer None.'''
        (i,j) = p # Igrana poteza
        poteze = self.veljavne_poteze() # Seznam veljavnih potez

        if (poteze[i] == NEVELJAVNO) or (self.na_potezi == None):
            # Poteza ni veljavna
            return None
        else:
            if len(self.zgodovina) > self.stevec:
                self.zgodovina = self.zgodovina[:self.stevec]
            self.shrani_polozaj()
            self.polozaj[i][poteze[i]] = self.na_potezi
            (zmagovalec, stirka) = self.stanje_igre()
            if zmagovalec == NI_KONEC:
                # Igra se nadaljuje, na potezi je nasprotnik
                self.na_potezi = nasprotnik(self.na_potezi)
            else:
                # Igra se je zaključila
                self.na_potezi = None
            self.zadnja = ([self.polozaj[i][:] for i in range(7)],
                           self.na_potezi)
            # Na koncu return dodamo False, zaradi kompatibilnosti s popout.py
            return (zmagovalec, stirka, (i,poteze[i]), False)

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
        # Preverimo najprej, če obstaja kakšna zmagovalna štirka
        for s in Igra.stirke_R:
            ((i1,j1),(i2,j2),(i3,j3),(i4,j4)) = s
            barva = self.polozaj[i1][j1]
            if (barva == IGRALEC_R) and (barva == self.polozaj[i2][j2] == self.polozaj[i3][j3] == self.polozaj[i4][j4]):
                # s je naša zmagovalna štirka
                return (barva, s)
        for s in Igra.stirke_Y:
            ((i1,j1),(i2,j2),(i3,j3),(i4,j4)) = s
            barva = self.polozaj[i1][j1]
            if (barva == IGRALEC_Y) and (barva == self.polozaj[i2][j2] == self.polozaj[i3][j3] == self.polozaj[i4][j4]):
                # s je naša zmagovalna štirka
                return (barva, s)
        for s in Igra.petke:
            ((i1,j1),(i2,j2),(i3,j3),(i4,j4), (i5,j5)) = s
            barva = self.polozaj[i1][j1]
            if (barva != PRAZNO) and (barva == self.polozaj[i2][j2] == self.polozaj[i3][j3] == self.polozaj[i4][j4] == self.polozaj[i5][j5]):
                # s je naša zmagovalna petka
                return (barva, s)
        # Če zmagovalca ni, moramo preveriti, če je igre konec
        poteze = self.veljavne_poteze()
        for i in poteze:
            if i < NEVELJAVNO:
                # Obstajajo še vsaj 1 veljavna poteza
                return (NI_KONEC, None)
        # Če pridemo do sem, so vsa polja zasedena in ni več veljavnih potez
        # Pravtako tudi zmagovalca ni, torej je rezultat neodločen
        return (NEODLOCENO, None)

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

    def veljavne_poteze(self):
        '''Vrne seznam veljavnih potez.'''
        poteze = []
        for a in self.polozaj:
            veljaven_stolpec = False
            for (j, b) in enumerate(a):
                if b == PRAZNO:
                    # Dobili smo veljavno potezo
                    # Veljavno je le prvo prazno polje v stolpu
                    poteze.append(j)
                    veljaven_stolpec = True
                    break
            if not veljaven_stolpec:
                # V stolpcu ni bilo prostih mest
                poteze.append(NEVELJAVNO)
        return poteze
