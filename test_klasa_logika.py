#!/usr/bin/python3.9
import unittest as UT
import random as RA
import os as OS
import copy as CO
import numpy as NP
import klasa_wpis_ulica_wpis_slowko as KW
import klasa_logika as KL

class TestKlasaLogika(UT.TestCase):
    ""
    def setUp(self):
        ""
        ust_log=['test_slowka.nauka','test_ulice.nauka','A',50]
        self.logika=KL.Logika(ust_log)

        self.wpis_zmyslonyS=KW.WpisSlowko("pankracy is a brick","pankracy to równy gość")
        self.wpis_dokladnyS=self.logika.lista_slowek[0]
        #częściowy ale o długości +3
        self.wpis_czesciowyS=KW.WpisSlowko("agil","zręczny","B",1)
        self.wpis1S=KW.WpisSlowko("next to","obok","B",2)
        self.wpis2S=KW.WpisSlowko("filozof","philosopher","B",2)

        self.wpis_zmyslonyU=KW.WpisUlica("różowa")
        self.wpis_dokladnyU=KW.WpisUlica("Krakowska")
        self.wpis_czesciowyU=KW.WpisUlica("górska")

    def tearDown(self):
        pass

    def test_init_zle_dane(self):
        "błędne argumenty klasy Logika powinny zgłosić wyjątek z dekoratora"
        with self.assertRaises(ValueError):
            ust_1=['test_slowka.nauka','test_ulice.nauka','A',111]
            self.logika=KL.Logika(ust_1)
            ust_2=['test_slowka.nauka','','A',111]
            self.logika=KL.Logika(ust_2)
            ust_3=['','','A',111]
            self.logika=KL.Logika(ust_3)
            ust_4=['djdjd','fijrie','r',111]
            self.logika=KL.Logika(ust_4)
            ust_5=[]
            self.logika=KL.Logika(ust_5)

    def test_init_poprawne_dane(self):
        "czy typy sie zgadzają + wartości"
        self.assertIsInstance(self.logika.plik_slowka,str)
        self.assertNotEqual(self.logika.plik_slowka,'')

        self.assertIsInstance(self.logika.plik_ulice,str)
        self.assertNotEqual(self.logika.plik_ulice,'')

        self.assertIsInstance(self.logika.biezacy_tryb,str)
        self.assertTrue(self.logika.biezacy_tryb in ['A','B','C'])

        self.assertIsInstance(self.logika.procent_slowek_reszta_ulic,int)
        self.assertTrue(0<=self.logika.procent_slowek_reszta_ulic<=100)

    def sprawdz_typy_z_listy_slowek(self):
        ""
        self.assertNotEqual(len(self.logika.lista_slowek),0,msg="chyba że plik slowka pusty")

        for slowko in self.logika.lista_slowek:
            self.assertIsInstance(slowko,KW.WpisSlowko)
        return True

    def sprawdz_typy_z_listy_ulic(self):
        ""
        self.assertNotEqual(len(self.logika.lista_ulic),0,msg="chyba że plik ulice pusty")

        for slowko in self.logika.lista_ulic:
            self.assertIsInstance(slowko,KW.WpisUlica)
        return True

    def test_wczytaj_slowka(self):
        "czy tworzy lista_slowek,ktorej elementy sa klasy WpisSlowko"

        self.assertTrue(self.sprawdz_typy_z_listy_slowek())

    def test_wczytaj_ulice(self):
        "czy tworzy lista_ulic, ktorej elementy są klasy WpisUlica"

        self.assertTrue(self.sprawdz_typy_z_listy_ulic())

    def test_zapisz_slowka(self):
        '''
        przed wywołaniem sprawdza:
            czy lista_slowek niepusta
            czy lista_slowek jest listą typu WpisSlowko
        po wywołaniu sprawdza:
            czy plik_slowka niepusty
        '''
        self.assertTrue(self.sprawdz_typy_z_listy_slowek())

        self.logika.zapisz_slowka()

        jaki_plik=self.logika.plik_slowka
        rozmiar_pliku=OS.stat(jaki_plik).st_size
        self.assertNotEqual(rozmiar_pliku,0)

    def test_zapisz_ulice(self):
        '''
        przed wywołaniem sprawdza:
            czy lista_ulic niepusty
            czy lista_ulic lista typu WpisUlica
        po wywołaniu sprawdza:
            czy plik_ulice niepusty
        '''
        self.assertTrue(self.sprawdz_typy_z_listy_ulic())

        self.logika.zapisz_ulice()

        jaki_plik=self.logika.plik_ulice
        rozmiar_pliku=OS.stat(jaki_plik).st_size

        self.assertNotEqual(rozmiar_pliku,0)

    def test_czy_sa_slowka_w_trybie(self):
        '''
        ponieważ tryb się zmienia w trakcie programu
        trzeba odnowić liste_zadan żeby niebyło dziur
        w wynikach losowania
        '''
        self.logika.ustaw_biezacy_tryb('A') #są
        wynik1=self.logika.czy_sa_slowka_w_trybie()
        self.assertTrue(wynik1)

        self.logika.ustaw_biezacy_tryb('B') #są
        wynik2=self.logika.czy_sa_slowka_w_trybie()
        self.assertTrue(wynik2)

        self.logika.ustaw_biezacy_tryb('C') #brak
        wynik3=self.logika.czy_sa_slowka_w_trybie()
        self.assertFalse(wynik3)

    def test_czy_sa_ulice_w_trybie(self):
        '''
        ponieważ tryb się zmienia w trakcie programu
        trzeba odnowić liste_zadan żeby niebyło dziur
        w wynikach losowania
        '''
        self.logika.ustaw_biezacy_tryb('A') #są
        wynik1=self.logika.czy_sa_ulice_w_trybie()
        self.assertTrue(wynik1)

        self.logika.ustaw_biezacy_tryb('B') #brak
        wynik2=self.logika.czy_sa_ulice_w_trybie()
        self.assertFalse(wynik2)

        self.logika.ustaw_biezacy_tryb('C') #jedno
        wynik3=self.logika.czy_sa_ulice_w_trybie()
        self.assertTrue(wynik3)

    def test_zrob_liste_zadan(self):
        '''
        czy self.lista_zadan jest listą niepustą
        3przypadki:
            są tylko słówka w plikach
            są tylko ulice w plikach
            w plikach są słówka i ulice(wtedy procent_slowek_reszta_ulic stosuje)
        '''
        def sprawdz_dla_trybu(czy_obecne_slowka,czy_obecne_ulice):
            self.logika.zrob_liste_zadan()
            #print('lista_zadan',self.logika.biezacy_tryb,self.logika.lista_zadan)
            self.assertNotEqual(len(self.logika.lista_zadan),0)
            obecne_slowka=False
            obecne_ulice=False

            for rodzaj in self.logika.lista_zadan:
                #print('rodzaj',self.logika.biezacy_tryb,rodzaj)
                if obecne_slowka is False and rodzaj=='s1':
                    obecne_slowka=True
                if obecne_ulice is False and rodzaj=='u':
                    obecne_ulice=True

                self.assertTrue(rodzaj in ['s1','u'])
            #czy w danym trybie są ulica i słówka
            if czy_obecne_slowka:
                self.assertTrue(obecne_slowka)
            else:
                self.assertFalse(obecne_slowka)
            if czy_obecne_ulice:
                self.assertTrue(obecne_ulice)
            else:
                self.assertFalse(obecne_ulice)

            if czy_obecne_slowka and czy_obecne_ulice:
                #policz ile_slowek względem procent_slowek_reszta_ulic
                procent_slowek=self.logika.procent_slowek_reszta_ulic
                rozm_listy_zadan=len(self.logika.lista_zadan)

                ile_slowek_znalazl=self.logika.lista_zadan.count('s1')
                ile_slowek_powinno_byc=int(rozm_listy_zadan*procent_slowek/100)
                self.assertEqual(ile_slowek_znalazl,ile_slowek_powinno_byc)

                ile_ulic_znalazl=self.logika.lista_zadan.count('u')
                ile_ulic_powinno_byc=rozm_listy_zadan-int(rozm_listy_zadan*procent_slowek/100)
                self.assertEqual(ile_ulic_znalazl,ile_ulic_powinno_byc)


        self.logika.ustaw_biezacy_tryb('A') #są słówka i ulice czyli proporcje sprawdz
        sprawdz_dla_trybu(True,True)

        self.logika.ustaw_biezacy_tryb('B') #są tylko słówka
        sprawdz_dla_trybu(True,False)

        self.logika.ustaw_biezacy_tryb('C') #są tylko ulice
        sprawdz_dla_trybu(False,True)


    def test_wez_z_listy_zadan(self):
        '''
        ta funkcja wybiera z lista_zadan a jak sie skoncza to wywoluje zrob_liste_zadan
        '''
        for _ in range(100):
            wynik=self.logika.wez_z_listy_zadan()
            self.assertTrue(wynik in ['u','s1'])

    def test_jaki_najrzadziej_slowko(self):
        "bierze pod uwagę biezacy_tryb"

        self.logika.ustaw_biezacy_tryb('A') #słówko:0
        self.assertTrue(self.logika.biezacy_tryb=='A')
        wynik_a=self.logika.jaki_najrzadziej_slowko()
        #print('biezacyA=',self.logika.biezacy_tryb)
        #print('wynik_a',wynik_a)
        self.assertTrue(wynik_a==0)

        self.logika.ustaw_biezacy_tryb('B') #słówko:2
        self.assertTrue(self.logika.biezacy_tryb=='B')
        #print('biezacyB=',self.logika.biezacy_tryb)
        wynik_b=self.logika.jaki_najrzadziej_slowko()
        #print('wynik_b',wynik_b)
        self.assertTrue(wynik_b==2)

        self.logika.ustaw_biezacy_tryb('C') #słówko brak
        self.assertTrue(self.logika.biezacy_tryb=='C')
        #print('biezacyC=',self.logika.biezacy_tryb)
        wynik_c=self.logika.jaki_najrzadziej_slowko()
        #print('wynik_c',wynik_c)
        self.assertFalse(wynik_c)

        #daj tryb A na koniec testu
        self.logika.zmien_biezacy_tryb()
        self.assertTrue(self.logika.biezacy_tryb=='A')

    def test_jaki_najrzadziej_ulica(self):
        "bierze pod uwagę biezacy_tryb"
        self.assertTrue(self.logika.biezacy_tryb=='A')
        wynik_a=self.logika.jaki_najrzadziej_ulica()
        #print('UbiezacyA=',self.logika.biezacy_tryb)
        #print('Uwynik_a',wynik_a)
        self.assertEqual(wynik_a,0)

        #daj tryb na B:
        self.logika.zmien_biezacy_tryb()
        self.assertTrue(self.logika.biezacy_tryb=='B')
        #print('UbiezacyB=',self.logika.biezacy_tryb)
        wynik_b=self.logika.jaki_najrzadziej_ulica()
        #print('Uwynik_b',wynik_b)
        self.assertFalse(wynik_b)

        #daj tryb na C:
        self.logika.zmien_biezacy_tryb()
        self.assertTrue(self.logika.biezacy_tryb=='C')
        #print('UbiezacyC=',self.logika.biezacy_tryb)
        wynik_c=self.logika.jaki_najrzadziej_ulica()
        #print('Uwynik_c',wynik_c)
        self.assertEqual(wynik_c,4)

        #daj tryb A na koniec testu
        self.logika.zmien_biezacy_tryb()
        self.assertTrue(self.logika.biezacy_tryb=='A')

    def rozpoznaj_inkrementacje_ilosci_wylos_ulic(self,stara_lista,nowa_lista):
        ""
        for sta,now in zip(stara_lista,nowa_lista):
            if sta!=now:
                self.assertEqual(sta.pierwszy,now.pierwszy)
                self.assertEqual(sta.tryb,now.tryb)
                self.assertEqual(sta.ile_razy_wylos+1,now.ile_razy_wylos)

        self.assertNotEqual(stara_lista,nowa_lista)
        return True

    def rozpoznaj_inkrementacje_ilosci_wylos_slowek(self,stara_lista,nowa_lista):
        ""
        for sta,now in zip(stara_lista,nowa_lista):
            if sta!=now:
                self.assertEqual(sta.pierwszy,now.pierwszy)
                self.assertEqual(sta.drugi,now.drugi)
                self.assertEqual(sta.tryb,now.tryb)
                self.assertEqual(sta.ile_razy_wylos+1,now.ile_razy_wylos)

        self.assertNotEqual(stara_lista,nowa_lista)
        return True

    def test_wylosuj_slowko_z_inkrem_tryb_A(self):
        '''
        tylko tryb A
        '''
        #daj tryb na A
        self.logika.ustaw_biezacy_tryb('A')

        stara=CO.deepcopy(self.logika.lista_slowek)
        #print('\nSstaraA',stara,id(stara))

        wylosowane=self.logika.wylosuj_slowko_z_inkrem()
        #print('SwylosowaneA',wylosowane)
        #bo w test_slowka.nauka są słówka A
        self.assertIsInstance(wylosowane,KW.WpisSlowko)
        self.assertEqual(wylosowane.tryb,'A')

        nowa=self.logika.lista_slowek
        #print('SnowaA',nowa,id(nowa))
        self.assertTrue(self.rozpoznaj_inkrementacje_ilosci_wylos_slowek(stara,nowa))



    def test_wylosuj_slowko_z_inkrem_tryb_B(self):
        "tylko tryb B"
        #daj tryb na B
        self.logika.ustaw_biezacy_tryb('B')

        stara=CO.deepcopy(self.logika.lista_slowek)
        #print('\nstaraB',stara,id(stara))

        wylosowane=self.logika.wylosuj_slowko_z_inkrem()
        #print('wylosowaneB',wylosowane)
        #bo w test_slowka.nauka są słówka A
        self.assertIsInstance(wylosowane,KW.WpisSlowko)
        self.assertEqual(wylosowane.tryb,'B')

        nowa=self.logika.lista_slowek
        #print('nowaB',nowa,id(nowa))
        self.assertTrue(self.rozpoznaj_inkrementacje_ilosci_wylos_slowek(stara,nowa))


    def test_wylosuj_slowko_z_inkrem_tryb_C(self):
        "tylko tryb C"
        #daj tryb na C
        self.logika.ustaw_biezacy_tryb('C')

        stara=CO.deepcopy(self.logika.lista_slowek)
        #print('\nstaraC',stara,id(stara))

        wylosowane=self.logika.wylosuj_slowko_z_inkrem()
        #print('wylosowaneC',wylosowane)
        #bo w test_slowka.nauka brak słówek C
        self.assertFalse(wylosowane)

        nowa=self.logika.lista_slowek
        #print('nowaC',nowa,id(nowa))

        self.assertEqual(stara,nowa)

    def test_wylosuj_ulice_z_inkrem_tryb_A(self):
        '''
        tylko tryb A
        '''
        #daj tryb na A
        self.logika.ustaw_biezacy_tryb('A')
        stara=CO.deepcopy(self.logika.lista_ulic)
        #print('\nUstaraA',stara,id(stara))

        wylosowane=self.logika.wylosuj_ulice_z_inkrem()
        #print('UwylosowaneA',wylosowane)
        self.assertTrue(wylosowane)

        nowa=self.logika.lista_ulic
        #print('nowa ',nowa,id(nowa))
        self.assertTrue(self.rozpoznaj_inkrementacje_ilosci_wylos_ulic(stara,nowa))

    def test_wylosuj_ulice_z_inkrem_tryb_B(self):
        '''
        tylko tryb B. brak takich ulic
        '''
        #daj tryb na B
        self.logika.ustaw_biezacy_tryb('B')
        stara=CO.deepcopy(self.logika.lista_ulic)
        #print('\nUstaraB',stara,id(stara))

        wylosowane=self.logika.wylosuj_ulice_z_inkrem()
        #print('UwylosowaneB',wylosowane)
        self.assertFalse(wylosowane)

        nowa=self.logika.lista_ulic
        #print('nowa ',nowa,id(nowa))
        self.assertEqual(stara,nowa)

    def test_wylosuj_ulice_z_inkrem_tryb_C(self):
        '''
        tylko tryb C. jest jedna ulica
        '''
        #daj tryb na C
        self.logika.ustaw_biezacy_tryb('C')
        stara=CO.deepcopy(self.logika.lista_ulic)
        #print('\nUstaraC',stara,id(stara))

        wylosowane=self.logika.wylosuj_ulice_z_inkrem()
        #print('UwylosowaneC',wylosowane)
        self.assertIsInstance(wylosowane,KW.WpisUlica)
        self.assertEqual(wylosowane.tryb,'C')

        nowa=self.logika.lista_ulic
        #print('nowa ',nowa,id(nowa))
        self.assertTrue(self.rozpoznaj_inkrementacje_ilosci_wylos_ulic(stara,nowa))

    def test_ustaw_biezacy_tryb(self):
        "druga f.do zmiany trybu"

        wyn_a=self.logika.ustaw_biezacy_tryb('A')
        self.assertEqual(self.logika.biezacy_tryb,'A')
        self.assertEqual(wyn_a,'A')

        wyn_b=self.logika.ustaw_biezacy_tryb('B')
        self.assertEqual(self.logika.biezacy_tryb,'B')
        self.assertEqual(wyn_b,'B')

        wyn_c=self.logika.ustaw_biezacy_tryb('C')
        self.assertEqual(self.logika.biezacy_tryb,'C')
        self.assertEqual(wyn_c,'C')

        with self.assertRaises(ValueError):
            self.logika.ustaw_biezacy_tryb(1)
            self.logika.ustaw_biezacy_tryb('G')

    def test_zmien_biezacy_tryb(self):
        ""
        self.logika.biezacy_tryb='A'
        self.logika.zmien_biezacy_tryb()
        self.assertTrue(self.logika.biezacy_tryb,'B')

        self.logika.biezacy_tryb='B'
        self.logika.zmien_biezacy_tryb()
        self.assertTrue(self.logika.biezacy_tryb,'C')

        self.logika.biezacy_tryb='C'
        self.logika.zmien_biezacy_tryb()
        self.assertTrue(self.logika.biezacy_tryb,'A')

        #dla nastepnych zeby bylo:
        self.logika.biezacy_tryb='A'

    def test_ustaw_tryb_biezacego_wpisu_slowko(self):
        '''
        zwraca True jak sie udalo
        False jak nie
        '''
        #zły typ powinien dać wyjątek
        with self.assertRaises(ValueError):
            self.logika.ustaw_tryb_biezacego_wpisu('G')

        #inicjalizacja biezacego wpisu
        self.logika.biezacy_wpis=RA.choice(self.logika.lista_slowek)
        #print('1biezacy',self.logika.biezacy_wpis)

        #teraz zmieniam tryb dla biezacego: daje na nastepny(A->B,B->C,C->A)
        if self.logika.biezacy_wpis.tryb=='A':
            self.logika.ustaw_tryb_biezacego_wpisu('B')
            self.assertEqual(self.logika.biezacy_wpis.tryb,'B')
        elif self.logika.biezacy_wpis.tryb=='B':
            self.logika.ustaw_tryb_biezacego_wpisu('C')
            self.assertEqual(self.logika.biezacy_wpis.tryb,'C')
        else:
            self.logika.ustaw_tryb_biezacego_wpisu('A')
            self.assertEqual(self.logika.biezacy_wpis.tryb,'A')


    def test_ustaw_tryb_biezacego_wpisu_ulica(self):
        '''
        zwraca True jak sie udalo
        False jak nie
        '''
        #zły typ powinien dać wyjątek
        with self.assertRaises(ValueError):
            self.logika.ustaw_tryb_biezacego_wpisu('G')

        #inicjalizacja biezacego wpisu
        self.logika.biezacy_wpis=RA.choice(self.logika.lista_ulic)
        #print('1biezacy',self.logika.biezacy_wpis)

        #teraz zmieniam tryb dla biezacego: daje na nastepny(A->B,B->C,C->A)
        if self.logika.biezacy_wpis.tryb=='A':
            self.logika.ustaw_tryb_biezacego_wpisu('B')
            self.assertEqual(self.logika.biezacy_wpis.tryb,'B')
        elif self.logika.biezacy_wpis.tryb=='B':
            self.logika.ustaw_tryb_biezacego_wpisu('C')
            self.assertEqual(self.logika.biezacy_wpis.tryb,'C')
        else:
            self.logika.ustaw_tryb_biezacego_wpisu('A')
            self.assertEqual(self.logika.biezacy_wpis.tryb,'A')


    def test_cofnij_ilosc_wylos_biez_wpisu_slowko(self):
        "w tej wersji biezacy A"
        self.logika.biezacy_wpis=RA.choice(self.logika.lista_slowek)
        stara_lista=CO.deepcopy(self.logika.lista_slowek)

        self.logika.cofnij_ilosc_wylos_biez_wpisu_lo()

        nowa_lista=self.logika.lista_slowek
        ind_rob_wpisu=self.logika.lista_slowek.index(self.logika.biezacy_wpis)
        #print('ind_rob_wpisu',ind_rob_wpisu)
        wieksze=stara_lista[ind_rob_wpisu].ile_razy_wylos
        mniejsze=nowa_lista[ind_rob_wpisu].ile_razy_wylos
        #print('w',wieksze,'m',mniejsze)

        if wieksze==0:
            self.assertEqual(wieksze,mniejsze)
        else:
            self.assertEqual(mniejsze+1,wieksze)


    def test_cofnij_ilosc_wylos_biez_wpisu_ulica(self):
        "w tej wersji testu losuje biezacy_wpis"
        self.logika.biezacy_wpis=RA.choice(self.logika.lista_ulic)
        stara_lista=CO.deepcopy(self.logika.lista_ulic)

        self.logika.cofnij_ilosc_wylos_biez_wpisu_lo()

        nowa_lista=self.logika.lista_ulic
        ind_rob_wpisu=self.logika.lista_ulic.index(self.logika.biezacy_wpis)
        #print('ind_rob_wpisu',ind_rob_wpisu)
        wieksze=stara_lista[ind_rob_wpisu].ile_razy_wylos
        mniejsze=nowa_lista[ind_rob_wpisu].ile_razy_wylos
        #print('w',wieksze,'m',mniejsze)

        if wieksze==0:
            self.assertEqual(wieksze,mniejsze)
        else:
            self.assertEqual(mniejsze+1,wieksze)



    #najpierw samodzielne funkcje edytujace
    def test_czy_wpis_istnieje_slowko(self):
        ""
        #zmyślony wpis
        wynik1=self.logika.czy_wpis_istnieje(self.wpis_zmyslonyS)
        self.assertFalse(wynik1)

        #istniejacy wpis
        wynik2=self.logika.czy_wpis_istnieje(self.wpis_dokladnyS)
        self.assertTrue(wynik2)

        #częsciowy wpis
        wynik3=self.logika.czy_wpis_istnieje(self.wpis_czesciowyS)
        self.assertFalse(wynik3)

    def test_czy_wpis_istnieje_ulica(self):
        ""
        #zmyślony wpis
        wynik1=self.logika.czy_wpis_istnieje(self.wpis_zmyslonyU)
        self.assertFalse(wynik1)

        #istniejacy wpis
        wynik2=self.logika.czy_wpis_istnieje(self.wpis_dokladnyU)
        self.assertTrue(wynik2)

        #częsciowy wpis
        wynik3=self.logika.czy_wpis_istnieje(self.wpis_czesciowyU)
        self.assertFalse(wynik3)


    def test_szukaj_wpis_slowko(self):
        ""
        #zmyślone
        wynik1=self.logika.szukaj_wpis("zmyślony",typ='s')
        #print('wynik1',wynik1)
        self.assertFalse(wynik1)

        #istniejacy
        wynik2=self.logika.szukaj_wpis(self.wpis_dokladnyS.drugi,typ='s')
        #print('wynik2',wynik2)
        self.assertIsInstance(wynik2,KW.WpisSlowko)

        #częściowy powinien się udać(dać klase Wpis)
        wynik3=self.logika.szukaj_wpis(self.wpis_czesciowyS.drugi,typ='s')
        #print('wynik3',wynik3)
        self.assertIsInstance(wynik3,KW.WpisSlowko)

        #za krótki
        wynik4=self.logika.szukaj_wpis("dw",typ='s')
        #print('wynik4',wynik4)
        self.assertFalse(wynik4)

    def test_szukaj_wpis_ulica(self):
        ""
        #zmyślone
        wynik1=self.logika.szukaj_wpis("zmyślony",typ='u')
        #print('wynik1',wynik1)
        self.assertFalse(wynik1)

        #istniejacy
        #wynik2=self.logika.szukaj_wpis(self.wpis_dokladnyU.pierwszy,typ='u')
        #print('wynik2',wynik2)
        #self.assertIsInstance(wynik2,KW.WpisUlica)

        #częściowy powinien się udać(dać klase Wpis)
        '''wynik3=self.logika.szukaj_wpis(self.wpis_czesciowyU.drugi,typ='u')
        #print('wynik3',wynik3)
        self.assertIsInstance(wynik3,KW.WpisUlica)

        #za krótki
        wynik4=self.logika.szukaj_wpis("dw",typ='u')
        #print('wynik4',wynik4)
        self.assertEqual(wynik4,False)'''

    def test_dodaj_wpis_slowko(self):
        ""
        #zmyślony (czyli przejdzie)
        wynik1=self.logika.dodaj_wpis(self.wpis_zmyslonyS)
        #print('wynik1',wynik1)
        self.assertTrue(wynik1)

        #istniejacy czyli nieuda się
        wynik2=self.logika.dodaj_wpis(self.wpis_zmyslonyS)
        #print('wynik2',wynik2)
        self.assertFalse(wynik2)

        #proba wstawienia str-a
        with self.assertRaises(TypeError):
            self.logika.dodaj_wpis("prowokacja")

    def test_dodaj_wpis_ulica(self):
        ""
        #zmyślony (czyli przejdzie)
        wynik1=self.logika.dodaj_wpis(self.wpis_zmyslonyU)
        #print('wynik1',wynik1)
        self.assertTrue(wynik1)

        #istniejacy czyli nieuda się
        wynik2=self.logika.dodaj_wpis(self.wpis_zmyslonyU)
        #print('wynik2',wynik2)
        self.assertFalse(wynik2)

        #proba wstawienia str-a
        with self.assertRaises(TypeError):
            self.logika.dodaj_wpis("prowokacja")

    def test_zmien_wpis_slowko(self):
        ""

        #podmieniam na nowy/nieistniejacy
        stary1=CO.deepcopy(self.logika.lista_slowek[1])
        #print('stary1',stary1)
        nowy1=KW.WpisSlowko("cdr","3er","A",3)
        #print('nowy1',nowy1)
        wynik1=self.logika.zmien_wpis(stary1,nowy1)
        #print('wynik1',wynik1)
        self.assertTrue(wynik1)
        #print('po zamianie',self.logika.lista_slowek)

        #proba zamiany na juz istniejacy na liscie
        stary2=self.logika.lista_slowek[1]
        #print('stary2',stary2)
        nowy2=self.logika.lista_slowek[0]
        #print('nowy2',nowy2)
        wynik2=self.logika.zmien_wpis(stary2,nowy2)
        #print('wynik2',wynik2)
        self.assertFalse(wynik2)

        #proba podmiany na str-a 
        with self.assertRaises(TypeError):
            stary3=self.logika.lista_slowek[0]
            nowy3="może się uda"
            self.logika.zmien_wpis(stary3,nowy3)

    def test_zmien_wpis_ulica(self):
        ""

        #podmieniam na nowy/nieistniejacy
        stare_ulice=CO.deepcopy(self.logika.lista_ulic)
        stary1=CO.deepcopy(self.logika.lista_ulic[1])
        #print('stary1',stary1)
        nowy1=KW.WpisUlica("cdr","A",3)
        #print('nowy1',nowy1)
        wynik1=self.logika.zmien_wpis(stary1,nowy1)
        #print('wynik1',wynik1)
        self.assertTrue(wynik1)
        nowe_ulice=self.logika.lista_ulic
        self.assertEqual(len(stare_ulice),len(nowe_ulice))
        #print('po zamianie',self.logika.lista_ulic)

        #proba zamiany na juz istniejacy na liscie
        stary2=self.logika.lista_ulic[1]
        #print('stary2',stary2)
        nowy2=self.logika.lista_ulic[0]
        #print('nowy2',nowy2)
        wynik2=self.logika.zmien_wpis(stary2,nowy2)
        #print('wynik2',wynik2)
        self.assertFalse(wynik2)

        #proba podmiany na str-a 
        with self.assertRaises(TypeError):
            stary3=self.logika.lista_ulic[0]
            nowy3="może się uda"
            self.logika.zmien_wpis(stary3,nowy3)

    def test_kasuj_wpis_slowko(self):
        ""
        #print('R=',len(self.logika.lista_slowek))
        #kasowanie istniejacego
        stare_slowka=CO.deepcopy(self.logika.lista_slowek)
        #print('stare_slowka',stare_slowka)
        wynik1=self.logika.kasuj_wpis(self.logika.lista_slowek[1])
        self.assertTrue(wynik1)
        nowe_slowka=self.logika.lista_slowek
        #print('nowe_slowka',nowe_slowka)
        self.assertEqual(len(stare_slowka)-1,len(nowe_slowka))

        #kasowanie nieistniejacego
        nieistniejacy=KW.WpisSlowko("piłka","ball")
        wynik2=self.logika.kasuj_wpis(nieistniejacy)
        self.assertFalse(wynik2)

        #zly typ do skasowania
        with self.assertRaises(TypeError):
            self.logika.kasuj_wpis("Krystyna")

    def test_kasuj_wpis_ulica(self):
        "kasuj: istniejacy,nieistniejacy i zły typ do skasowanie"

        #kasowanie istniejacego
        stare_ulice=CO.deepcopy(self.logika.lista_ulic)
        #print('\nstare_ulice',stare_ulice)
        wynik1=self.logika.kasuj_wpis(self.logika.lista_ulic[1])
        self.assertTrue(wynik1)
        nowe_ulice=self.logika.lista_ulic
        #print('nowe_ulice',nowe_ulice)
        self.assertEqual(len(stare_ulice)-1,len(nowe_ulice))

        #kasowanie nieistniejacego
        nieistniejacy=KW.WpisUlica("piłkarska")
        wynik2=self.logika.kasuj_wpis(nieistniejacy)
        self.assertFalse(wynik2)

        #zly typ do skasowania
        with self.assertRaises(TypeError):
            self.logika.kasuj_wpis("Krystyna")

    def test_czy_lista_slowek_unikaty(self):
        "po wielu operacjach powinny być unikaty w lista_slowek i pliku ze slowkami"

        #1.to co jest po operacjach na wpisach
        rozmiar_listy_slowek1=len(self.logika.lista_slowek)
        rozmiar_unikalnej_listy_slowek1=len(NP.unique(self.logika.lista_slowek))

        #print('rozmiar_listy_slowek1',rozmiar_listy_slowek1)
        #print('rozmiar_unikalnej_listy_slowek1',rozmiar_unikalnej_listy_slowek1)
        self.assertEqual(rozmiar_listy_slowek1,rozmiar_unikalnej_listy_slowek1)

        #2.porównanie z tym co zapisał w plikach
        self.logika.wczytaj_slowka()
        rozmiar_listy_slowek2=len(self.logika.lista_slowek)
        rozmiar_unikalnej_listy_slowek2=len(NP.unique(self.logika.lista_slowek))

        #print('rozmiar_listy_slowek2',rozmiar_listy_slowek2)
        #print('rozmiar_unikalnej_listy_slowek2',rozmiar_unikalnej_listy_slowek2)
        self.assertEqual(rozmiar_listy_slowek2,rozmiar_unikalnej_listy_slowek2)

        #porównanie pamięci z dyskiej
        self.assertEqual(rozmiar_listy_slowek1,rozmiar_listy_slowek2)

    def test_czy_lista_ulic_unikaty(self):
        "po wielu operacjach powinny być unikaty w lista_ulic i pliku z ulicami"

        #1.to co jest po operacjach na wpisach
        rozmiar_listy_ulic1=len(self.logika.lista_ulic)
        rozmiar_unikalnej_listy_ulic1=len(NP.unique(self.logika.lista_ulic))

        #print('rozmiar_listy_ulic1',rozmiar_listy_ulic1)
        #print('rozmiar_unikalnej_listy_ulic1',rozmiar_unikalnej_listy_ulic1)
        self.assertEqual(rozmiar_listy_ulic1,rozmiar_unikalnej_listy_ulic1)

        #2.porównanie z tym co zapisał w plikach
        self.logika.wczytaj_ulice()
        rozmiar_listy_ulic2=len(self.logika.lista_ulic)
        rozmiar_unikalnej_listy_ulic2=len(NP.unique(self.logika.lista_ulic))
        #print('rozmiar_listy_ulic2',rozmiar_listy_ulic2)
        #print('rozmiar_unikalnej_listy_ulic2',rozmiar_unikalnej_listy_ulic2)

        self.assertEqual(rozmiar_listy_ulic2,rozmiar_unikalnej_listy_ulic2)

        #porównanie pamięci z dyskiem
        self.assertEqual(rozmiar_listy_ulic1,rozmiar_listy_ulic2)

    def test_zwroc_ust_log_do_zapisu(self):
        "do zapisu ustawienia.xml potrzebne ustawienia klasy Logika"
        wynik=self.logika.zwroc_ust_log_do_zapisu()
        #wynik=['cos','gdzie','V',100]

        self.assertEqual(len(wynik),4)

        self.assertIsInstance(wynik[0],str)
        self.assertNotEqual(wynik[0],'')
        self.assertIsInstance(wynik[1],str)
        self.assertNotEqual(wynik[1],'')

        self.assertTrue(wynik[2] in ['A','B','C'])

        self.assertIsInstance(wynik[3],int)
        self.assertTrue(0<=wynik[3]<=100)

if __name__=='__main__':
    UT.main()
