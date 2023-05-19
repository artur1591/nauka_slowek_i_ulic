'''
testy dla klas WpisUlica i WpisSlowko
'''
import unittest as UT
import klasa_wpis_ulica_wpis_slowko as KW

class TestKlasWpisObu(UT.TestCase):
    "..."
    def test_init_wpis_ulica_arg_konieczne(self):
        "domyślne tryb i ile_razy_wylos"
        one=KW.WpisUlica("Czerwona")
        self.assertTrue(one.tryb in ['A','B','C'])
        self.assertEqual(one.ile_razy_wylos,0)
        self.assertIsInstance(one.pierwszy,str)

    def test_init_wpis_ulica_arg_pelne_poprawne(self):
        "pełny zestaw danych WpisUlica"
        one=KW.WpisUlica('Zielona','B',2)
        self.assertTrue(one.tryb in ['A','B','C'])
        self.assertTrue(one.ile_razy_wylos>=0)

    def test_init_wpis_ulica_arg_pelne_zle(self):
        "wyjątki powinny być"
        with self.assertRaises(ValueError):
            KW.WpisUlica("Jasna","F",2)
            KW.WpisUlica("Ciemna","A",-2)

        with self.assertRaises(TypeError):
            KW.WpisUlica(123,'C',34)
            KW.WpisSlowko(123,45,'B',0)

    def test_init_wpis_slowko_arg_pelne_dobre(self):
        "sprawdza typy ustawione w init"
        one=KW.WpisSlowko("one","jeden","A",0)
        self.assertIsInstance(one.pierwszy,str)
        self.assertIsInstance(one.drugi,str)
        self.assertIsInstance(one.tryb,str)
        self.assertIsInstance(one.ile_razy_wylos,int)

    def test_init_wpis_slowko_arg_zle(self):
        "wyjątki powinny być"
        with self.assertRaises(ValueError):
            KW.WpisSlowko(3,5,'A')
            KW.WpisSlowko(3,5,'A',2)
            KW.WpisSlowko(3,5)

    def test__eq__ulic(self):
        "sprawdza wszystkie składowe"
        one=KW.WpisUlica("rf")
        two=KW.WpisUlica("rf")
        self.assertEqual(one,two)

        three=KW.WpisUlica('rf','A',2)
        four=KW.WpisUlica('rf','A',0)
        self.assertNotEqual(three,four)

    def test__lt__ulic(self):
        "sprawdza tylko składową pierwszy"

        one=KW.WpisUlica("gvdi")
        two=KW.WpisUlica("harf")
        self.assertLess(one,two)

        one=KW.WpisUlica("zkkddgvdi")
        two=KW.WpisUlica("harf")
        self.assertLess(two,one)

        one=KW.WpisUlica("askjif","B",10)
        two=KW.WpisUlica("bieloa","A",1)
        self.assertLess(one,two)

    def test__eq__slowek(self):
        "sprawdza wszystkie składowe"

        one=KW.WpisSlowko("rf","wa")
        two=KW.WpisSlowko("rf","wa")
        self.assertEqual(one,two)

        one=KW.WpisSlowko("rf","wa","A",0)
        two=KW.WpisSlowko("rf","wa","A",3)
        self.assertNotEqual(one,two)

        three=KW.WpisSlowko("rf","gv","A",2)
        four=KW.WpisSlowko("rf","31","A",0)
        self.assertNotEqual(three,four)

    def test__lt__slowek(self):
        "sprawdza tylko skłądową pierwszy"

        one=KW.WpisSlowko("rf","wa")
        two=KW.WpisSlowko("rf2","wa")
        self.assertLess(one,two)

        one=KW.WpisSlowko("drf","wa")
        two=KW.WpisSlowko("rf","wa")
        self.assertLess(one,two)

        one=KW.WpisSlowko("ygdrf","wa")
        two=KW.WpisSlowko("rf","wa")
        self.assertLess(two,one)

    def test_czy_str_jest_klasy_WpisUlica(self):
        "rozpoznawanie typu z str(WpisUlica)"

        zero=KW.WpisUlica("Kwiecista","B",14)
        ulica_na_str=str(zero)
        wynik0=KW.WpisUlica.czy_str_jest_klasy_WpisUlica(ulica_na_str)
        self.assertTrue(wynik0)

        two=KW.WpisUlica("Jasna")
        ulica_na_str=str(two)
        wynik1=KW.WpisUlica.czy_str_jest_klasy_WpisUlica(ulica_na_str)
        self.assertTrue(wynik1)

        wynik2=KW.WpisUlica.czy_str_jest_klasy_WpisUlica("zmyślony 9")
        self.assertFalse(wynik2)

        two=KW.WpisSlowko("jeden","one")
        slowko_na_str=str(two)
        wynik3=KW.WpisUlica.czy_str_jest_klasy_WpisUlica(slowko_na_str)
        self.assertFalse(wynik3)

    def test_str_do_WpisUlica(self):
        "zamienia str-a na obiekt klasy WpisUlica"

        one=KW.WpisUlica("Zielona")
        jako_str=str(one)
        wynik1=KW.WpisUlica.str_do_WpisUlica(jako_str)
        self.assertIsInstance(wynik1,KW.WpisUlica)

        two=KW.WpisSlowko("grey","szary")
        jako_str=str(two)
        wynik2=KW.WpisUlica.str_do_WpisUlica(jako_str)
        self.assertFalse(wynik2)

        wynik3=KW.WpisUlica.str_do_WpisUlica("ty to filozof jesteś")
        self.assertFalse(wynik3)

    def test_czy_str_jest_klasy_WpisSlowko(self):
        "rozpoznawanie typu z str(WpisSlowko)"

        one=KW.WpisSlowko("jeden","one")
        slowko_na_str=str(one)
        wynik1=KW.WpisSlowko.czy_str_jest_klasy_WpisSlowko(slowko_na_str)
        self.assertTrue(wynik1)

        two=KW.WpisSlowko("dlugi_napis_jakis","long_text_in_english")
        slowko_na_str=str(two)
        wynik2=KW.WpisSlowko.czy_str_jest_klasy_WpisSlowko(slowko_na_str)
        self.assertTrue(wynik2)

        trzy=KW.WpisUlica("Czerwona")
        ulica_na_str=str(trzy)
        wynik3=KW.WpisSlowko.czy_str_jest_klasy_WpisSlowko(ulica_na_str)
        self.assertFalse(wynik3)

        wynik4=KW.WpisSlowko.czy_str_jest_klasy_WpisSlowko("zmyslam123 C")
        self.assertFalse(wynik4)

        wynik5=KW.WpisSlowko.czy_str_jest_klasy_WpisSlowko("past simple (zdanie)|podmiot 2f A 2")
        self.assertTrue(wynik5)

    def test_str_do_WpisSlowko(self):
        "zamienia str-a na obiekt klasy WpisSlowko"

        one=KW.WpisSlowko("zielony","green")
        jako_str=str(one)
        wynik1=KW.WpisSlowko.str_do_WpisSlowko(jako_str)
        self.assertIsInstance(wynik1,KW.WpisSlowko)

        two=KW.WpisUlica("Szara")
        jako_str=str(two)
        wynik2=KW.WpisSlowko.str_do_WpisSlowko(jako_str)
        self.assertFalse(wynik2)

        wynik3=KW.WpisSlowko.str_do_WpisSlowko("ty to filozof jesteś")
        self.assertFalse(wynik3)


if __name__=='__main__':
    UT.main()
