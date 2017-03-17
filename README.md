# Štiri v vrsto
My Connect-Four game made in Python.

# Uporaba
Zaženete `connect4.py`.

# Cilj
Cilj projekta je izdelati delujočo igrico 'štiri v vrsto' ter še kakšno "podzvrst", ki jo lahko najdete na https://en.wikipedia.org/wiki/Connect_Four pod Rule variations.

# Kratka razlaga
V `connect4.py` je koda za uporabniški vmesnik, `igra.py` vsebuje logiko igre, `clovek.py` pa predstavlja igralca.

# Trenutno stanje
Logika igre je večinoma končana, igra bi trenutno za 2 igralca morala delovati brez problemov. Računalnika še za nasprotnika ni možno izbrati.

# Nekaj idej za v prihodnje
Dodati je potrebno še možnosti `undo` ter `redo`.

V načrtu je tudi, da se dodela meni, ki bo bolj vizualno privlačen, ter bo imel več možnosti (trenutno ponuja le začetek nove igre) kot so tip igre, single-player ali multi-player, morda tudi tip okvirja itd.

Dodati nameravam tudi "števec", ki bi prikazoval število zmag vsakega igralca znotraj ene "seje".

# Pop Out
Trenutno je primarna variacija igre, ki si jo oglejujem, t.i. Pop Out. Tukaj bi verjetno dodal, da Control-B1 poizkusi odstraniti krogec, če je le-to veljavna poteza. Spremeniti bi moral tudi funkcijo `veljavne_poteze`, ki se nahaja v logiki igre, saj trenuten zapis ne omogoča dodatnih kriterijev. Ena izmed opcij bi verjetno bila, da se doda za vsak stolpec še "indikator", ki bi povedal, če je možno izvesti dodatno funkcijo (t.j. odstraniti spodnji krogec).
