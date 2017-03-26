########################
## LOGIKA PET-V-VRSTO ##
########################

IGRALEC_R = 1 # Igralec, ki ima rdeče krogce
IGRALEC_Y = 2 # Igralec, ki ima rumene krogce
PRAZNO = 0 # Prazno polje
NEODLOCENO = "neodločeno" # Igra se je končala z neodločenim izzidom
NI_KONEC = "ni konec" # Igre še ni konec
NEVELJAVNO = 99 # Ta stolpec ni veljaven

class five_logika():
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
    # Dodajmo še robne diagonalne rešitve
    for i in range(6):
        if i%2 == 0:
            stirke_R.append([(0,i), (1,i), (2,i), (3,i)])
            stirke_Y.append([(3,i), (4,i), (5,i), (6,i)])
        else:
            stirke_Y.append([(0,i), (1,i), (2,i), (3,i)])
            stirke_R.append([(3,i), (4,i), (5,i), (6,i)])
    petke = []
    for i in range(7):
        for j in range(2): # Navpične
            petke.append([(i,j), (i,j+1), (i,j+2), (i,j+3), (i,j+4)])
        if i < 3:
            for j in range(6):
                petke.append([(i,j), (i+1,j), (i+2,j), (i+3,j), (i+4,j)])
                if j < 2: # Diagonale desno gor
                    petke.append([(i,j), (i+1,j+1), (i+2,j+2), (i+3,j+3), (i+4,j+4)])
                if j > 3: # Diagonalne desno dol
                    petke.append([(i,j), (i+1,j-1), (i+2,j-2), (i+3,j-3), (i+4,j-4)])
    
    def __init__(self, v_igri):
        self.v_igri = v_igri

    def stanje_igre(self):
        '''Vrne nam trenutno stanje igre. Možnosti so:
            - (IGRALEC_R, stirka), če je igre konec in je zmagal IGRALEC_R z dano zmagovalno štirko,
            - (IGRALEC_Y, stirka), če je igre konec in je zmagal IGRALEC_Y z dano zmagovalno štirko,
            - (NEODLOCENO, None), če je igre konec in je neodločeno,
            - (NI_KONEC, None), če je igra še vedno v teku.'''
        # Najprej preverimo, če obstaja kakšna zmagovalna štirka
        for s in five_logika.stirke_R:
            ((i1,j1),(i2,j2),(i3,j3),(i4,j4)) = s
            barva = self.v_igri.polozaj[i1][j1]
            if (barva == IGRALEC_R) and (barva == self.v_igri.polozaj[i2][j2] == self.v_igri.polozaj[i3][j3] == self.v_igri.polozaj[i4][j4]):
                # s je naša zmagovalna štirka
                return (barva, s)
        for s in five_logika.stirke_Y:
            ((i1,j1),(i2,j2),(i3,j3),(i4,j4)) = s
            barva = self.v_igri.polozaj[i1][j1]
            if (barva == IGRALEC_Y) and (barva == self.v_igri.polozaj[i2][j2] == self.v_igri.polozaj[i3][j3] == self.v_igri.polozaj[i4][j4]):
                # s je naša zmagovalna štirka
                return (barva, s)
        # Preverimo še sedaj, če obstaja zmagovalna petka
        for p in five_logika.petke:
            ((i1,j1),(i2,j2),(i3,j3),(i4,j4), (i5,j5)) = p
            barva = self.v_igri.polozaj[i1][j1]
            if (barva != PRAZNO) and (barva == self.v_igri.polozaj[i2][j2] == self.v_igri.polozaj[i3][j3] == self.v_igri.polozaj[i4][j4] == self.v_igri.polozaj[i5][j5]):
                # s je naša zmagovalna petka
                return (barva, p)
        # Če zmagovalca ni, moramo preveriti, če je igre konec
        (poteze, popout) = self.veljavne_poteze()
        for i in poteze:
            if i < NEVELJAVNO:
                # Obstajajo še vsaj 1 veljavna poteza
                return (NI_KONEC, None)
        # Če pridemo do sem, so vsa polja zasedena in ni več veljavnih potez
        # Pravtako tudi zmagovalca ni, torej je rezultat neodločen
        return (NEODLOCENO, None)

    def veljavne_poteze(self):
        '''Vrne seznam veljavnih potez.'''
        poteze = []
        for a in self.v_igri.polozaj:
            veljaven_stolpec = False
            for (j, b) in enumerate(a):
                if b == PRAZNO:
                    # Našli smo veljavno potezo
                    # Veljavno je le prvo prazno polje v stolpcu
                    poteze.append(j)
                    veljaven_stolpec = True
                    break
            if not veljaven_stolpec:
                # V stolpcu ni bilo prostih mest
                poteze.append(NEVELJAVNO)
        return (poteze, False)
