# Štiri v vrsto
My Connect-Four game made in Python.

# Uporaba
Zaženete `connect4.py`.

# Cilj
Cilj projekta je izdelati delujočo igrico 'štiri v vrsto' ter še kakšno "podzvrst", ki jo lahko najdete na https://en.wikipedia.org/wiki/Connect_Four pod Rule variations.

# Kratka razlaga
V `connect4.py` je koda za uporabniški vmesnik.
V datotekah `igra.py`, `popout.py` ter `five_row.py` se nahajajo logike iger.
Možnosti človeka so v `clovek.py`, medtem ko je računalnik ustvarjen v `racunalnik.py`. Za odločanje o svojih potezah uporablja algoritem, ki je zapisan v `rand_algoritem.py`.

# Trenutno stanje
Logika vseh treh zvrsti igre je dokončana.
Uporabniški ponuja že večino možnosti, ki bodo na voljo v končnem izdelku. Vizualno še ni dokončan.
Za nasprotnika je možno izbrati tudi računalnik, ki vleče naključne poteze, vendar deluje le za `štiri v vrsto`. Pri podigrah še ne zna igrati.
Funkciji `Razveljavi` ter `Uveljavi` delujeta. Igra zna beležiti tudi rezultat (število zmaganih iger).

# Nekaj idej za v prihodnje (zastarelo)
Dodati je potrebno še možnosti `undo` ter `redo`.

V načrtu je tudi, da se dodela meni, ki bo bolj vizualno privlačen, ter bo imel več možnosti (trenutno ponuja le začetek nove igre) kot so tip igre, single-player ali multi-player, morda tudi tip okvirja itd.

Dodati nameravam tudi "števec", ki bi prikazoval število zmag vsakega igralca znotraj ene "seje".

# Pop Out (dodano)
Trenutno je primarna variacija igre, ki si jo oglejujem, t.i. Pop Out. Tukaj bi verjetno dodal, da Control-B1 poizkusi odstraniti krogec, če je le-to veljavna poteza. Spremeniti bi moral tudi funkcijo `veljavne_poteze`, ki se nahaja v logiki igre, saj trenuten zapis ne omogoča dodatnih kriterijev. Ena izmed opcij bi verjetno bila, da se doda za vsak stolpec še "indikator", ki bi povedal, če je možno izvesti dodatno funkcijo (t.j. odstraniti spodnji krogec).

# Nekaj nepravilnih oziroma pomanjkljivih zadev
1. Logika pri Pop Out še ne deluje kot bi morala. Če je tabla polna, je igre konec, čeprav lahko odstraniš kakšen žeton iz spodnje vrstice. (popravljeno)
2. Pri 5 v vrsto, če imaš 5 v vrsto po diagonali, ti obkroži le 4.
3. Tipke za Undo / Redo. (dodano)
4. Usposobi igro, ko je Igralec 1 računalnik, Igralec 2 pa človek.
