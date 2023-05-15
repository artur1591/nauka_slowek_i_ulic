'''
oddzielenie klasy Okno od klasy Logika
'''
import tkinter as TK
import tkinter.ttk as TTK
import tkinter.font as FO
import threading as TH
import time as TI
import playsound as PS
import klasa_pasek_stanu as KPS
import klasa_logika as KL
import klasa_ustawienia as KU

class Okno:
    "..."
    def __init__(self,procent_slowek=None):
        ""
        self.rozm_x=None
        self.rozm_y=None
        self.czcionka_big=None
        self.czcionka_small=None
        self.czcionka_family=None
        self.alarm_po_ilu_sek=None
        self.watek_zakoncz_minutnika=False
        self.pasekstanu=None

        #main
        ust_okn,ust_log=self.wczytaj_ustawienia_programu()
        self.okno=TK.Tk()
        self.wpisz_ustawienia_w_klase_okno(ust_okn)

        if not procent_slowek is None:
            ust_log[3]=procent_slowek
        self.logika=KL.Logika(ust_log)
        self.zbuduj_okno()

        self.fun_spacja()

        self.okno.mainloop()

    def zamknij(self,event=None):
        ""
        self.watek_zakoncz_minutnika=True
        self.logika.zamknij()
        self.pasekstanu.zamknij()
        self.zapisz_ustawienia_programu()
        self.okno.destroy()

    def wczytaj_ustawienia_programu(self):
        "z pliku ustawienia.xml"
        #ust=KU.Ustawienia()
        #ust.wczytaj_z_pliku()

        #return ust.zwroc_ustawienia_programu()
        return [[1920,600,70,16,'Arial',10],['slowka.nauka','ulice.nauka','A',0]]

    def wpisz_ustawienia_w_klase_okno(self,ust_okn):
        "ustawienia pobrane przez f.wczytaj_ustawienia_programu wpisuje w klase Okno"
        print('ustO=',ust_okn)
        self.rozm_x=ust_okn[0]
        self.rozm_y=ust_okn[1]
        self.czcionka_family=ust_okn[4]
        self.czcionka_big=FO.Font(family=ust_okn[4],size=ust_okn[2])
        self.czcionka_small=FO.Font(family=ust_okn[4],size=ust_okn[3])
        self.alarm_po_ilu_sek=ust_okn[5]


    def zapisz_ustawienia_programu(self):
        "do pliku ustawienia.xml"
        roz_x=self.okno.winfo_width()
        roz_y=self.okno.winfo_height()
        czc_fam=self.czcionka_big['family']
        czc_roz_b=self.czcionka_big['size']
        czc_roz_s=self.czcionka_small['size']

        ust_okn_lista=[roz_x,roz_y,czc_roz_b,czc_roz_s,czc_fam,self.alarm_po_ilu_sek]

        plik_slo=self.logika.plik_slowka
        plik_uli=self.logika.plik_ulice
        tryb=self.logika.biezacy_tryb
        procent=self.logika.procent_slowek_reszta_ulic

        ust_log_lista=[plik_slo,plik_uli,tryb,procent]

        wynik=[ust_okn_lista,ust_log_lista]
        print(wynik)

    def zbuduj_okno(self):
        ""
        self.okno.config(bg='grey')
        self.okno.title("Nauka Słówek i Ulic")
        self.okno.geometry(str(self.rozm_x)+"x"+str(self.rozm_y))

        #logo
        #photo=TK.PhotoImage(file='logo.png')
        self.okno.wm_iconphoto(False,TK.PhotoImage(file='logo.png'))

        self.okno.rowconfigure(0,weight=1)
        self.okno.rowconfigure(1,weight=1)
        self.okno.rowconfigure(2,weight=1)
        self.okno.rowconfigure(3,weight=1)
        self.okno.columnconfigure(0,weight=1)

        self.napis1=TK.Label(text="słowo1",font=self.czcionka_small)
        self.napis1.grid(row=0)
        self.entry1=TK.Entry(width=70,font=self.czcionka_big,bg='green') #,height=20)
        self.entry1.grid(row=1)
        self.napis2=TK.Label(text="słowo2",font=self.czcionka_small)
        self.napis2.grid(row=2)
        self.entry2=TK.Entry(width=70,font=self.czcionka_big,bg='green')
        self.entry2.grid(row=3)
        self.pasekstanu=KPS.Pasekstanu(self.okno,self.czcionka_small)
        self.pasekstanu.grid(row=4,sticky='SWE')
        self.sajzgrip=TTK.Sizegrip(self.okno)
        self.sajzgrip.grid(row=4,sticky='SE')
        self.pasekstanu.ustaw(ktory=1,tresc="Jestem",na_ile_sek=3)
        #print('tryb=',self.logika.biezacy_tryb)
        self.pasekstanu.ustaw(ktory=0,tresc="Tryb: "+self.logika.biezacy_tryb)


        self.wlacz_minutnik()

        #bindy:
        self.okno.bind("<space>",self.fun_spacja)
        self.okno.bind("<KeyPress-Escape>",self.zamknij)
        self.okno.bind("<Control-Key-q>",self.zamknij)
        self.okno.bind("<KeyPress-F1>",self.pokaz_pomoc)
        self.okno.bind("<KeyPress-F4>",self.zarzadzaj_wpisami)
        self.okno.bind("<Control-Key-a>",lambda event:self.ustaw_tryb_biezacego_wpisu('A'))
        self.okno.bind("<Control-Key-b>",lambda event:self.ustaw_tryb_biezacego_wpisu('B'))
        self.okno.bind("<Control-Key-c>",lambda event:self.ustaw_tryb_biezacego_wpisu('C'))
        self.okno.bind("<Control-Key-t>",self.zmien_biezacy_tryb)
        self.okno.bind("<Control-KP_Add>",lambda event:self.czcionke_zmien('+'))
        self.okno.bind("<Control-KP_Subtract>",lambda event:self.czcionke_zmien('-'))
        self.okno.bind("<Control-KP_Multiply>",lambda event:self.czcionke_zmien('*'))
        self.okno.bind("<Control-Key-0>",self.cofnij_ilosc_wylos_biez_wpisu_ok)
        self.okno.bind("<Control-Key-u>",self.edycja_ustawien)
        self.okno.bind("<Control-Key-z>",self.zerowanie_wpisow)
        self.okno.bind("<Control-Key-s>",self.pokaz_sytuacje)

    def zerowanie_wpisow(self,event):
        '''
        tworzy okno i zeruje(ile_razy_wylos=0) wskazany rodzaj wpisów
        '''
        def anulowanie(self,event=None):
            okienko.destroy()

        okienko=TK.Toplevel(self.okno,)
        okienko.title('Zerowanie ilości wylosowań')
        okienko.geometry('+350+300')

        guzik1=TK.Button(okienko,text="Słówka: Zeruj Ilości Wylosowań",width=25,command=lambda:self.logika.zeruj_slowka())
        guzik1.config(font=self.czcionka_small)
        guzik2=TK.Button(okienko,text=" Ulica:  Zeruj Ilości Wylosowań",width=25,command=lambda:self.logika.zeruj_ulice())
        guzik2.config(font=self.czcionka_small)
        guzik3=TK.Button(okienko,text=" Zamknij (Escape)",width=25,command=lambda:anulowanie(event))
        guzik3.config(font=self.czcionka_small)

        okienko.bind("<KeyPress-Escape>",anulowanie)

        guzik1.grid()
        guzik2.grid()
        guzik3.grid()


    def pokaz_sytuacje(self,event):
        "tylko do celów kontrolnych"
        print('logika')
        print('   ',self.logika.lista_slowek)
        print('   ',self.logika.lista_ulic)
        print('   ',self.logika.biezacy_tryb)
        print('   ',self.logika.lista_zadan)
        print('   ',self.logika.biezacy_wpis)
        print('   ',self.logika.rodzaj_biezacego_wpisu)
        print('   ',self.logika.procent_slowek_reszta_ulic,'%')


    def wlacz_minutnik(self):
        '''
        robi watek ktory aktualizuje pasek stanu co sekunde
        '''
        odliczone=0
        #self.pasek.ustaw(ktory=2,tresc='--:--:--')
        def czasomierz():
            def konwertuj(ile_sek):
                "format do wyświetlania"
                ile_sekund=ile_sek%60
                ile_minut=ile_sek/60
                ile_godzin=ile_minut/60

                return "%02d:%02d:%02d"%(ile_godzin,ile_minut,ile_sekund)
            nonlocal odliczone
            while True:
                if self.watek_zakoncz_minutnika:
                    return
                #self.pasek.ustaw(ktory=2,tresc='Zacząłem '+str(odliczone)+' sekund temu')
                self.pasekstanu.ustaw(ktory=2,tresc='Zacząłem '+konwertuj(odliczone))
                if self.alarm_po_ilu_sek==odliczone:
                    self.pasekstanu.ustaw(ktory=1,tresc='--KONIEC JUŻ--',na_ile_sek=5)
                    self.alarmuj_dzwiekiem("moan.mp3")
                    #self.alarmuj_dzwiekiem("clock-strike.wav")
                TI.sleep(0.25)
                if self.watek_zakoncz_minutnika:
                    return
                TI.sleep(0.25)
                if self.watek_zakoncz_minutnika:
                    return
                TI.sleep(0.25)
                if self.watek_zakoncz_minutnika:
                    return
                TI.sleep(0.25)
                odliczone+=1

        watek=TH.Thread(target=czasomierz)
        watek.start()

    def alarmuj_dzwiekiem(self,jaki_utwor):
        "sugestia zmiany "
        watek=TH.Thread(target=PS.playsound,args=(jaki_utwor,))
        watek.start()

    def fun_spacja(self,event=None):
        ""
        print('fun_spacja',self.logika.biezacy_tryb)
        if self.logika.rodzaj_biezacego_wpisu=='':
            self.logika.rodzaj_biezacego_wpisu=self.logika.wez_z_listy_zadan()
            print('wzialem z listy zadan',self.logika.rodzaj_biezacego_wpisu)
            self.fun_spacja()

        elif self.logika.rodzaj_biezacego_wpisu=='u':
            self.logika.biezacy_wpis=self.logika.wylosuj_ulice_z_inkrem()
            if self.logika.biezacy_wpis is False:
                self.ustaw_pole_tekstowe(0,"---brak słówek w trybie "+self.logika.biezacy_tryb+"---")
                self.ustaw_pole_tekstowe(1,"---brak słówek w trybie "+self.logika.biezacy_tryb+"---")
                self.logika.rodzaj_biezacego_wpisu=''
            else:
                self.ustaw_pole_tekstowe(0,self.logika.biezacy_wpis.pierwszy)
                self.czysc_pole_tekstowe(1)
                self.logika.rodzaj_biezacego_wpisu=''

        elif self.logika.rodzaj_biezacego_wpisu=='s1':
            self.logika.biezacy_wpis=self.logika.wylosuj_slowko_z_inkrem()
            if self.logika.biezacy_wpis is False:
                self.ustaw_pole_tekstowe(0,"---brak słówek w trybie "+self.logika.biezacy_tryb+"---")
                self.ustaw_pole_tekstowe(1,"---brak słówek w trybie "+self.logika.biezacy_tryb+"---")
                self.logika.rodzaj_biezacego_wpisu=''
            else:
                self.ustaw_pole_tekstowe(0,self.logika.biezacy_wpis.pierwszy)
                self.czysc_pole_tekstowe(1)
                self.logika.rodzaj_biezacego_wpisu='s2'

        elif self.logika.rodzaj_biezacego_wpisu=='s2':
            self.ustaw_pole_tekstowe(1,self.logika.biezacy_wpis.drugi)
            self.logika.rodzaj_biezacego_wpisu=''

        else:
            print('co się wydarzyło?')



    def ustaw_pole_tekstowe(self,ktory,tresc):
        "górne i dolne pole do wyświetlania słówek/tłumaczeń/ulic/..."
        if ktory not in [0,1]:
            raise TypeError('ktory musi być 0/1. jest',ktory)

        if ktory==0:
            self.entry1.delete(0,TK.END)
            self.entry1.insert(0,tresc)
        else:
            self.entry2.delete(0,TK.END)
            self.entry2.insert(0,tresc)

    def czysc_pole_tekstowe(self,ktory):
        "górne i dolne pole do wyświetlania słówek/tłumaczeń/ulic/..."
        if ktory not in [0,1]:
            raise TypeError('ktory musi być 0/1. jest',ktory)

        if ktory==0:
            self.entry1.delete(0,TK.END)
        else:
            self.entry2.delete(0,TK.END)


    def cofnij_ilosc_wylos_biez_wpisu_ok(self,event):
        ""
        print('cofnij_ilosc_wylos_biez_wpisu_Ok')
        print('biezacy',self.logika.biezacy_wpis)
        self.logika.cofnij_ilosc_wylos_biez_wpisu_lo()
        print('poprawiony',self.logika.biezacy_wpis)

    def zmien_biezacy_tryb(self,event):
        ""
        self.logika.zmien_biezacy_tryb()
        print("zmien_biezacy_tryb.nowy=",self.logika.biezacy_tryb)
        self.pasekstanu.ustaw(ktory=0,tresc="Tryb: "+self.logika.biezacy_tryb)
        self.logika.zrob_liste_zadan()

    def ustaw_tryb_biezacego_wpisu(self,na_jaki):
        "konwencja tryb z dużej czyli A B C"
        print('dotychczasowy tryb=',self.logika.biezacy_wpis)
        if self.logika.biezacy_wpis.tryb!=na_jaki:
            self.logika.ustaw_tryb_biezacego_wpisu(na_jaki)
            print('poprawiony tryb=',self.logika.biezacy_wpis)
            self.pasekstanu.ustaw(ktory=1,tresc='zmieniłem tryb bieżacego wpisu na '+na_jaki,na_ile_sek=3)
        else:
            self.pasekstanu.ustaw(ktory=1,tresc='już jest ten tryb',na_ile_sek=3)

    def pokaz_pomoc(self,event):
        ""
        print('pokaz pomoc')

    def edycja_ustawien(self,event):
        ""
        print('edycja_ustawien')

    def czcionke_zmien(self,jaka_operacja):
        "operacje to +  -   *"
        print('czcionke_zmien.operacja',jaka_operacja)

    def zarzadzaj_wpisami(self,event):
        "wykorzystac moduł re"
        print('zarzadzaj_wpisami')
