'''
oddzielenie klasy Logika od klasy Okno
'''
import os as OS
import datetime as DT
import threading as TH
import random as RA
import re as RE
import enum as EN
import nltk.corpus as NL_CO
import polyglot.detect as POL_DET
import polyglot.detect.base as POL_BAS
POL_BAS.logger.setLevel("ERROR")
import reportlab.pdfgen.canvas as RL_CAN
import reportlab.lib.pagesizes as RL_ROZ
import reportlab.pdfbase.ttfonts as RL_TTF
import reportlab.pdfbase.pdfmetrics as RL_MET
import klasa_statystyki as KS
import klasa_wpis_ulica_wpis_slowko as KW
from klasa_wpis_ulica_wpis_slowko import WpisUlica as KWU
from klasa_wpis_ulica_wpis_slowko import WpisSlowko as KWS

dopiski_status=EN.Enum('dopiski_status',['WCZYTALEM_W_LISTE_DOPISKI',
                                        'WYKRYWAM_JEZYK','JEZYK_WYKRYTY',
                                        'DOPISALEM_DO_LISTY_WPISOW','UKRYJ_LABEL'])

def sprawdzanie_param_inita(func):
    "jakiś dekorator chciałem dać"
    def wewn(*arg):
        #print('arg[1]',arg[1])
        if not len(arg[1])==6:
            raise ValueError('zły zestaw arg wejsciowych klasy Logika.jest',arg)

        if arg[1][0]=='':
            raise ValueError('plik ulice powinien byc niepusty')
        if arg[1][1]=='':
            raise ValueError('plik slowka powinien byc niepusty')
        if not arg[1][2] in ['A','B','C']:
            raise ValueError('tryb powinien byc A/B/C. jest',arg[1][2])
        if int(arg[1][3])<0 or int(arg[1][3])>100:
            raise ValueError('procent powinien byc 0-100',int(arg[1][3]))
        if arg[1][4]=='':
            raise ValueError('plik_dopiski_ulice pusty')
        if arg[1][5]=='':
            raise ValueError('plik_dopiski_slowka pusty')

        func(*arg)
    return wewn

