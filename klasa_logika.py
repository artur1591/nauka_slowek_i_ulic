'''
oddzielenie klasy Logika od klasy Okno
'''
import os as OS
import random as RA
from klasa_wpis_ulica_wpis_slowko import WpisSlowko as KWS
from klasa_wpis_ulica_wpis_slowko import WpisUlica as KWU

def sprawdzanie_param_inita(func):
    "jakiś dekorator chciałem dać"
    def wewn(*arg):
        #print('arg[1]',arg[1])
        if not len(arg[1])==4:
            raise ValueError('zły zestaw arg wejsciowych klasy Logika.jest',arg)

        if arg[1][0]=='':
            raise ValueError('plik slowka powinien byc niepusty')
        if arg[1][1]=='':
            raise ValueError('plik ulice powinien byc niepusty')
        if not arg[1][2] in ['A','B','C']:
            raise ValueError('tryb powinien byc A/B/C. jest',arg[1][2])
        if int(arg[1][3])<0 or int(arg[1][3])>100:
            raise ValueError('procent powinien byc 0-100',int(arg[1][3]))

        func(*arg)
    return wewn

class Logika:
    "..."
    @sprawdzanie_param_inita
    def __init__(self,ust_log):
        "potrzebuje argumentów początkowych"
        #print('ustL=',ust_log)
        self.plik_slowka=ust_log[0]
        self.plik_ulice=ust_log[1]
        self.lista_zadan=list()
        self.lista_slowek=None
        self.lista_ulic=None
        self.komunikat_bledu=''

        self.biezacy_tryb=ust_log[2]
        self.procent_slowek_reszta_ulic=ust_log[3]

        self.biezacy_wpis=None
        self.rodzaj_biezacego_wpisu=''

        self.wczytaj_slowka()
        self.wczytaj_ulice()

    def zamknij(self):
        "taki __del__"
        self.zapisz_slowka()
        self.zapisz_ulice()

    def wczytaj_slowka(self):
        '''
        wypełnia self.lista_slowek listą typu WpisSlowko

        zwraca True jak się udało

        zwraca False jak brak pliku
        zwraca False jak pusty plik
        zwraca False jak są błędne dane
        ustawia self.komunikat_bledu żeby było wiadomo co źle poszło

        jak sprawdza że są błędne dane:
            ilość | powinna być 1
            powinno być tryb czyli zawierać jeden z ' A ' ' B ' ' C '
            na końcu powinna być liczba
        '''
        #czy plik istnieje:
        if not OS.path.exists(self.plik_slowka):
            self.komunikat_bledu='brakuje pliku plik_slowka('+self.plik_slowka+')'
            return False

        #czy plik niepusty:
        if OS.stat(self.plik_slowka).st_size==0:
            self.komunikat_bledu='plik_slowka(',self.plik_slowka,') jest pusty'
            return False

        #jak plik niepusty wczytywanie:
        self.lista_slowek=list()

        with open(self.plik_slowka) as plik:
            linie=plik.read()
            #print('linie1',linie,'_')

        linie=linie[:-1]
        #print('linie2',linie,'_')

        for linia in linie.split('\n'):
            #print('liniaS=',linia)
            if linia.count('|')!=1:
                self.komunikat_bledu='błędne dane wejściowe(słówka): brak | w linii:'+str(linia)
                #print('błędne dane wejściowe. brak | w linii:',linia)
                return False
            if not any([linia.__contains__(wl) for wl in [' A',' B',' C']]):
                self.komunikat_bledu='błędne dane wejściowe(słówka): brak trybu w linii:'+str(linia)
                #print('błędne dane wejściowe. brak trybu w linii:',linia)
                return False
            if not linia.split()[-1].isdigit():
                self.komunikat_bledu='błędne dane wejściowe(słówka): brak liczby na końcu w linii:'+str(linia)
                #print('błędne dane wejściowe(słówka): brak liczby na końcu w linii:',linia)
                return False
            przerwa_po_pierwszy=linia.index('|')
            tmp_pierwszy=linia[0:przerwa_po_pierwszy]
            przerwa_po_trybie=linia.rindex(' ')
            tmp_ile_x=linia[przerwa_po_trybie+1:].rstrip()
            tmp_drugi=linia[przerwa_po_pierwszy+1:przerwa_po_trybie-2]
            tmp_tryb=linia[przerwa_po_trybie-1:przerwa_po_trybie]

            tmp=KWS(tmp_pierwszy,tmp_drugi,tmp_tryb,int(tmp_ile_x))
            self.lista_slowek.append(tmp)
        #print('self.lista_slowek',self.lista_slowek)

        if len(self.lista_slowek)==0:
            raise ValueError('brak słówek w lista_slowek')
        return True

    def wczytaj_ulice(self):
        '''
        wypełnia self.lista_ulic listą typu WpisUlica

        zwraca True jak się udało

        zwraca False jak brak pliku
        zwraca False jak pusty plik
        zwraca False jak są błędne dane
        ustawia self.komunikat_bledu żeby było wiadomo co źle poszło

        jak sprawdza że są błędne dane:
            ilość | powinna być 1
            powinno być tryb czyli zawierać jeden z '|A' '|B' '|C'
            na końcu powinna być liczba
        '''
        #czy plik istnieje:
        if not OS.path.exists(self.plik_ulice):
            self.komunikat_bledu='brakuje pliku plik_ulice('+self.plik_ulice+')'
            return False

        #czy plik niepusty:
        if OS.stat(self.plik_ulice).st_size==0:
            self.komunikat_bledu='plik_ulice(',self.plik_ulice,') jest pusty'
            return False

        #jak plik niepusty wczytywanie:
        self.lista_ulic=list()

        with open(self.plik_ulice) as plik:
            linie=plik.read()
            #print('linie1',linie,'_')

        linie=linie[:-1]
        #print('linie2',linie,'_')

        for linia in linie.split('\n'):
            #print('liniaU=',linia)
            if linia.count('|')!=1:
                self.komunikat_bledu='błędne dane wejściowe(ulice): brak | w linii:'+str(linia)
                #print('błędne dane wejściowe. brak | w linii:',linia)
                return False
            if not any([linia.__contains__(wl) for wl in ['|A','|B','|C']]):
                self.komunikat_bledu='błędne dane wejściowe(ulice): brak trybu w linii:'+str(linia)
                #print('błędne dane wejściowe. brak trybu w linii:',linia)
                return False
            if not linia.split()[-1].isdigit():
                self.komunikat_bledu='błędne dane wejściowe(ulice): brak liczby na końcu w linii:'+str(linia)
                #print('błędne dane wejściowe(ulice): brak liczby na końcu w linii:',linia)
                return False
            przerwa_po_pierwszy=linia.rindex('|')
            tmp_pierwszy=linia[0:przerwa_po_pierwszy]
            tmp_tryb=linia[przerwa_po_pierwszy+1:przerwa_po_pierwszy+2]
            tmp_ile_x=linia[przerwa_po_pierwszy+3:]

            tmp=KWU(tmp_pierwszy,tmp_tryb,int(tmp_ile_x))
            #print('tmpU',tmp)
            self.lista_ulic.append(tmp)
        #print('self.lista_ulic',self.lista_ulic)

        if len(self.lista_ulic)==0:
            raise ValueError('brak ulic w lista_ulic')
        return True

    def zapisz_slowka(self):
        "self.lista_slowek do pliku okreslonego w self.plik_slowka"
        #sortuj dla czytelności pliku
        self.lista_slowek.sort()

        with open(self.plik_slowka,'w') as plik:
            for wpis in self.lista_slowek:
                plik.write(str(wpis)+'\n')

        return True

    def zapisz_ulice(self):
        "self.lista_ulic do pliku określonego w self.plik_ulice"
        #sortuj dla czytelności pliku
        self.lista_ulic.sort()

        with open(self.plik_ulice,"w") as plik:
            for wpis in self.lista_ulic:
                plik.write(str(wpis)+'\n')

        return True

    def czy_sa_slowka_w_trybie(self):
        '''
        potrzebne przy zmianie trybu
        '''
        for slowko in self.lista_slowek:
            if slowko.tryb==self.biezacy_tryb:
                return True

        return False

    def czy_sa_ulice_w_trybie(self):
        '''
        potrzebne przy zmianie trybu
        jawnie określony tryb dla czytelności
        '''
        for ulica in self.lista_ulic:
            if ulica.tryb==self.biezacy_tryb:
                return True

        return False

    def zrob_liste_zadan(self):
        '''
        lista_zadan żeby były albo 'u' albo 's1' wg procent_slowek_reszta_ulic
        ale lista skorygowana o obecność/brak słówek/ulic w danym trybie
            (wtedy tylko istniejące na liście zadan)
        '''
        self.lista_zadan=list()
        #print('czy_sa_slowka_w_trybie',self.biezacy_tryb,self.czy_sa_slowka_w_trybie())
        #print('czy_sa_ulice_w_trybie',self.biezacy_tryb,self.czy_sa_ulice_w_trybie())

        #jeżeli ile_slowek/ile_ulic w danym trybie SĄ to proporcje zachowuje
        #jeśli brak to 100% danego
        ile_zrobic=10
        ile_ulic=0
        ile_slowek=0

        if self.czy_sa_slowka_w_trybie() and not self.czy_sa_ulice_w_trybie():
            ile_slowek=ile_zrobic
        if not self.czy_sa_slowka_w_trybie() and self.czy_sa_ulice_w_trybie():
            ile_ulic=ile_zrobic
        if self.czy_sa_slowka_w_trybie() and self.czy_sa_ulice_w_trybie():
            ile_slowek=int(ile_zrobic*self.procent_slowek_reszta_ulic/100)
            ile_ulic=ile_zrobic-ile_slowek
            #print('ile_slowek',ile_slowek,'ile_ulic',ile_ulic)

        for _ in range(ile_slowek):
            self.lista_zadan.append('s1')

        for _ in range(ile_ulic):
            self.lista_zadan.append('u')

        RA.shuffle(self.lista_zadan)
        #print('lista_zadan',self.lista_zadan)

    def wez_z_listy_zadan(self):
        "daje kolejne z listy zadan i w razie potrzeby uzupełnia ją(od końca)"
        if len(self.lista_zadan)==0:
            self.zrob_liste_zadan()

        return self.lista_zadan.pop()

    def jaki_najrzadziej_slowko(self):
        '''
        tylko z tych z biezacy_tryb
        zwraca int-a jak są słówka z biezacy_tryb
        zwraca False jak brakuje slowek z biezacy_tryb
        '''
        lista_slowek_z_biez_tryb=list()

        for slowko in self.lista_slowek:
            if slowko.tryb==self.biezacy_tryb:
                lista_slowek_z_biez_tryb.append(slowko)
        #print('lista_slowek_z_biez_tryb(',self.biezacy_tryb,')',lista_slowek_z_biez_tryb)

        if len(lista_slowek_z_biez_tryb)==0:
            return False

        najrzadsze_slowko_int=lista_slowek_z_biez_tryb[0].ile_razy_wylos

        for ktore in lista_slowek_z_biez_tryb:
            if ktore.ile_razy_wylos<najrzadsze_slowko_int:
                najrzadsze_slowko_int=ktore.ile_razy_wylos

        return najrzadsze_slowko_int

    def jaki_najrzadziej_ulica(self):
        '''
        tylko z tych z biezacy_tryb
        zwraca int-a jak są ulice z biezacy_tryb
        zwraca False jak brakuje ulic z biezacy_tryb
        '''
        lista_ulic_z_biez_tryb=list()

        for ulica in self.lista_ulic:
            if ulica.tryb==self.biezacy_tryb:
                lista_ulic_z_biez_tryb.append(ulica)
        #print('lista_ulic_z_biez_tryb(',self.biezacy_tryb,')',lista_ulic_z_biez_tryb)

        if len(lista_ulic_z_biez_tryb)==0:
            return False

        najrzadsza_ulica_int=lista_ulic_z_biez_tryb[0].ile_razy_wylos

        for ktore in lista_ulic_z_biez_tryb:
            if ktore.ile_razy_wylos<najrzadsza_ulica_int:
                najrzadsza_ulica_int=ktore.ile_razy_wylos

        return najrzadsza_ulica_int

    def wylosuj_slowko_z_inkrem(self):
        '''
        wylosuj takie jak biezacy_tryb
        jak lista pusta lub brak słówek z bieżacym trybem zwraca False.
        powienien zwrócić typ WpisSlowko
        '''
        if len(self.lista_slowek)==0:
            #print('lista slowek 0')
            return False

        najrzadsze=self.jaki_najrzadziej_slowko()
        #print('najrzadsze',najrzadsze)
        if najrzadsze is False:
            #print('brak w tym trybie')
            return False

        lista_najrzadszych=[]

        for wpis in self.lista_slowek:
            if wpis.ile_razy_wylos==najrzadsze and wpis.tryb==self.biezacy_tryb:
                #print('wpis',wpis)
                lista_najrzadszych.append(wpis)

        wylosowane=RA.choice(lista_najrzadszych)
        #print('wylosowane',wylosowane)

        #inkrem:
        for wpisy in self.lista_slowek:
            if wpisy==wylosowane:
                wpisy.ile_razy_wylos+=1
                break
        #print('po',self.lista_slowek)
        return wylosowane

    def wylosuj_ulice_z_inkrem(self):
        '''
        wylosuj takie jak biezacy_tryb
        jak lista pusta lub brak ulic z bieżacym trybem zwraca False.
        powienien zwrócić typ WpisUlica
        '''
        if len(self.lista_slowek)==0:
            return False

        najrzadsze=self.jaki_najrzadziej_ulica()
        if najrzadsze is False:
            return False

        lista_najrzadszych=[]

        for wpis in self.lista_ulic:
            if wpis.ile_razy_wylos==najrzadsze and wpis.tryb==self.biezacy_tryb:
                lista_najrzadszych.append(wpis)

        wylosowane=RA.choice(lista_najrzadszych)
        #print('wylosowane',wylosowane)

        #inkrem:
        for wpisy in self.lista_ulic:
            if wpisy==wylosowane:
                wpisy.ile_razy_wylos+=1
                break
        #print('po',self.lista_ulic)
        return wylosowane

    def zeruj_slowka(self):
        "slowka z lista_slowek ile_razy_wylos=0"
        for wpis in self.lista_slowek:
            wpis.ile_razy_wylos=0

    def zeruj_ulice(self):
        "ulice z lista_ulic ile_razy_wylos=0"
        for wpis in self.lista_ulic:
            wpis.ile_razy_wylos=0

    def ustaw_biezacy_tryb(self,na_jaki):
        '''
        jednak druga f.zmiany trybu może się przydać
        aktualizuje liste_zadan
        zwraca nowy tryb
        '''
        if not na_jaki in ['A','B','C']:
            raise ValueError('tryb musi być:A/B/C.jest',na_jaki)

        self.biezacy_tryb=na_jaki
        self.zrob_liste_zadan()

        return self.biezacy_tryb

    def zmien_biezacy_tryb(self):
        '''
        konwencja trybu z dużej czyli A lub B lub C
        aktualizuje liste_zadan
        zwraca nowy biezacy tryb
        '''

        if self.biezacy_tryb=='A':
            self.biezacy_tryb='B'
        elif self.biezacy_tryb=='B':
            self.biezacy_tryb='C'
        else:
            self.biezacy_tryb='A'

        self.zrob_liste_zadan()
        #print('nowy biezacy_tryb',self.biezacy_tryb)
        return self.biezacy_tryb

    def ustaw_tryb_biezacego_wpisu(self,na_jaki):
        '''
        konwencja trybu z dużej czyli A lub B lub C
        zwraca True jak sie udało.
        False jak nie
        jak przydziela nowy tryb do zeruje ile_razy_wylos
        po wykonaniu zmiany trybu aktualizaje lista_slowek/ulic
        '''
        if not na_jaki in ['A','B','C']:
            raise ValueError('nowy tryb musi być A/B/C')
        #print('na_jaki',na_jaki)

        #zapamietuje biezacy(zeby podmienic)
        dotychczasowy=self.biezacy_wpis
        #print('dotychczasowy',dotychczasowy)

        #aktualizacja trybu + ile_razy_wylos zeruj
        self.biezacy_wpis.tryb=na_jaki
        self.biezacy_wpis.ile_razy_wylos=0

        poprawiony=self.biezacy_wpis
        #print('poprawiony',poprawiony)

        #aktualizuje w lista_*
        self.zmien_wpis(dotychczasowy,poprawiony)

    def cofnij_ilosc_wylos_biez_wpisu_lo(self):
        "dla bieżącego wpisu dekrementuj ile_razy_wylos w self.lista_slowek/ulic"

        if isinstance(self.biezacy_wpis,KWS):
            ind_biez=self.lista_slowek.index(self.biezacy_wpis)
            #print('jaki_jestS',ind_biez)
            if self.lista_slowek[ind_biez].ile_razy_wylos>0:
                #print('było już losowane=>dekrement')
                self.lista_slowek[ind_biez].ile_razy_wylos-=1
            else:
                print()
                #print('jest już 0')
        else:
            ind_biez=self.lista_ulic.index(self.biezacy_wpis)
            #print('jaki_jestU',ind_biez)
            if self.lista_ulic[ind_biez].ile_razy_wylos>0:
                #print('było już losowane=>dekrement')
                self.lista_ulic[ind_biez].ile_razy_wylos-=1
            else:
                print()
                #print('jest już 0')

    #CRUD. ale kolejność od samodzielnych po zależne
    def czy_wpis_istnieje(self,jaki_wpis):
        '''
        sprawdza typ wpisu i sprawdza obecność w pierwszy/drugi
            przy pomocy == czyli konieczne ścisłe dopasowanie
        zwraca True jak istnieje taki lub False jak nie ma takiego
        '''
        if not isinstance(jaki_wpis,KWS) and not isinstance(jaki_wpis,KWU):
            raise TypeError('czy_wpis_istnieje. typ=',type(jaki_wpis))

        if isinstance(jaki_wpis,KWS):
            return jaki_wpis in self.lista_slowek
        return jaki_wpis in self.lista_ulic

    def szukaj_wpis(self,szukany_str,*,typ):
        '''
        pobiera str  wymaga typu 's' lub 'u'
        szukanie metodą str.find ale wymaga co najmniej 3znaków
        zwraca znaleziony Wpis (lub listę Wpisów) jeśli dopasował pierwszy/drugi
        zwraca False jeśli:
            mniej niż 3 znaki zapytania
            dopasowanie pierwszy/drugi nieudało się
        '''
        #print('szukany_str',szukany_str,len(szukany_str),typ)
        if szukany_str=='':
            raise ValueError('szukany_str powinien być niepusty')
        if not isinstance(szukany_str,str):
            raise TypeError('szukany powinien być str-em.jest',type(szukany_str))
        if len(szukany_str)<3:
            #print('wpisz więcej niż 2 znaki szukanego')
            return False
        if not typ in ['s','u']:
            raise ValueError('typ powinien być s/u. jest',typ)

        #print('szukaj_wpis',szukany_str,len(szukany_str),typ)

        znalezione_wpisy=[]

        if typ=='s':
            #jak WpisSlowko
            for slowko in self.lista_slowek:
                if slowko.pierwszy.find(szukany_str)!=-1 or slowko.drugi.find(szukany_str)!=-1:
                    znalezione_wpisy.append(slowko)
        else:
            #jak WpisUlica
            for ulica in self.lista_ulic:
                if ulica.pierwszy.find(szukany_str)!=-1:
                    znalezione_wpisy.append(ulica)

        if len(znalezione_wpisy)==0:
            return False
        if len(znalezione_wpisy)==1:
            return znalezione_wpisy[0]
        return znalezione_wpisy


    def dodaj_wpis(self,nowy_wpis):
        '''
        sprawdza czy jest taki: f.czy_wpis_istnieje()
        False jesli istnieje juz
        wykrywa typ i doklada czyli zwraca True jeśli dopis się udał
        '''
        if not isinstance(nowy_wpis,KWS) and not isinstance(nowy_wpis,KWU):
            raise TypeError('dodać można Wpis a nie',type(nowy_wpis))

        czy_jest_taki=self.czy_wpis_istnieje(nowy_wpis)
        if czy_jest_taki:
            return False

        if isinstance(nowy_wpis,KWS):
            #jak WpisSlowko
            self.lista_slowek.append(nowy_wpis)
        else:
            #jak WpisUlica
            self.lista_ulic.append(nowy_wpis)
        return True

    def zmien_wpis(self,stary_wpis,nowy_wpis):
        '''
        wykrywa typ
        stary_wpis musi być na liście
        nowy_wpis niemoże być na liście

        return True jak sie udalo
        return False jak nie
        '''
        if not isinstance(nowy_wpis,KWS) and not isinstance(nowy_wpis,KWU):
            raise TypeError('zmien_wpis typy=',type(stary_wpis),type(nowy_wpis))

        if type(stary_wpis) is not type(nowy_wpis):
            raise TypeError("nieuprawniona zmiana typu wpisu")

        if self.czy_wpis_istnieje(stary_wpis) and not self.czy_wpis_istnieje(nowy_wpis):
            if isinstance(stary_wpis,KWS):
                indeks_starego=self.lista_slowek.index(stary_wpis)
                self.lista_slowek[indeks_starego]=nowy_wpis
            else:
                indeks_starego=self.lista_ulic.index(stary_wpis)
                self.lista_ulic[indeks_starego]=nowy_wpis
            return True
        #else:
        #print('brakuje starego wpisu i/lub nowy już istnieje')
        return False

    def kasuj_wpis(self,do_kasow_wpis):
        '''
        ścisłe dopasowanie nazw konieczne czyli pierwszy tylko sprawdza
        True jak skasowal
        False jak nie
        '''
        if not isinstance(do_kasow_wpis,KWS) and not isinstance(do_kasow_wpis,KWU):
            raise TypeError('kasować można Wpis a nie',type(do_kasow_wpis))

        if isinstance(do_kasow_wpis,KWS):
            #jak WpisSlowko
            for slowko in self.lista_slowek:
                if do_kasow_wpis.pierwszy==slowko.pierwszy:
                    self.lista_slowek.remove(do_kasow_wpis)
                    return True
        else:
            #jak WpisUlica
            for ulica in self.lista_ulic:
                if do_kasow_wpis.pierwszy==ulica.pierwszy:
                    self.lista_ulic.remove(do_kasow_wpis)
                    return True
        return False

    def zwroc_ust_log_do_zapisu(self):
        "daje składowe klasy do zapisu w pliku ustawienia.xml"
        return [self.plik_slowka,self.plik_ulice,self.biezacy_tryb,self.procent_slowek_reszta_ulic]

if __name__=='__main__':
    print('---są testy do tej klasy---')
