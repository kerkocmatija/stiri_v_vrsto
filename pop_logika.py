###################
## LOGIKA POPOUT ##
###################

IGRALEC_R = 1 # Igralec, ki ima rdeče krogce
IGRALEC_Y = 2 # Igralec, ki ima rumene krogce
PRAZNO = 0 # Prazno polje
NEODLOCENO = "neodločeno" # Igra se je končala z neodločenim izzidom
NI_KONEC = "ni konec" # Igre še ni konec
NEVELJAVNO = 99 # Ta stolpec ni veljaven
from igra import *

class pop_logika(Igra):

    def veljavne_poteze(self):
        '''Vrne seznam veljavnih potez.'''
        poteze = []
        barva = self.na_potezi
        for (i,a) in enumerate(self.polozaj):
            if a[-1] == 0:
                # V stolpcu je še vsaj 1 prosto mesto
                poteze.append(i+1)
            if barva and a[0] == barva:
                # Spodnji element stolpca je od igralca, ki je na potezi
                poteze.append(-i-1)
        return poteze