class Logika:
    '''
    self.komunikat_bledu ustawiany przez:
        wczytaj_slowka,wczytaj_ulice,zrob_liste_zadan

    zerowany:
        zrob_liste_zadan,
    '''
    class Dopiski:
        ""
        def __init__(self,plik_ulice,plik_slowka):
            ""
            self.ob_kl_lo=None
            self.ulice_lista=list()
            self.ulice_plik=plik_ulice
            self.ulice_status=dopiski_status.UKRYJ_LABEL
            self.slowka_lista=list()
            self.slowka_plik=plik_slowka
            self.slowka_status=dopiski_status.UKRYJ_LABEL
            self.zakoncz_watki=False
            #print('init klasy Dopiski(',plik_ulice,',',plik_slowka,')',sep='')

        def ustaw(self,ob_kl_lo):
            self.ob_kl_lo=ob_kl_lo
            self.ob_kl_lo.fun_dopiski()

        def zamknij(self):
            self.zakoncz_watki=True
            #print('zamykanie klasy Dopiski')

    @sprawdzanie_param_inita
    def __init__(self,ust_log):
        "potrzebuje argumentów początkowych"
        #print('ustL=',ust_log)
        self.plik_ulice=ust_log[0]
        self.plik_slowka=ust_log[1]
        self.lista_zadan=list()
        self.lista_ulic=list()
        self.lista_slowek=list()
        self.komunikat_bledu=''
        self.stats=KS.Statystyki()
        self.plik_dopiski_ulice=ust_log[4]
        self.plik_dopiski_slowka=ust_log[5]
        self.dopiski=self.Dopiski(self.plik_dopiski_ulice,self.plik_dopiski_slowka)

        self.biezacy_tryb=ust_log[2]
        self.procent_slowek_reszta_ulic=ust_log[3]

        self.biezacy_wpis=None
        self.rodzaj_biezacego_wpisu=''

        #main
        self.wczytaj_ulice()
        self.wczytaj_slowka()
        self.stats.wczytaj()
        self.dopiski.ustaw(self)
        if not self.komunikat_bledu:
            self.ustaw_biezacy_tryb(self.biezacy_tryb)

    def zamknij(self):
        "taki __del__"
        print('zamknij logika')
        if not self.komunikat_bledu:
            self.zapisz_ulice()
            self.zapisz_slowka()
            self.stats.zapisz()
            self.dopiski.zamknij()
            print('---czyste zamknięcie programu---')
        else:
            print('niezapisuje ulic,słówek bo błąd:',self.komunikat_bledu)

    def wczytaj_ulice(self):
        '''
        wypełnia self.lista_ulic listą typu WpisUlica

        zwraca True jak się udało

        zwraca False jak brak pliku
        zwraca False jak pusty plik
        zwraca False jak są błędne dane(klasa WpisUlica o tym decyduje)
        ustawia self.komunikat_bledu żeby było wiadomo co źle poszło
        (może też wypisać w konsoli)
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
            #print('linieU1',linie,'_')

        linie=linie[:-1]
        #print('linieU2',linie,'_')

        for linia in linie.split('\n'):
            #print('liniaU1=',linia)
            co_wyszlo=KW.str_do_wpis_ulica(linia)
            #print('co_wyszloU',co_wyszlo,'_')
            #if isinstance(co_wyszlo,KWU):
            #    print('dobrze str->WpisUlica')

            if co_wyszlo is False:
                self.komunikat_bledu='str->WpisUlica nieudany'
                print('wczytując ulice.linia:',linia,'_')
                print('błąd:',self.komunikat_bledu)
                return False
            self.lista_ulic.append(co_wyszlo)
        #print('self.lista_ulic',self.lista_ulic)

        if len(self.lista_ulic)==0:
            raise ValueError('brak ulic w lista_ulic')
        return True

    def wczytaj_slowka(self):
        '''
        wypełnia self.lista_slowek listą typu WpisSlowko

        zwraca True jak się udało

        zwraca False jak brak pliku
        zwraca False jak pusty plik
        zwraca False jak są błędne dane(klasa WpisSlowko o tym decyduje)
        ustawia self.komunikat_bledu żeby było wiadomo co źle poszło
        (może też wypisać w konsoli)
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
            #print('linieS1',linie,'_')

        linie=linie[:-1]
        #print('linieS2',linie,'_')

        for linia in linie.split('\n'):
            #print('liniaS=',linia)
            co_wyszlo=KW.str_do_wpis_slowko(linia)
            #if isinstance(co_wyszlo,KWS):
            #    print('dobrze str->WpisSlowko')

            if co_wyszlo is False:
                self.komunikat_bledu='str->WpisSlowko nieudany'
                print('wczytując słówka.linia:',linia,'_')
                print('błąd:',self.komunikat_bledu)
                return False
            self.lista_slowek.append(co_wyszlo)
        #print('self.lista_slowek',self.lista_slowek)

        if len(self.lista_slowek)==0:
            raise ValueError('brak słówek w lista_slowek')
        return True


    def zrob_kopie_bezpieczenstwa(self,jakiego_pliku,komentarz=''):
        '''
        jakby między wczytaniem a zapisem wydarzyło się coś dziwnego
        zmienia nazwę plikowi który był. więc zapisanie nawet niepoprawne przejdzie
        '''
        nowa_nazwa=jakiego_pliku+str(DT.datetime.today())
        OS.rename(jakiego_pliku,nowa_nazwa)
        print('---robię kopie bezpieczeństwa pliku:',nowa_nazwa,'---',komentarz)

    def zapisz_ulice(self):
        '''
        self.lista_ulic do pliku określonego w self.plik_ulice

        jeśli lista_ulic ma mniej niż 2 elementy to tworzy kopie bezpieczeństwa
        bo pewnie coś poszło źle
        '''
        #sortuj dla czytelności pliku
        self.lista_ulic.sort()

        if len(self.lista_ulic)<2:
            self.zrob_kopie_bezpieczenstwa(self.plik_ulice,"podejrzanie mało wpisów")

        with open(self.plik_ulice,"w") as plik:
            for wpis in self.lista_ulic:
                plik.write(str(wpis)+'\n')

        return True

    def zapisz_slowka(self):
        '''
        self.lista_slowek do pliku okreslonego w self.plik_slowka

        jeśli lista_ulic ma mniej niż 2 elementy to tworzy kopie bezpieczeństwa
        bo pewnie coś poszło źle
        '''
        #sortuj dla czytelności pliku
        self.lista_slowek.sort()

        if len(self.lista_slowek)<2:
            self.zrob_kopie_bezpieczenstwa(self.plik_slowka,"podejrzanie mało wpisów")

        with open(self.plik_slowka,'w') as plik:
            for wpis in self.lista_slowek:
                plik.write(str(wpis)+'\n')

        return True

    def fun_dopiski(self):
        ""
        #print('f.fun_dopiski')
        def zwroc_plik_w_liscie(nazwa_pliku):
            "wczytuj wszystko jak leci"
            #print('f.zwroc_plik_w_liscie',nazwa_pliku)
            caly_plik=list()
            gotowy=list()

            with open(nazwa_pliku,mode='r',encoding='UTF-8') as plik:
                caly_plik=plik.readlines()

            #print('---caly_plik(',nazwa_pliku,'):',caly_plik)
            for slowo in caly_plik:
                slowo=slowo.rstrip()
                if slowo:
                    #print('slowo=',slowo)
                    if slowo.isdigit():
                        print('---wykryłem liczbę',slowo,'więc pomijam.')
                    else:
                        gotowy.append(slowo)

            print('---gotowy(',nazwa_pliku,'):',gotowy)
            return gotowy

        def wykrywanie_jezyka_slowek_watek():
            #print('tlumacze...')
            self.dopiski.slowka_status=dopiski_status.WYKRYWAM_JEZYK
            self.dopiski.slowka_lista=[self.jezyk_slowa(slowo) for slowo in self.dopiski.slowka_lista]
            print('---po',self.dopiski.slowka_lista)
            self.dopiski.slowka_status=dopiski_status.JEZYK_WYKRYTY

        ilu_plikow_brakuje=0

        if OS.path.exists(self.dopiski.ulice_plik):
            #print('---jest plik',self.dopiski.ulice_plik)
            if OS.stat(self.dopiski.ulice_plik).st_size>0:
                #print('--- plik',self.dopiski.ulice_plik,'niepusty')
                self.dopiski.ulice_lista=zwroc_plik_w_liscie(self.dopiski.ulice_plik)
                self.dopiski.ulice_status=dopiski_status.WCZYTALEM_W_LISTE_DOPISKI
            else:
                ilu_plikow_brakuje+=1
        else:
            ilu_plikow_brakuje+=1

        if OS.path.exists(self.dopiski.slowka_plik):
            #print('---jest plik',self.dopiski.slowka_plik)
            if OS.stat(self.dopiski.slowka_plik).st_size>0:
                #print('--- plik',self.dopiski.slowka_plik,'niepusty')
                self.dopiski.slowka_lista=zwroc_plik_w_liscie(self.dopiski.slowka_plik)
                self.dopiski.slowka_status=dopiski_status.WCZYTALEM_W_LISTE_DOPISKI
                #watek=TH.Thread(target=wykrywanie_jezyka_slowek_watek,daemon=True).start()
                TH.Thread(target=wykrywanie_jezyka_slowek_watek,daemon=True).start()
            else:
                ilu_plikow_brakuje+=1
        else:
            ilu_plikow_brakuje+=1

        #print('ilu_plikow_brakuje=',ilu_plikow_brakuje)
        if ilu_plikow_brakuje==2:
            self.dopiski.zakoncz_watki=True
        #print('dopiski.zakoncz_watki=',self.dopiski.zakoncz_watki)

    def jezyk_slowa(self,slowo):
        '''
        celem jest orzeczenie czy polskie czy angielskie,
        może sobie nieradzić więc w razie czego orzeka na polskie
        '''
        class Watek(TH.Thread):
            ""
            def __init__(self,slowo):
                ""
                TH.Thread.__init__(self,daemon=True)
                self.slowo=slowo
                self.value=''
            def czy_zawiera_polskie_znaki(self):
                "zwraca True lub False"
                wzor=RE.compile('[ąćęłńóżźĄĆĘŁŃÓŻŹ]')
                wynik=wzor.search(self.slowo)
                if wynik is None:
                    return False
                return True
            def czy_to_ang_slowo(self):
                "zwraca True lub False"
                wordnet=NL_CO.wordnet
                if wordnet.synsets(self.slowo):
                    return True
                return False
            def polyglotem_jezyk(self):
                "zwraca en lub pl"
                for lang in POL_DET.Detector(self.slowo).languages:
                    if not lang.code in ['en','pl']:
                        #print('Detector->niewłaściwe: słowo',slowo)
                        #print('POL->',slowo,lang.code)
                        pass
                    return lang.code

            def jezyk_wykryj(self):
                "powinna zwrócić en lub pl. sprawdzić czy daje radę zawsze"
                #print('sprawdzam slowo=',self.slowo)
                if self.czy_zawiera_polskie_znaki():
                    #print('zawiera_polskie_znaki')
                    return 'pl'
                if self.czy_to_ang_slowo():
                    #print('ANG slowo')
                    return 'en'
                return self.polyglotem_jezyk()

            def run(self):
                ""
                if self.slowo:
                    self.value=self.jezyk_wykryj()
                else:
                    self.value=False

        wat=Watek(slowo)
        wat.start()
        wat.join()
        return [wat.value,slowo]

    def czy_sa_ulice_w_trybie(self):
        '''
        potrzebne przy zmianie trybu
        '''
        for ulica in self.lista_ulic:
            if ulica.tryb==self.biezacy_tryb:
                return True

        return False

    def czy_sa_slowka_w_trybie(self):
        '''
        potrzebne przy zmianie trybu
        '''
        for slowko in self.lista_slowek:
            if slowko.tryb==self.biezacy_tryb:
                return True

        return False


    def zrob_liste_zadan(self):
        '''
        lista_zadan żeby były albo 'u' albo 's1' wg procent_slowek_reszta_ulic
        ale lista skorygowana o obecność/brak słówek/ulic w danym trybie
            (wtedy tylko istniejące na liście zadan)

        zwraca False jak brakuje słówek i ulic w danym trybie
            i ustawia self.komunikat_bledu, zeruje rodzaj_biezacego_wpisu+biezacy_wpis
        zwraca True jak sie udało zrobić listę w danym trybie
            i czyści komunikat_bledu (self.komunikat_bledu='')
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
        if not self.czy_sa_slowka_w_trybie() and not self.czy_sa_ulice_w_trybie():
            self.komunikat_bledu='brak ulic i słówek z trybie'+self.biezacy_tryb
            self.biezacy_wpis=''
            self.rodzaj_biezacego_wpisu=''
            return False

        for _ in range(ile_ulic):
            self.lista_zadan.append('u')

        for _ in range(ile_slowek):
            self.lista_zadan.append('s1')

        RA.shuffle(self.lista_zadan)
        #print('lista_zadan',self.lista_zadan)
        self.komunikat_bledu=''
        #print('komunikat_bledu wyzerowany')
        return True

    def wez_z_listy_zadan(self):
        "daje kolejne z listy zadan i w razie potrzeby uzupełnia ją(od końca)"
        if len(self.lista_zadan)==0:
            self.zrob_liste_zadan()

        return self.lista_zadan.pop()  #przypominam że pop można dać indeks

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

    def wylosuj_ulice_z_inkrem(self):
        '''
        wylosuj takie jak biezacy_tryb
        jak lista pusta lub brak ulic z bieżacym trybem zwraca False.
        powienien zwrócić typ WpisUlica

        inkrementacja ilości wylosowanych ulic
        '''
        if len(self.lista_slowek)==0:
            return False

        najrzadsze=self.jaki_najrzadziej_ulica()
        if najrzadsze is False:
            return False

        lista_najrzadszych=[]

        for ulica in self.lista_ulic:
            if ulica.ile_razy_wylos==najrzadsze and ulica.tryb==self.biezacy_tryb:
                lista_najrzadszych.append(ulica)

        wylosowane=RA.choice(lista_najrzadszych)
        #print('wylosowane',wylosowane)

        #inkrem:
        for wpisy in self.lista_ulic:
            if wpisy==wylosowane:
                wpisy.ile_razy_wylos+=1
                break

        self.stats.kolejna_ulica()
        #print('po',self.lista_ulic)
        return wylosowane

    def wylosuj_slowko_z_inkrem(self):
        '''
        wylosuj takie jak biezacy_tryb
        jak lista pusta lub brak słówek z bieżacym trybem zwraca False.
        powienien zwrócić typ WpisSlowko

        inkrementacja ilości wylosowanych słówek
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

        for slowko in self.lista_slowek:
            if slowko.ile_razy_wylos==najrzadsze and slowko.tryb==self.biezacy_tryb:
                #print('slowko',slowko)
                lista_najrzadszych.append(slowko)

        wylosowane=RA.choice(lista_najrzadszych)
        #print('wylosowane',wylosowane)

        #inkrem:
        for slowko in self.lista_slowek:
            if slowko==wylosowane:
                slowko.ile_razy_wylos+=1
                break

        self.stats.kolejne_slowko()
        #print('po',self.lista_slowek)
        return wylosowane

    def zeruj_ilosc_wylosowan_ulic(self):
        "wszystkie ulice ustawia ile_razy_wylos=0"
        for wpis in self.lista_ulic:
            wpis.ile_razy_wylos=0

    def zeruj_tryb_ulic(self):
        "wszystkie ulice ustawia tryb A"
        for wpis in self.lista_ulic:
            wpis.tryb='A'

    def zeruj_ilosc_wylosowan_slowek(self):
        "wszystkie slowka ustawia ile_razy_wylos=0"
        for wpis in self.lista_slowek:
            wpis.ile_razy_wylos=0

    def zeruj_tryb_slowek(self):
        "wszystkie ulice ustawia tryb A"
        for wpis in self.lista_slowek:
            wpis.tryb='A'

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
        jak przydziela nowy tryb to zeruje ile_razy_wylos
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
        "dla bieżącego wpisu dekrementuj ile_razy_wylos w self.lista_slowek/lista_ulic"

        if type(self.biezacy_wpis) is KWS:
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


    def eksportuj_jako_pdf(self,dane_bazowe_lista,dane_bazowe_nazwa,plik_wynikowy_pdf):
        '''
        jedna funkcja do ulic i słówek.
        są watpliwości jak zmieścić zbyt długie wpisy w pdfie.
        narazie przycina do pewnej długości, a jak będzie lepszy pomysł to poprawie.
        '''
        def ilosci_do_tworzenia_pdfa():
            ""
            ile_wpisow_na_stronie=int((ilosci['gorny_y']-ilosci['dolny_y'])/ilosci['krok_y'])
            ile_wpisow_jest=len(dane_bazowe_lista)
            ilosc_stron_bedzie=0

            if ile_wpisow_jest%ile_wpisow_na_stronie==0:
                ilosc_stron_bedzie=int(ile_wpisow_jest/ile_wpisow_na_stronie)
            else:
                ilosc_stron_bedzie=int(ile_wpisow_jest/ile_wpisow_na_stronie)+1
            return ile_wpisow_jest,ilosc_stron_bedzie,ile_wpisow_na_stronie

        def naglowek_zrob(dane_bazowe_nazwa):
            ""
            plotno.setFont("DejaVuSans",25)
            plotno.setTitle(dane_bazowe_nazwa)
            plotno.line(30,810,500,810)
            plotno.setFillColorRGB(0,0,255)
            plotno.drawCentredString(290,770,'--- '+dane_bazowe_nazwa+' ---')
            plotno.line(30,750,500,750)
            plotno.drawInlineImage('logo.png',510,750,width=60, height=60)

        def stopke_zrob(ktora_strona):
            ""
            plotno.setFillColorRGB(0,0,0)
            plotno.setFont("DejaVuSans",13)
            plotno.drawCentredString(290,30,"strona "+str(ktora_strona))
            plotno.line(30,50,560,50)

        def wstaw_wpisy_na_strone(indeks_pocz,indeks_konc):
            ""
            plotno.setFillColorRGB(0,0,0)
            plotno.setFont("DejaVuSans",15)
            ile_od_gory_wstawic=indeks_konc-indeks_pocz+1

            for ktory_wpis,jaki_y in zip(range(0,ile_od_gory_wstawic),
                range(ilosci['gorny_y'],ilosci['dolny_y'],-ilosci['krok_y'])):
                indeks_wpisu=indeks_pocz+ktory_wpis

                if jaki_typ is KW.WpisUlica:
                    linia_do_wstawienia=str(dane_bazowe_lista[indeks_wpisu].pierwszy)
                    plotno.drawCentredString(300,jaki_y,linia_do_wstawienia)
                else:
                    linia_do_wstawienia1=str(dane_bazowe_lista[indeks_wpisu].pierwszy)
                    linia_do_wstawienia2=str(dane_bazowe_lista[indeks_wpisu].drugi)

                    if len(linia_do_wstawienia1)>=29:
                        linia_do_wstawienia1=linia_do_wstawienia1[:27]+'...'
                    if len(linia_do_wstawienia2)>=30:
                        linia_do_wstawienia2=linia_do_wstawienia2[:28]+'...'

                    plotno.drawString(30,jaki_y,linia_do_wstawienia1)
                    plotno.drawString(295,jaki_y,linia_do_wstawienia2)

        #poczatek f. eksportuj_jako_pdf
        if len(dane_bazowe_lista)==0:
            return 'pusta lista wpisów'
        jaki_typ=type(dane_bazowe_lista[0])

        czcionka_ttf={'nazwa':'DejaVuSans','sciezka':'DejaVuSans-Bold.ttf'}
        RL_MET.registerFont(RL_TTF.TTFont(czcionka_ttf['nazwa'],czcionka_ttf['sciezka']))

        if not OS.path.exists(czcionka_ttf['sciezka']):
            return 'brakuje pliku czcionki: '+czcionka_ttf['sciezka']

        plotno=RL_CAN.Canvas(plik_wynikowy_pdf,pagesize=RL_ROZ.A4)
        plotno.setFont(czcionka_ttf['nazwa'],15)

        ilosci={'gorny_y':700,'dolny_y':50,'krok_y':40}
        ile_wpisow_jest,ile_stron_bedzie,ile_wpisow_na_stronie=ilosci_do_tworzenia_pdfa()

        for strona in range(0,ile_stron_bedzie):
            indeks_pocz=strona*ile_wpisow_na_stronie
            indeks_konc=(strona+1)*ile_wpisow_na_stronie-1
            if indeks_konc>ile_wpisow_jest:
                indeks_konc=ile_wpisow_jest-1

            naglowek_zrob(dane_bazowe_nazwa)
            wstaw_wpisy_na_strone(indeks_pocz,indeks_konc)
            stopke_zrob(strona+1)
            plotno.showPage()

        plotno.save()
        print('--- wygenerowałem plik: '+plik_wynikowy_pdf+' ---')
        return True
        #koniec f.eksportuj_jako_pdf


    #CRUD. ale kolejność od samodzielnych po zależne
    def czy_wpis_istnieje(self,jaki_wpis):
        '''
        sprawdza typ wpisu i sprawdza obecność w pierwszy/drugi
            przy pomocy == czyli konieczne ścisłe dopasowanie
        zwraca True jak istnieje taki lub False jak nie ma takiego
        '''
        if not isinstance(jaki_wpis,KWU):
            #jeden warunek obejmuje bazową i pochodną
            raise TypeError('czy_wpis_istnieje. typ=',type(jaki_wpis))

        if type(jaki_wpis) is KWU:
            #ten warunek jest do ulicy tylko
            return jaki_wpis in self.lista_ulic

        return jaki_wpis in self.lista_slowek

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
        if not szukany_str:
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
        if not isinstance(nowy_wpis,KWU):
            #sprawdzenie obejmuje oba typy
            raise TypeError('dodać można Wpis a nie',type(nowy_wpis))

        czy_jest_taki=self.czy_wpis_istnieje(nowy_wpis)
        if czy_jest_taki:
            return False

        if type(nowy_wpis) is KWS:
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
        if not isinstance(nowy_wpis,KWU):
            #jeden warunek obejmuję klasę bazową i pochodną
            raise TypeError('zmien_wpis typy=',type(stary_wpis),type(nowy_wpis))

        if type(stary_wpis) is not type(nowy_wpis):
            raise TypeError("nieuprawniona zmiana typu wpisu")

        if self.czy_wpis_istnieje(stary_wpis) and not self.czy_wpis_istnieje(nowy_wpis):
            if type(stary_wpis) is KWS:
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
        if not isinstance(do_kasow_wpis,KWU):
            #jeden warunek 2 klasy Wpis
            raise TypeError('kasować można Wpis a nie',type(do_kasow_wpis))

        if type(do_kasow_wpis) is KWS:
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
        return [self.plik_ulice,self.plik_slowka,self.biezacy_tryb,self.procent_slowek_reszta_ulic]

if __name__=='__main__':
    print('---są testy do tej klasy---')
