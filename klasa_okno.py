#!/usr/bin/python3.9
'''
oddzielenie klasy Okno od klasy Logika
'''
import tkinter as TK
import tkinter.ttk as TTK
import tkinter.font as FO
import os
import sys
import time as TI
import threading as TH
os.environ['PYGAME_HIDE_SUPPORT_PROMPT']="hide"
import pygame as PG
import klasa_logika as KL

import klasa_pasek_stanu as KPS

class Okno:
    "dlaczego ta klasa nie dziedziczy po jakieś tkinter? co mi to da?"
    def __init__(self,procent_slowek=None):
        ""
        self.rozm_x=None
        self.rozm_y=None
        self.czcionka_big=None
        self.czcionka_middle=None
        self.czcionka_small=None
        self.czcionka_family=None
        self.alarm_po_ilu_sek=None
        self.plik_minutnika=''
        self.watki_zakoncz=False
        self.pasekstanu=None

        #main
        print('sprawdzić czy pokazuje tylko najrzadziej losowane')
        print('import Pmw sprawdzić widżety')
        ust_okn,ust_log=self.wczytaj_ustawienia_programu()
        self.okno=TK.Tk()
        self.wpisz_ustawienia_w_klase_okno(ust_okn)

        if not procent_slowek is None:
            ust_log[3]=procent_slowek
        self.logika=KL.Logika(ust_log)

        self.zbuduj_okno(self.logika.komunikat_bledu)

        self.fun_spacja()

        self.okno.mainloop()

    def zamknij(self,event=None):
        "..."
        self.watki_zakoncz=True
        if self.logika.komunikat_bledu=='':
            self.zapisz_ustawienia_programu()
        self.logika.zamknij()
        self.pasekstanu.zamknij()
        self.okno.destroy()

    def wczytaj_ustawienia_programu(self):
        '''
        z pliku ustawienia.xml

        alarm_po_ilu_sek jeśli 0 to minutnik nie startuje
        '''
        #return ust.zwroc_ustawienia_programu()
        #ust_okn=[1920,600,70,23,16,'Arial',3,'kimwilde.mp3']
        #ust_okn=[1920,600,70,23,16,'Arial',120,'data-scaner.wav']
        ust_okn=[1920,600,70,23,16,'Arial',0,'data-scaner.wav']
        ust_log=['ulice.nauka','slowka.nauka','A',50]
        return [ust_okn,ust_log]

    def zapisz_ustawienia_programu(self):
        "do pliku ustawienia.xml"
        roz_x=self.okno.winfo_width()
        roz_y=self.okno.winfo_height()
        czc_fam=self.czcionka_big['family']
        czc_roz_b=self.czcionka_big['size']
        czc_roz_m=self.czcionka_middle['size']
        czc_roz_s=self.czcionka_small['size']
        ala_ile=self.alarm_po_ilu_sek
        ala_pli=self.plik_minutnika

        ust_okn_lista=[roz_x,roz_y,czc_roz_b,czc_roz_m,czc_roz_s,czc_fam,ala_ile,ala_pli]

        plik_uli=self.logika.plik_ulice
        plik_slo=self.logika.plik_slowka
        tryb=self.logika.biezacy_tryb
        procent=self.logika.procent_slowek_reszta_ulic

        ust_log_lista=[plik_uli,plik_slo,tryb,procent]

        wynik=[ust_okn_lista,ust_log_lista]
        print(wynik)

    def wpisz_ustawienia_w_klase_okno(self,ust_okn):
        "ustawienia pobrane przez f.wczytaj_ustawienia_programu wpisuje w klase Okno"
        print('ustO=',ust_okn)
        self.rozm_x=ust_okn[0]
        self.rozm_y=ust_okn[1]
        self.czcionka_family=ust_okn[5]
        self.czcionka_big=FO.Font(family=self.czcionka_family,size=ust_okn[2])
        self.czcionka_middle=FO.Font(family=self.czcionka_family,size=ust_okn[3])
        self.czcionka_small=FO.Font(family=self.czcionka_family,size=ust_okn[4])
        self.alarm_po_ilu_sek=ust_okn[6]
        self.plik_minutnika=ust_okn[7]

    def zbuduj_okno(self,potencjalny_blad):
        '''
        jak wszystko idzie dobrze buduje okno
        ale jak jest komunikat_bledu z klasy Logika to prezentuje go w Oknie
        '''
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

        self.entry1_tresc=TK.StringVar()
        self.entry2_tresc=TK.StringVar()

        self.entry1=TK.Entry(width=70,font=self.czcionka_big,textvariable=self.entry1_tresc,
                    state=TK.DISABLED,disabledbackground='green',disabledforeground='black')
        self.entry1.grid(row=1)
        self.napis2=TK.Label(text="słowo2",font=self.czcionka_small)
        self.napis2.grid(row=2)

        self.entry2=TK.Entry(width=70,font=self.czcionka_big,textvariable=self.entry2_tresc,
                    state=TK.DISABLED,disabledbackground='green',disabledforeground='black')
        self.entry2.grid(row=3)

        self.pasekstanu=KPS.Pasekstanu(self.okno,self.czcionka_small)
        self.pasekstanu.grid(row=4,sticky='SWE')
        self.sajzgrip=TTK.Sizegrip(self.okno)
        self.sajzgrip.grid(row=4,sticky='SE')
        self.pasekstanu.ustaw(ktory=1,tresc="Jestem",na_ile_sek=3)
        #print('tryb=',self.logika.biezacy_tryb)
        self.pasekstanu.ustaw(ktory=0,tresc="Tryb: "+self.logika.biezacy_tryb)

        if potencjalny_blad!='':
            #jest komunikat_bledu więc niestartuj programu
            self.entry1_tresc.set(potencjalny_blad)
            self.entry1_tresc.set(potencjalny_blad)
            print('---komunikat_bledu:',potencjalny_blad,'---')
        else:
            if self.alarm_po_ilu_sek>0:
                self.wlacz_minutnik()
            else:
                #print('---minutnik wyłączony---')
                self.pasekstanu.ustaw(ktory=2,tresc="---minutnik wyłączony---")

        #bindy:
        self.okno.bind("<space>",self.fun_spacja)
        self.okno.bind("<KeyPress-Escape>",self.zamknij)
        self.okno.bind("<KeyPress-F1>",self.pokaz_pomoc)
        self.okno.bind("<Control-Key-0>",self.cofnij_ilosc_wylos_biez_wpisu_ok)

        self.okno.bind("<Control-Key-s>",self.szukaj_wpisow_ok)
        self.okno.bind("<Control-Key-e>",self.edytuj_wpis_ok)
        self.okno.bind("<Control-Key-d>",self.dodaj_wpis_ok)
        self.okno.bind("<Control-Key-k>",self.kasuj_wpis_ok)

        self.okno.bind("<Control-Key-a>",lambda event:self.ustaw_tryb_biezacego_wpisu('A'))
        self.okno.bind("<Control-Key-b>",lambda event:self.ustaw_tryb_biezacego_wpisu('B'))
        self.okno.bind("<Control-Key-c>",lambda event:self.ustaw_tryb_biezacego_wpisu('C'))
        self.okno.bind("<Control-Key-t>",self.zmien_biezacy_tryb)
        self.okno.bind("<Control-Key-u>",self.edycja_ustawien)
        #też Escape
        self.okno.bind("<Control-Key-q>",self.zamknij)
        self.okno.bind("<Control-Key-z>",self.zerowanie_wpisow)

        self.okno.bind("<Control-KP_Add>",lambda event:self.czcionke_zmien('+'))
        self.okno.bind("<Control-KP_Subtract>",lambda event:self.czcionke_zmien('-'))
        self.okno.bind("<Control-KP_Multiply>",lambda event:self.czcionke_zmien('*'))

    def zerowanie_wpisow(self,event):
        '''
        tworzy okno i zeruje wskazany rodzaj wpisów,tj:
            albo ile_razy_wylos na 0
            albo tryb na A
                dla ulic i słówek oddzielnie
        '''
        def anulowanie(_):
            okienko.destroy()

        okienko=TK.Toplevel(self.okno,)
        okienko.title('Ilość Wylosowań na Zero lub Tryb na A')
        okienko.geometry('+350+300')

        guzik1=TK.Button(okienko,font=self.czcionka_small,width=25,
                            text="Ulice:  Zeruj Ilości Wylosowań",
                            command=self.logika.zeruj_ilosc_wylosowan_ulic)
        guzik2=TK.Button(okienko,font=self.czcionka_small,width=25,
                            text="Słówka: Zeruj Ilości Wylosowań",
                            command=self.logika.zeruj_ilosc_wylosowan_slowek)

        guzik3=TK.Button(okienko,font=self.czcionka_small,width=25,
                            text="Ulice: Zeruj do Trybu A",
                            command=self.logika.zeruj_tryb_ulic)
        guzik4=TK.Button(okienko,font=self.czcionka_small,width=25,
                            text="Słówka: Zeruj do Trybu A",
                            command=self.logika.zeruj_tryb_slowek)

        guzikZ=TK.Button(okienko,font=self.czcionka_small,
                            text=" Zamknij (Escape)",width=52,
                            command=lambda:anulowanie(event))

        okienko.bind("<KeyPress-Escape>",anulowanie)

        guzik1.grid(row=0,column=0)
        guzik2.grid(row=0,column=1)
        guzik3.grid(row=1,column=0)
        guzik4.grid(row=1,column=1)
        guzikZ.grid(row=2,columnspan=2)


    def pokaz_sytuacje(self,_):
        "tylko do celów kontrolnych"
        print('logika')
        print('   ',self.logika.lista_ulic)
        print('   ',self.logika.lista_slowek)
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
                if self.watki_zakoncz:
                    return
                self.pasekstanu.ustaw(ktory=2,tresc='Zacząłem '+konwertuj(odliczone))
                if self.alarm_po_ilu_sek==odliczone:
                    self.pasekstanu.ustaw(ktory=1,tresc='--KONIEC JUŻ--',na_ile_sek=5)
                    self.alarmuj_dzwiekiem(self.plik_minutnika)
                TI.sleep(0.25)
                if self.watki_zakoncz:
                    return
                TI.sleep(0.25)
                if self.watki_zakoncz:
                    return
                TI.sleep(0.25)
                if self.watki_zakoncz:
                    return
                TI.sleep(0.25)
                odliczone+=1

        watek=TH.Thread(target=czasomierz,daemon=True)
        watek.start()

    def alarmuj_dzwiekiem(self,jaki_utwor):
        "daemon True powoduje wyłączenie dźwięku przy szybkim zamknięciu programu"
        def wlacz_play():
            "radzi sobie z wav i mp3 na debianie"
            if jaki_utwor.endswith('.mp3'):
                print('---plik_minutnika jest w formacie mp3---')
                PG.mixer.init()
                PG.mixer.music.load(jaki_utwor)
                PG.mixer.music.play()
            elif jaki_utwor.endswith('.wav'):
                print('---plik_minutnika jest w formacie wav---')
                PG.mixer.init()
                play_obj=PG.mixer.Sound(jaki_utwor)
                play_obj.play()
            else:
                print('---plik inny niż mp3 i wav---')

        watek=TH.Thread(target=wlacz_play,daemon=True)
        watek.start()

    def fun_spacja(self,event=None):
        "jak jest błąd fun_spacja niewykonuje się"
        #print('fun_spacja',self.logika.biezacy_wpis,'_',self.logika.rodzaj_biezacego_wpisu,'_')
        if self.logika.komunikat_bledu:
            print('fun_spacja.blad:',self.logika.komunikat_bledu)
            self.ustaw_pole_tekstowe(0,self.logika.komunikat_bledu)
            self.ustaw_pole_tekstowe(1,self.logika.komunikat_bledu)
            return

        #print('fun_spacja2',self.logika.rodzaj_biezacego_wpisu)
        if self.logika.rodzaj_biezacego_wpisu=='':
            self.logika.rodzaj_biezacego_wpisu=self.logika.wez_z_listy_zadan()
            #print('wzialem z listy zadan',self.logika.rodzaj_biezacego_wpisu)
            self.fun_spacja()

        elif self.logika.rodzaj_biezacego_wpisu=='u':
            self.logika.biezacy_wpis=self.logika.wylosuj_ulice_z_inkrem()
            if self.logika.biezacy_wpis is False:
                self.ustaw_pole_tekstowe(0,"---brak słówek w trybie "+
                                            self.logika.biezacy_tryb+"---")
                self.ustaw_pole_tekstowe(1,"---brak słówek w trybie "+
                                            self.logika.biezacy_tryb+"---")
                self.logika.rodzaj_biezacego_wpisu=''
            else:
                self.ustaw_pole_tekstowe(0,self.logika.biezacy_wpis.pierwszy)
                self.czysc_pole_tekstowe(1)
                self.logika.rodzaj_biezacego_wpisu=''

        elif self.logika.rodzaj_biezacego_wpisu=='s1':
            self.logika.biezacy_wpis=self.logika.wylosuj_slowko_z_inkrem()
            if self.logika.biezacy_wpis is False:
                self.ustaw_pole_tekstowe(0,"---brak słówek w trybie "+
                                            self.logika.biezacy_tryb+"---")
                self.ustaw_pole_tekstowe(1,"---brak słówek w trybie "+
                                            self.logika.biezacy_tryb+"---")
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
            #self.entry1.delete(0,TK.END)
            #self.entry1.insert(0,tresc)
            #print('ustawiam na',tresc)
            self.entry1_tresc.set(tresc)
        else:
            #self.entry2.delete(0,TK.END)
            #self.entry2.insert(0,tresc)
            self.entry2_tresc.set(tresc)

    def czysc_pole_tekstowe(self,ktory):
        "górne i dolne pole do wyświetlania słówek/tłumaczeń/ulic/..."
        if ktory not in [0,1]:
            raise TypeError('ktory musi być 0/1. jest',ktory)

        if ktory==0:
            #self.entry1.delete(0,TK.END)
            self.entry1_tresc.set('')
        else:
            #self.entry2.delete(0,TK.END)
            self.entry2_tresc.set('')

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
            self.pasekstanu.ustaw(ktory=1,tresc='zmieniłem tryb bieżacego wpisu na '+na_jaki,
                                    na_ile_sek=3)
        else:
            self.pasekstanu.ustaw(ktory=1,tresc='już jest ten tryb',na_ile_sek=3)

    def pokaz_pomoc(self,_):
        ""
        print('pokaz pomoc')

    def edycja_ustawien(self,_):
        ""
        print('edycja_ustawien')

    def czcionke_zmien(self,jaka_operacja):
        "operacje to +  -   *"
        print('czcionke_zmien.operacja',jaka_operacja)


    #4 metody zarządzające wpisami
    def szukaj_wpisow_ok(self,_):
        '''
        wykorzystuje metode szukaj_wpis klasy Logika
        realizuje również kasowanie metodą kasuj_wpis klasy Logika
        '''
        #print('f.szukaj_wpisow_ok')
        def zamknij_okienko(event):
            "zamykanie Escape lub ręcznie"
            okienko.destroy()

        def kasowanie_wpisu_guzikiem():
            print('f.kasowanie_wpisu_guzikiem')
            ktory=wyniki_szukania.curselection()
            #print(wyniki_szukania.get(ktory))
            do_skasowania_str=wyniki_szukania.get(ktory)[3:]
            print('do skasowania:',do_skasowania_str)
            print('typ',wybor_ulica.get(),wybor_slowko.get())

            if wybor_ulica.get()=='ulice' and wybor_slowko.get()=='':
                do_skasowania_wpis=KL.KW.str_do_wpis_ulica(do_skasowania_str)
                if do_skasowania_wpis:
                    self.logika.kasuj_wpis(do_skasowania_wpis)
                    guzik_kasuj.config(state=TK.DISABLED)
                    wyniki_szukania.delete(0,TK.END)
            else:
                do_skasowania_wpis=KL.KW.str_do_wpis_slowko(do_skasowania_str)
                if do_skasowania_wpis:
                    self.logika.kasuj_wpis(do_skasowania_wpis)
                    guzik_kasuj.config(state=TK.DISABLED)
                    wyniki_szukania.delete(0,TK.END)

        def ustaw_szukanie_ulic():
            #print('ulica do szukania')
            wybor_ulica.set('ulice')
            wybor_slowko.set('')
            okienko.title('Szukanie Ulic')

        def ustaw_szukanie_slowek():
            #print('slowko do szukania')
            wybor_ulica.set('')
            wybor_slowko.set('slowka')
            okienko.title('Szukanie Słówek')

        def zaznaczony_wpis(event):
            print('zaznaczony_wpis')
            ktory=wyniki_szukania.curselection()
            #print(wyniki_szukania.get(ktory))
            uzyskany_wpis=wyniki_szukania.get(ktory)[3:]
            print('uzyskany_wpis',uzyskany_wpis)
            guzik_kasuj.config(state=TK.NORMAL)

        def szukanie(event):
            #print('wybrane',wybor_slowko.get(),wybor_ulica.get(),'_')
            #print('wpisałeś',pole_szukania.get(),'=')
            wybrany_typ=None

            if wybor_ulica.get()=='ulice' and wybor_slowko.get()=='':
                wybrany_typ='u'
            else:
                wybrany_typ='s'

            if pole_szukania.get()=='' or len(pole_szukania.get())<3:
                wyniki_szukania.delete(0,TK.END)
                wyniki_szukania.insert(1,'---wpisz przynajmniej 3 znaki---')
            else:
                co_znalazl=self.logika.szukaj_wpis(szukany_str=pole_szukania.get(),typ=wybrany_typ)
                #print('co_znalazl',co_znalazl)
                if not co_znalazl:
                    wyniki_szukania.delete(0,TK.END)
                    wyniki_szukania.insert(TK.END,'---nic się nie znalazło---')
                else:
                    wyniki_szukania.delete(0,TK.END)
                    #print('co_znalazl',co_znalazl)
                    if isinstance(co_znalazl,list):
                        #jak jest więcej niż 1 znalezionych
                        for ktory in enumerate(co_znalazl):
                            #print('ktory',ktory)
                            #wyniki_szukania.insert(TK.END,'---'+str(co_znalazl[ktory])+'\n')
                            wyniki_szukania.insert(ktory[0]+1,'---'+str(ktory[1]))
                    else:
                        #jak tylko 1 jest
                        wyniki_szukania.insert(1,'---'+str(co_znalazl))

        okienko=TK.Toplevel(self.okno)
        okienko.geometry('+350+300')
        okienko.bind('<KeyPress-Escape>',zamknij_okienko)

        wybor_ulica=TK.StringVar('')
        wybor_slowko=TK.StringVar('')

        radio1=TK.Radiobutton(okienko,text='Ulice',variable=wybor_ulica,
                        command=ustaw_szukanie_ulic,value='ulice',font=self.czcionka_small)
        radio2=TK.Radiobutton(okienko,text='Słówka',variable=wybor_slowko,
                        command=ustaw_szukanie_slowek,value='slowka',font=self.czcionka_small)
        guzik_kasuj=TK.Button(okienko,text='Kasuj Wpis',state=TK.DISABLED,
                        command=kasowanie_wpisu_guzikiem,font=self.czcionka_small)

        if self.logika.procent_slowek_reszta_ulic==0:
            wybor_slowko.set('')
            wybor_ulica.set('ulice')
            #print('szukanie ulic')
        else:
            wybor_slowko.set('slowka')
            wybor_ulica.set('')
            #print('szukanie slowek')

        napis1=TK.Label(okienko,text="Wpisz tutaj (przynajmniej 3 znaki):",font=self.czcionka_small)

        pole_szukania=TK.Entry(okienko,font=self.czcionka_small,width=30)
        pole_szukania.bind("<Return>",szukanie)
        pole_szukania.focus_set()

        wyniki_szukania=TK.Listbox(okienko,font=self.czcionka_small,width=50,height=17)
        wyniki_szukania.bind("<<ListboxSelect>>",zaznaczony_wpis)

        if type(self.logika.biezacy_wpis) is KL.KWU:
            ustaw_szukanie_ulic()
        else:
            ustaw_szukanie_slowek()

        #grid-y okienka:
        radio1.grid(row=0,column=0)
        radio2.grid(row=0,column=1)
        guzik_kasuj.grid(row=0,column=2,sticky='E')
        napis1.grid(row=1,columnspan=3)
        pole_szukania.grid(row=2,columnspan=3)
        wyniki_szukania.grid(row=3,rowspan=9,columnspan=3)
        #koniec f.szukaj_wpisow_ok

    def dodaj_wpis_ok(self,_):
        '''
        wykorzystuje metodę dodaj_wpis klasy Logika

        rozumiem że jest błąd w Radiobutton. donosili o tym w necie
        dlatego użyłem podwójnego StringVar(wybor_ulica i wybor_slowko)
        '''
        if self.logika.komunikat_bledu!='':
            print('---jest błąd:',self.logika.komunikat_bledu,'---')
            print('---ale można dodawać wpisy ---')

        def ustaw_dodawanie_ulicy():
            ""
            wybor_ulica.set('ulica')
            wybor_slowko.set('')
            okienko.title('Dodawanie Ulicy')
            podpis1.config(text='Ulica:')
            wpis2.delete(0,TK.END)
            podpis2.config(text='')
            wpis2.config(state=TK.DISABLED)
            guzik_potwierdz.config(text='Dodaj Nową Ulicę')

        def ustaw_dodawanie_slowka():
            ""
            wybor_slowko.set('slowko')
            wybor_ulica.set('')
            okienko.title('Dodawanie Słówka')
            podpis1.config(text='Angielski:')
            podpis2.config(text='Polski:')
            wpis2.config(state=TK.NORMAL)
            guzik_potwierdz.config(text='Dodaj Nowe Słówko')

        def zamknij_okienko(_=None):
            "jak chcesz tylko zamknąć okno"
            okienko.destroy()

        def dodawanie_wpisu(_=None):
            "zastosowanie i zamykanie okna"
            if wybor_ulica.get()=='ulica' and wybor_slowko.get()=='':
                if wpis1.get()=='':
                    print('---nie można dodać pustej ulicy ---')
                    return
                #print('dodaje nową:',wpis1.get())
                tmp=KL.KWU(wpis1.get())
                zwrocil=self.logika.dodaj_wpis(tmp)
                if zwrocil:
                    wpis1.delete(0,TK.END)
                    print('---dodałem nową ulicę---')
                else:
                    print('---nieudane dodanie nowej ulicy---')

            elif wybor_slowko.get()=='slowko' and wybor_ulica.get()=='':
                if wpis1.get()=='' or wpis2.get()=='':
                    print('---jedno/drugie znaczenie nowego słowa puste---')
                    return
                #print('dodaje nowe:',wpis1.get(),wpis2.get())
                tmp=KL.KWS(wpis1.get(),wpis2.get())
                zwrocil=self.logika.dodaj_wpis(tmp)
                if zwrocil:
                    wpis1.delete(0,TK.END)
                    wpis2.delete(0,TK.END)
                    print('---dodałem nowe słówko---')
                else:
                    print('---nieudane dodanie nowego słówka---')

        okienko=TK.Toplevel(self.okno)
        okienko.geometry('+350+300')
        okienko.bind("<KeyPress-Escape>",zamknij_okienko)

        wybor_ulica=TK.StringVar('')
        wybor_slowko=TK.StringVar('')

        radio1=TK.Radiobutton(okienko,text='Ulica',value='ulica',command=ustaw_dodawanie_ulicy,
                    font=self.czcionka_small,variable=wybor_ulica)
        radio2=TK.Radiobutton(okienko,text='Słówko',value='slowko',command=ustaw_dodawanie_slowka,
                    font=self.czcionka_small,variable=wybor_slowko)

        if self.logika.procent_slowek_reszta_ulic==0:
            wybor_ulica.set('ulica')
            wybor_slowko.set('')
        else:
            wybor_ulica.set('')
            wybor_slowko.set('slowko')

        podpis1=TK.Label(okienko,font=self.czcionka_small)
        wpis1=TK.Entry(okienko,font=self.czcionka_middle,width=30)
        podpis2=TK.Label(okienko,font=self.czcionka_small)
        wpis2=TK.Entry(okienko,font=self.czcionka_middle,width=30)

        guzik_cofaj=TK.Button(okienko,text='Anuluj(Escape)',font=self.czcionka_small,
                                    command=zamknij_okienko)
        guzik_potwierdz=TK.Button(okienko,text='Dodaj Nowy Wpis',font=self.czcionka_small,
                                    command=dodawanie_wpisu)


        if type(self.logika.biezacy_wpis) is KL.KWU:
            podpis1.config(text='Nazwa Ulicy:')
            podpis2.config(text='')
            wpis2.config(state=TK.DISABLED)
        else:
            podpis1.config(text='Angielski:')
            podpis2.config(text='Polski:')
            wpis2.config(state=TK.NORMAL)
        wpis1.focus_set()

        if type(self.logika.biezacy_wpis) is KL.KWU:
            ustaw_dodawanie_ulicy()
        else:
            ustaw_dodawanie_slowka()

        radio1.grid(row=0,column=0)
        radio2.grid(row=0,column=1)

        podpis1.grid(row=1,columnspan=2)
        wpis1.grid(row=2,columnspan=2)
        podpis2.grid(row=3,columnspan=2)
        wpis2.grid(row=4,columnspan=2)
        guzik_cofaj.grid(row=7,column=0)
        guzik_potwierdz.grid(row=7,column=1)
        #koniec f.dodaj_wpis_ok


    def kasuj_wpis_ok(self,_):
        "kasuj wpis"
        print('f.kasuj_wpis_ok. kasowanie powinno być częścią szukania raczej')

    def edytuj_wpis_ok(self,event):
        "edycja wpisu"
        print('f.edytuj_wpis_ok')
        if self.logika.komunikat_bledu!='':
            print('---jest błąd:',self.logika.komunikat_bledu,'---')
            return

        def zamknij_okienko_bez_zmian(_=None):
            "jak chcesz tylko zamknąć okno"
            #print('zamknij_okienko_bez_zmian')
            okienko.destroy()

        def zamknij_okienko_zastosuj_zmiany(_=None):
            "zastosowanie i zamykanie okna"
            #print('zamknij_okienko_zastosuj_zmiany')
            #print('wpis_biezacy',self.logika.biezacy_wpis,type(self.logika.biezacy_wpis))

            #użyłem type bo isinstance nie rozróżnia klas bazowych i pochodnych(to właśnie to jest)
            if type (self.logika.biezacy_wpis) is KL.KWU:
                #print('stwierdzam ze ulica 1',wpis1.get(),'3',wpis3.get(),'4',wpis4.get())
                if wpis1.get()!='' and wpis2.get()=='' and wpis3.get()!='' and wpis4.get()!='':
                    nowszy=KL.KWU(wpis1.get(),wpis3.get(),int(wpis4.get()))
                    #print('Unowszy=',nowszy)
                    #print('starszy=',starszy)
                    if starszy!=nowszy:
                        print('--- udana podmiana---')
                        self.logika.zmien_wpis(starszy,nowszy)
                        self.logika.biezacy_wpis=nowszy
                    self.entry1_tresc.set(self.logika.biezacy_wpis.pierwszy)
                    self.entry2_tresc.set('')
                    self.logika.rodzaj_biezacego_wpisu=''
                else:
                    print('---niemożna podmienić na puste---')
            else:
                #print('stwierdzam ze słówko 1',wpis1.get(),'2',wpis2.get(),
                #                    '3',wpis3.get(),'4',wpis4.get())
                if wpis1.get()!='' and wpis2.get()!='' and wpis3.get()!='' and wpis4.get()!='':
                    nowszy=KL.KWS(wpis1.get(),wpis2.get(),wpis3.get(),int(wpis4.get()))
                    #print('Snowszy=',nowszy)
                    #print('starszy=',starszy)
                    if starszy!=nowszy:
                        print('--- udana podmiana---')
                        self.logika.zmien_wpis(starszy,nowszy)
                        self.logika.biezacy_wpis=nowszy
                    self.entry1_tresc.set(self.logika.biezacy_wpis.pierwszy)
                    self.entry2_tresc.set(self.logika.biezacy_wpis.drugi)
                    self.logika.rodzaj_biezacego_wpisu=''
                else:
                    print('---niemożna podmienić na puste---')
            okienko.destroy()


        okienko=TK.Toplevel(self.okno)
        okienko.title('Edycja wpisu')
        okienko.geometry('+350+300')
        okienko.bind("<KeyPress-Escape>",zamknij_okienko_zastosuj_zmiany)

        podpis1=TK.Label(okienko,font=self.czcionka_small)
        wpis1=TK.Entry(okienko,font=self.czcionka_middle,width=30)
        podpis2=TK.Label(okienko,font=self.czcionka_small)
        wpis2=TK.Entry(okienko,font=self.czcionka_middle,width=30)
        podpis3=TK.Label(okienko,text='Tryb:',font=self.czcionka_small)
        wpis3=TTK.Combobox(okienko,font=self.czcionka_middle,width=30,state='readonly')

        tryby=('A','B','C')
        wpis3['values']=tryby
        #wpis3.current(ord(self.biezacy_tryb)-65)
        #print('trybik',ord(self.logika.biezacy_wpis.tryb)-65)
        wpis3.current(ord(self.logika.biezacy_wpis.tryb)-65)

        podpis4=TK.Label(okienko,text='Ile Razy Wylosowany:',font=self.czcionka_small)
        wpis4=TTK.Combobox(okienko,font=self.czcionka_middle,width=30,state='readonly')

        ilosci=tuple(range(0,self.logika.biezacy_wpis.ile_razy_wylos+11))
        wpis4['values']=ilosci
        #print('ilosci',ilosci)
        wpis4.current(self.logika.biezacy_wpis.ile_razy_wylos)

        #print('biezacy',self.logika.biezacy_wpis)
        starszy=self.logika.biezacy_wpis

        guzik_cofaj=TK.Button(okienko,text='Rezygnuj ze zmian',font=self.czcionka_small,
                                    command=lambda:zamknij_okienko_bez_zmian(event))
        guzik_potwierdz=TK.Button(okienko,text='Zatwierdź(Escape)',font=self.czcionka_small,
                                    command=lambda:zamknij_okienko_zastosuj_zmiany(event))


        if type(self.logika.biezacy_wpis) is KL.KWU:
            #print('stwierdzam ze ulica')
            podpis1.config(text='Nazwa Ulicy:')
            podpis2.config(text='')
            wpis1.delete(0,TK.END)
            wpis1.insert(0,self.logika.biezacy_wpis.pierwszy)
            wpis2.delete(0,TK.END)
            wpis2.config(state=TK.DISABLED)
            #if self.logika.biezacy_wpis.tryb=='A':
            #wpis3.current(0) #text=self.logika.biezacy_wpis.tryb)
            wpis3.delete(0,TK.END)
            wpis3.insert(0,self.logika.biezacy_wpis.tryb)
            wpis4.delete(0,TK.END)
            wpis4.insert(0,self.logika.biezacy_wpis.ile_razy_wylos)
        else:
            #print('stwierdzam ze slowko')
            podpis1.config(text='Angielski:')
            podpis2.config(text='Polski:')
            wpis1.delete(0,TK.END)
            wpis1.insert(0,self.logika.biezacy_wpis.pierwszy)
            wpis2.delete(0,TK.END)
            wpis2.insert(0,self.logika.biezacy_wpis.drugi)
            wpis2.config(state=TK.NORMAL)
            wpis3.delete(0,TK.END)
            wpis3.insert(0,self.logika.biezacy_wpis.tryb)
            wpis4.delete(0,TK.END)
            wpis4.insert(0,self.logika.biezacy_wpis.ile_razy_wylos)

        wpis1.focus_set()

        podpis1.grid(row=0,columnspan=2)
        wpis1.grid(row=1,columnspan=2)
        podpis2.grid(row=2,columnspan=2)
        wpis2.grid(row=3,columnspan=2)
        podpis3.grid(row=4,columnspan=2)
        wpis3.grid(row=5,columnspan=2)
        podpis4.grid(row=6,columnspan=2)
        wpis4.grid(row=7,columnspan=2)
        guzik_cofaj.grid(row=8,column=0)
        guzik_potwierdz.grid(row=8,column=1)
        #koniec f.edytuj_wpis_ok

if __name__=='__main__':
    #bo można podać argument procent_slowek_reszta_ulic zakres 0-100
    if len(sys.argv)>1:
        App=Okno(int(sys.argv[1]))
    else:
        App=Okno()
