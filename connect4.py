import tkinter # Uvozimo tkinter za uporabniški vmesnik

from igra import *
from clovek import *

#########################
## UPORABNIŠKI VMESNIK ##
#########################

class Gui():
    # To so vsi grafični elementi v self.platno, ki 'pripadajo'
    # igralcema, torej krožci, ki so bili igrani
    TAG_FIGURA = 'figura'

    # Oznaka za črte, ki sestavljajo okvir
    TAG_OKVIR = 'okvir'

    # Velikost polja
    VELIKOST_POLJA = 100

    # Razdalja med okvirjem in figuro
    VELIKOST_GAP = 5

    def __init__(self, master):
        self.igralec_r = None # Objekt, ki igra rdeče krogce
        self.igralec_y = None # Objekt, ki igra rumene krogce
        self.igra = None # Objekt, ki predstavlja igro
        
        # Če uporabnik zapre okno, naj se pokliče self.zapri_okno
        master.protocol('WM_DELETE_WINDOW', lambda: self.zapri_okno(master))

        # Glavni menu
        menu = tkinter.Menu(master)
        master.config(menu=menu)

        # Podmenu 'Igra'
        menu_igra = tkinter.Menu(menu)
        menu.add_cascade(label='Igra', menu=menu_igra)
        menu_igra.add_command(label='Nova igra', command=self.zacni_igro)

        # Napis, ki prikazuje stanje igre
        self.napis = tkinter.StringVar(master, value='Dobrodošli v 4 v vrsto!')
        tkinter.Label(master, textvariable=self.napis).grid(row=0, column=0)

        # Igralno območje
        self.platno = tkinter.Canvas(master,
                                     width=8*Gui.VELIKOST_POLJA,
                                     height=7*Gui.VELIKOST_POLJA)
        self.platno.grid(row=1, column=0)

        # Narišemo črte na igralnem polju (ustvarimo igralno površino)
        self.narisi_okvir()

        # Določimo, kaj se zgodi, ko uporabnik pritisne levi klik
        self.platno.bind('<Button-1>', self.platno_klik)

        # Pričnemo igro
        self.zacni_igro()

    def koncaj_igro(self, zmagovalec, stirka):
        '''Nastavi stanje igre na 'konec igre'.'''
        if zmagovalec == IGRALEC_R:
            self.napis.set('Zmagal je RDEČI!')
        elif zmagovalec == IGRALEC_Y:
            self.napis.set('Zmagal je RUMENI!')
        else:
            self.napis.set('Igra je NEODLOČENA!')
        self.obkrozi(stirka)

    def narisi_okvir(self):
        '''Nariše črte (okvir) na igralno povrčino.'''
        self.platno.delete(Gui.TAG_OKVIR)
        d = Gui.VELIKOST_POLJA
        for i in range(8):
            self.platno.create_line(d/2 + i*d, d/2,
                                    d/2 + i*d, 13*d/2,
                                    tag=Gui.TAG_OKVIR)
        for i in range(7):
            self.platno.create_line(d/2, d/2 + i*d,
                                    15*d/2, d/2 + i*d,
                                    tag=Gui.TAG_OKVIR)

    def narisi_R(self, p):
        d = Gui.VELIKOST_POLJA
        x = (p[0] + 1) * d
        y = (6 - p[1]) * d
        gap = Gui.VELIKOST_GAP
        self.platno.create_oval(x - d/2 + gap, y - d/2 + gap,
                                x + d/2 - gap, y + d/2 - gap,
                                fill = 'red',
                                width=0,
                                tag=Gui.TAG_FIGURA)

    def narisi_Y(self, p):
        d = Gui.VELIKOST_POLJA
        x = (p[0] + 1) * d
        y = (6 - p[1]) * d
        gap = Gui.VELIKOST_GAP
        self.platno.create_oval(x - d/2 + gap, y - d/2 + gap,
                                x + d/2 - gap, y + d/2 - gap,
                                fill = 'yellow',
                                width=0,
                                tag=Gui.TAG_FIGURA)

    def obkrozi(self, stirka):
        w = 5
        d = Gui.VELIKOST_POLJA
        (i1,j1) = stirka[0]
        (i2,j2) = stirka[-1]
        if (i1 == i2) or (j1 == j2):
            x1 = d/2 + i1*d
            y1 = 13*d/2 - j1*d
            x2 = d/2 + (i2+1)*d
            y2 = 13*d/2 - (j2+1)*d
            self.platno.create_rectangle(x1, y1, x2, y2,
                                         width=w,
                                         tag=Gui.TAG_FIGURA)
        else: # Diagonalni - popravi jih še (koti in oddaljenost na levi in desni)
            a = (d * 2**0.5) / 4
            x1 = d/2 + i1*d - a
            x2 = d/2 + i1*d + a
            x3 = d/2 + (i2+1)*d - a
            x4 = d/2 + (i2+1)*d + a

            if j1 > j2:
                y1 = 13*d/2 - (j1+1)*d + a
                y2 = 13*d/2 - (j1+1)*d - a
                y3 = 13*d/2 - j2*d + a
                y4 = 13*d/2 - j2*d - a
            else:
                y1 = 13*d/2 - j1*d - a
                y2 = 13*d/2 - j1*d + a
                y3 = 13*d/2 - (j2+1)*d - a
                y4 = 13*d/2 - (j2+1)*d + a

            self.platno.create_line(x1, y1, x3, y3,
                                    width=w,
                                    tag=Gui.TAG_FIGURA)
            self.platno.create_line(x2, y2, x4, y4,
                                    width=w,
                                    tag=Gui.TAG_FIGURA)
            self.platno.create_line(x1, y1, x2, y2,
                                    width=w,
                                    tag=Gui.TAG_FIGURA)
            self.platno.create_line(x3, y3, x4, y4,
                                    width=w,
                                    tag=Gui.TAG_FIGURA)
