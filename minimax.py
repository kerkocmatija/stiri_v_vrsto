import logging

from igra import IGRALEC_R, IGRALEC_Y, PRAZNO, NEODLOCENO, NI_KONEC, nasprotnik, NEVELJAVNO

#######################
## ALGORITEM MINIMAX ##
#######################

class Minimax:
    # Algoritem minimax

    def __init__(self, globina):
        self.globina = globina # Kako globoko iščemo?
        self.prekinitev = False # Želimo algoritem prekiniti?
        self.igra = None # Objekt, ki predstavlja igro
        self.jaz = None # Katerega igralca igramo?
        self.poteza = None # Sem vpišemo potezo, ko jo najdemo

    def prekini(self):
        '''Metoda, ki jo pokliče GUI, če je treba nehati razmišljati, ker
            je uporabnik zapr okno ali izbral novo igro.'''
        self.prekinitev = True

    def izracunaj_potezo(self, igra):
        '''Izračunaj potezo za trenutno stanje dane igre.'''
        # To metodo pokličemo iz vzporednega vlakna
        self.igra = igra
        self.prekinitev = False # Glavno vlakno bo to nastavilo na True, če bomo morali prekiniti
        self.poteza = None # Sem napišemo potezo, ko jo najdemo

        # Poženemo minimax
        (poteza, vrednost) = self.minimax(self.globina, True)
        self.jaz = None
        self.igra = None
        if not self.prekinitev:
            # Nismo bili prekinjeni, torej potezo izvedemo
            self.poteza = poteza

    # Vrednosti igre
    ZMAGA = 10**5
    NESKONCNO = ZMAGA + 1 # Več kot zmaga

    def vrednost_pozicije(self):
        '''Ocena vrednosti polozaja.'''
        # TODO
        return 10**3

    def minimax(self, globina, maksimiziramo):
        '''Glavna metoda minimax.'''
        if self.prekinitev:
            # Sporočili so nam, da moramo prekiniti
            return (None, 0)

        (zmagovalec, stirka) = self.igra.stanje_igre()
        if zmagovalec in (IGRALEC_R, IGRALEC_Y, NEODLOCENO):
            # Igre je konec, vrnemo njeno vrednost
            if zmagovalec == self.jaz:
                return (None, Minimax.ZMAGA)
            elif zmagovalec == nasprotnik(self.jaz):
                return (None, -Minimax.ZMAGA)
            else:
                return (None, 0)
        elif zmagovalec == NI_KONEC:
            # Igre ni konec
            if globina == 0:
                return (None, self.vrednost_pozicije())
            else:
                # Naredimo en korak minimax metode
                if maksimiziramo:
                    # Maksimiziramo
                    najboljsa_poteza = None
                    vrednost_najboljse = -Minimax.NESKONCNO
                    for (i,p) in enumerate(self.igra.tip.veljavne_poteze()[0]):
                        if p == NEVELJAVNO:
                            continue
                        self.igra.povleci_potezo((i,p))
                        vrednost = self.minimax(globina-1, not maksimiziramo)[1]
                        self.igra.razveljavi()
                        if vrednost > vrednost_najboljse:
                            najboljsa_poteza = (i,p)
                            vrednost_najboljse = vrednost
                else:
                    # Minimiziramo
                    najboljsa_poteza = None
                    vrednost_najboljse = Minimax.NESKONCNO
                    for (i,p) in enumerate(self.igra.tip.veljavne_poteze()[0]):
                        if p == NEVELJAVNO:
                            continue
                        self.igra.povleci_potezo((i,p))
                        vrednost = self.minimax(globina-1, not maksimiziramo)[1]
                        self.igra.razveljavi()
                        if vrednost < vrednost_najboljse:
                            najboljsa_poteza = (i,p)
                            vrednost_najboljse = vrednost
                assert (najboljsa_poteza is not None), 'minimax: izračunana poteza je None'
                return (najboljsa_poteza, vrednost_najboljse)
        else:
            assert False, 'minimax: nedefinirano stanje igre'
