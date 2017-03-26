##########################
## LOGIKA ŠTIRI-V-VRSTO ##
##########################

IGRALEC_R = 1 # Igralec, ki ima rdeče krogce
IGRALEC_Y = 2 # Igralec, ki ima rumene krogce
PRAZNO = 0 # Prazno polje
NEODLOCENO = "neodločeno" # Igra se je končala z neodločenim izzidom
NI_KONEC = "ni konec" # Igre še ni konec
NEVELJAVNO = 99 # Ta stolpec ni veljaven

class norm_logika():
    # Tabela vseh možnih zmagovalnih kombinacij 4 v vrsto
    stirke = []
    for i in range(7):
        for j in range(3): # Navpične
            stirke.append([(i,j), (i,j+1), (i,j+2), (i,j+3)])
        if i < 4: # 4 = 7 - 3, 3 mesta še naprej za 4ko
            for j in range(6): # 6 vrstic
                stirke.append([(i,j), (i+1,j), (i+2, j), (i+3, j)]) # Vodoravne
                if j < 3: # Diagonalne desno gor
                    stirke.append([(i,j), (i+1,j+1), (i+2,j+2), (i+3,j+3)])
                if j > 2: # Diagonalne desno dol
                    stirke.append([(i,j), (i+1,j-1), (i+2,j-2), (i+3,j-3)])

    
    def __init__(self, v_igri):
        self.v_igri = v_igri

    def stanje_igre(self):
        '''Vrne nam trenutno stanje igre. Možnosti so:
            - (IGRALEC_R, stirka), če je igre konec in je zmagal IGRALEC_R z dano zmagovalno štirko,
            - (IGRALEC_Y, stirka), če je igre konec in je zmagal IGRALEC_Y z dano zmagovalno štirko,
            - (NEODLOCENO, None), če je igre konec in je neodločeno,
            - (NI_KONEC, None), če je igra še vedno v teku.'''
        # Najprej preverimo, če obstaja kakšna zmagovalna štirka
        for s in norm_logika.stirke:
            ((i1,j1),(i2,j2),(i3,j3),(i4,j4)) = s
            barva = self.v_igri.polozaj[i1][j1]
            if (barva != PRAZNO) and (barva == self.v_igri.polozaj[i2][j2] == self.v_igri.polozaj[i3][j3] == self.v_igri.polozaj[i4][j4]):
                # s je naša zmagovalna štirka
                return (barva, s)
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
