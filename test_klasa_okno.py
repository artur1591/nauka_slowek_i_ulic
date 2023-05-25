#!/usr/bin/python3.9
import klasa_logika as KL
import klasa_okno as KO
import unittest as UT
import tkinter as TK

class TestKlasaOkno(UT.TestCase):
    ""
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_wczytaj_ustawienia_programu(self):
        "czy listy po 6elem + 4elem. czy typy dobre"
        self.okno=KO.Okno()
        wynik=self.okno.wczytaj_ustawienia_programu()
        ust_okn,ust_log=wynik[0],wynik[1]

        self.assertEqual(len(ust_okn),8)
        self.assertEqual(len(ust_log),4)

        self.assertIsInstance(ust_okn,list)
        self.assertIsInstance(ust_log,list)

        self.assertIsInstance(ust_okn[0],int)
        self.assertIsInstance(ust_okn[1],int)
        self.assertIsInstance(ust_okn[2],int)
        self.assertIsInstance(ust_okn[3],int)
        self.assertIsInstance(ust_okn[4],int)
        self.assertIsInstance(ust_okn[5],str)
        self.assertIsInstance(ust_okn[6],int)
        self.assertIsInstance(ust_okn[7],str)

        self.assertIsInstance(ust_log[0],str)
        self.assertIsInstance(ust_log[1],str)
        self.assertIsInstance(ust_log[2],str)
        self.assertIsInstance(ust_log[3],int)

    def test_wpisz_ustawienia_w_klase_okno(self):
        "oddzielna funkcja dla kontroli"
        self.okno=KO.Okno()
        #ust_okn,ust_log=self.okno.wczytaj_ustawienia_programu()
        #self.okno.wpisz_ustawienia_w_klase_okno(ust_okn)
        self.assertTrue(100<self.okno.rozm_x<=1920)
        self.assertTrue(100<self.okno.rozm_y<=920)
        self.assertTrue(self.okno.alarm_po_ilu_sek>0)
        self.assertNotEqual(self.okno.plik_minutnika,'')
        self.assertTrue(self.okno.logika.biezacy_tryb in ['A','B','C'])
        self.assertIsInstance(self.okno.czcionka_big,TK.font.Font)
        self.assertIsInstance(self.okno.czcionka_middle,TK.font.Font)
        self.assertIsInstance(self.okno.czcionka_small,TK.font.Font)

if __name__=='__main__':
    UT.main()