##        else:
##            a = (d * 2**0.5) / 4
##            x1 = d/2 + i1*d - a
##            x2 = d/2 + i1*d + a
##            x3 = d/2 + (i2+1)*d - a
##            x4 = d/2 + (i2+1)*d + a
##
##            y1 = 13*d/2 - (j1+1)*d + a
##            y2 = 13*d/2 - (j1+1)*d - a
##            y3 = 13*d/2 - j2*d + a
##            y4 = 13*d/2 - j2*d - a
##
##            self.platno.create_line(x1, y1, x3, y3,
##                                    width=w,
##                                    tag=Gui.TAG_FIGURA)
##            self.platno.create_line(x2, y2, x4, y4,
##                                    width=w,
##                                    tag=Gui.TAG_FIGURA)
##            self.platno.create_line(x1, y1, x2, y2,
##                                    width=w,
##                                    tag=Gui.TAG_FIGURA)
##            self.platno.create_line(x3, y3, x4, y4,
##                                    width=w,
##                                    tag=Gui.TAG_FIGURA)

    def platno_klik(self, event):
        (x,y) = (event.x, event.y)
        d = Gui.VELIKOST_POLJA
        if (x < d/2) or (x > 15*d/2) or (y < d/2) or (y > 13*d/2):
            # V tem primeru smo zunaj igralnega območja
            pass
        else:
            # TODO - preveri za robne pogoje
            i = int((x - d/2) // Gui.VELIKOST_POLJA)
            j = int((y - d/2) // Gui.VELIKOST_POLJA) # BRIŠI
            if 1 >= 0: # To bo v neki verziji v logiki probably
                if self.igra.na_potezi == IGRALEC_R:
                    self.igralec_r.klik((i,j))
                elif self.igra.na_potezi == IGRALEC_Y:
                    self.igralec_r.klik((i,j))
                else:
                    # Nihče ni na potezi
                    pass
    
    def povleci_potezo(self, p):
        igralec = self.igra.na_potezi
        t = self.igra.povleci_potezo(p)

        if t is None:
            # Poteza ni bila veljavna
            pass
        else:
            # Premisli še, če res potrebuješ cel p, ali lahko spremeniš,
            # da bodo funkcije vračale le x koordinato
            (zmagovalec, stirka, p1) = t # Tukaj je p1 dejanska poteza
            if igralec == IGRALEC_R:
                self.narisi_R(p1)
            elif igralec == IGRALEC_Y:
                self.narisi_Y(p1)

            # Sedaj pa preverimo, kako se bo igra nadaljevala
            if zmagovalec == NI_KONEC:
                # Igre še ni konec
                if self.igra.na_potezi == IGRALEC_R:
                    self.napis.set('Na potezi je RDEČI!')
                    self.igralec_r.igraj()
                elif self.igra.na_potezi == IGRALEC_Y:
                    self.napis.set('Na potezi je RUMENI!')
                    self.igralec_y.igraj()
            else:
                # Igra se je končala
                self.koncaj_igro(zmagovalec, stirka)
    
    def prekini_igralce(self):
        '''Sporoči igralcem, da morajo nehati razmišljati.'''
        if self.igralec_r:
            self.igralec_r.prekini()
        if self.igralec_y:
            self.igralec_y.prekini()

    def zacni_igro(self):
        '''Zacne novo igro. Torej zaenkrat le pobriše vse dosedanje poteze.'''
        self.prekini_igralce()

        # Dodamo igralce
        self.igralec_r = Clovek(self)
        self.igralec_y = Clovek(self)

        # Pobrišemo vse figure iz igralne površine        
        self.platno.delete(Gui.TAG_FIGURA)

        # Ustvarimo novo igro
        self.igra = Igra()

        # Rdeči je prvi na potezi
        self.napis.set('Na potezi je RDEČI.')
        self.igralec_r.igraj()

    def zapri_okno(self, master):
        '''Ta metoda se pokliče, ko uporabnik zapre aplikacijo.'''
        # TODO
        # Igralce najprej ustavimo
        self.prekini_igralce()

        # Zapremo okno
        master.destroy()


######################################################################
## Glavni program

# Glavnemu oknu rečemo "root" (koren), ker so grafični elementi
# organizirani v drevo, glavno okno pa je koren tega drevesa

# Ta pogojni stavek preveri, ali smo datoteko pognali kot glavni program in v tem primeru
# izvede kodo. (Načeloma bi lahko datoteko naložili z "import" iz kakšne druge in v tem
# primeru ne bi želeli pognati glavne kode. To je standardni idiom v Pythonu.)

if __name__ == '__main__':
    # Naredimo glavno okno in nastavimo ime
    root = tkinter.Tk()
    root.title('Stiri v vrsto')

    # Naredimo objekt razreda Gui in ga spravimo v spremenljivko,
    # sicer bo Python mislil, da je objekt neuporabljen in ga bo pobrisal
    # iz pomnilnika.
    aplikacija = Gui(root)

    # Kontrolo prepustimo glavnemu oknu. Funkcija mainloop neha
    # delovati, ko okno zapremo.
    root.mainloop()
