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
        self.zbuduj_okno()

        self.fun_spacja()

        self.okno.mainloop()

    def zamknij(self,event=None):
        ""
        self.watki_zakoncz=True
        self.zapisz_ustawienia_programu()
        self.logika.zamknij()
        self.pasekstanu.zamknij()
        self.okno.destroy()

    def wczytaj_ustawienia_programu(self):
        "z pliku ustawienia.xml"
        #ust=KU.Ustawienia()
        #ust.wczytaj_z_pliku()

        #return ust.zwroc_ustawienia_programu()
        return [[1920,600,70,23,16,'Arial',120,'clock-strike.wav'],['slowka.nauka','ulice.nauka','A',100]]

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

        plik_slo=self.logika.plik_slowka
        plik_uli=self.logika.plik_ulice
        tryb=self.logika.biezacy_tryb
        procent=self.logika.procent_slowek_reszta_ulic

        ust_log_lista=[plik_slo,plik_uli,tryb,procent]

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

        self.entry1_tresc=TK.StringVar()
        self.entry2_tresc=TK.StringVar()

        self.entry1=TK.Entry(width=70,font=self.czcionka_big,textvariable=self.entry1_tresc)
        self.entry1.config(state=TK.DISABLED,disabledbackground='green')
        self.entry1.config(disabledforeground='black')

        self.entry1.grid(row=1)
        self.napis2=TK.Label(text="słowo2",font=self.czcionka_small)
        self.napis2.grid(row=2)

        self.entry2=TK.Entry(width=70,font=self.czcionka_big,textvariable=self.entry2_tresc)
        self.entry2.config(state=TK.DISABLED,disabledbackground='green')
        self.entry2.config(disabledforeground='black')


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
                if self.watki_zakoncz:
                    return
                #self.pasek.ustaw(ktory=2,tresc='Zacząłem '+str(odliczone)+' sekund temu')
                self.pasekstanu.ustaw(ktory=2,tresc='Zacząłem '+konwertuj(odliczone))
                if self.alarm_po_ilu_sek==odliczone:
                    self.pasekstanu.ustaw(ktory=1,tresc='--KONIEC JUŻ--',na_ile_sek=5)
                    #self.alarmuj_dzwiekiem("clock-strike.wav")
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

        watek=TH.Thread(target=czasomierz)
        watek.start()

    def alarmuj_dzwiekiem(self,jaki_utwor):
        "sugestia zmiany "
        watek=TH.Thread(target=PS.playsound,args=(jaki_utwor,))
        watek.start()

    def fun_spacja(self,event=None):
        ""
        #print('fun_spacja',self.logika.biezacy_wpis)
        #print('fun_spacja2',self.logika.rodzaj_biezacego_wpisu)
        if self.logika.rodzaj_biezacego_wpisu=='':
            self.logika.rodzaj_biezacego_wpisu=self.logika.wez_z_listy_zadan()
            #print('wzialem z listy zadan',self.logika.rodzaj_biezacego_wpisu)
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


    #4 metody zarządzające wpisami
    def szukaj_wpisow_ok(self,event):
        "do szukania tylko będzie"
        print('f.szukaj_wpisow_ok')
        '''
        def anulowanie(event):
            okienko.destroy()
        def szukanie(event):
            print("szukanie")
            print('wpisałeś',pole_szukania.get(),'=')
            print('wybrane',wybor_slowko_ulica.get(),'_')
            wybrany_typ=None

            if self.logika.procent_slowek_reszta_ulic==0:
                wybrany_typ='u'
            if self.logika.procent_slowek_reszta_ulic==100:
                wybrany_typ='s'

            if wybor_slowko_ulica.get()=='slowka':
                wybrany_typ='s'
            if wybor_slowko_ulica.get()=='ulice':
                wybrany_typ='u'
            #print('wybrany_typ',wybrany_typ)

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
                    print('co_znalazl',co_znalazl)
                    if isinstance(co_znalazl,list):
                        #jak jest więcej niż 1 znalezionych
                        for ktory in enumerate(co_znalazl):
                            print('ktory',ktory)
                            #wyniki_szukania.insert(TK.END,'---'+str(co_znalazl[ktory])+'\n')
                            wyniki_szukania.insert(ktory[0]+1,'---'+str(ktory[1]))
                    else:
                        #jak tylko 1 jest
                        wyniki_szukania.insert(1,'---'+str(co_znalazl))
        okienko=TK.Toplevel(self.okno,)
        okienko.title('---ogólne przeznaczenie---')
        okienko.geometry('+350+300')
        okienko.bind('<KeyPress-Escape>',anulowanie)

        wybor_slowko_ulica=TK.StringVar(okienko)
        if self.logika.procent_slowek_reszta_ulic==0:
            wybor_slowko_ulica.set('ulice')
        else:
            wybor_slowko_ulica.set('slowka')
        print('wybor_slowko_ulica',wybor_slowko_ulica.get())

        radio1=TK.Radiobutton(okienko,text='Słówka',variable=wybor_slowko_ulica,value='slowka',font=self.czcionka_small)
        radio2=TK.Radiobutton(okienko,text='Ulica',variable=wybor_slowko_ulica,value='ulice',font=self.czcionka_small)


        napis1=TK.Label(okienko,text="Wpisz tutaj (przynajmniej 3 znaki):",font=self.czcionka_small)

        pole_szukania=TK.Entry(okienko,font=self.czcionka_small,width=30)
        pole_szukania.bind("<Return>",szukanie)
        pole_szukania.focus_set()

        wyniki_szukania=TK.Listbox(okienko,font=self.czcionka_small,width=50,height=17)
        #wyniki_szukania.bind("<<ListboxSelect>>",zaznaczony_wpis)
        podpis1=TK.Label(okienko,text='Angielskie:',font=self.czcionka_small)
        wpis1=TK.Entry(okienko,font=self.czcionka_small)
        podpis2=TK.Label(okienko,text='Polskie:',font=self.czcionka_small)
        wpis2=TK.Entry(okienko,font=self.czcionka_small)
        podpis3=TK.Label(okienko,text='Tryb:',font=self.czcionka_small)
        wpis3=TTK.Combobox(okienko,font=self.czcionka_small)
        podpis4=TK.Label(okienko,text='ile_razy_wylosowany:',font=self.czcionka_small)
        wpis4=TK.Entry(okienko,font=self.czcionka_small)

        #grid-y okienka:
        radio1.grid(row=0,column=0)
        radio2.grid(row=0,column=1)
        napis1.grid(row=1,columnspan=2)
        pole_szukania.grid(row=2,columnspan=2)
        #guzik1.grid(row=2,column=1)
        wyniki_szukania.grid(row=3,rowspan=9,columnspan=2)
        #guzik2.grid(row=12,column=0)
        #guzik3.grid(row=12,column=1)
        '''

    def dodaj_wpis_ok(self,event):
        "dodaj wpis"
        print('f.dodaj_wpis_ok')

    def kasuj_wpis_ok(self,event):
        "kasuj wpis"
        print('f.kasuj_wpis_ok')

    def edytuj_wpis_ok(self,event):
        "edycja wpisu"
        print('f.edytuj_wpis_ok')

        def zamknij_okienko_bez_zmian(event=None):
            "jak chcesz tylko zamknąć okno"
            #print('zamknij_okienko_bez_zmian')
            okienko.destroy()

        def zamknij_okienko_zastosuj_zmiany(event=None):
            "zastosowanie i zamykanie okna"
            #print('zamknij_okienko_zastosuj_zmiany')
            #print('wpis_biezacy',self.logika.biezacy_wpis,type(self.logika.biezacy_wpis))

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
                #print('stwierdzam ze słówko 1',wpis1.get(),'2',wpis2.get(),'3',wpis3.get(),'4',wpis4.get())
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

        guzik_cofaj=TK.Button(okienko,text='Rezygnuj ze zmian',command=lambda:zamknij_okienko_bez_zmian(event))
        guzik_potwierdz=TK.Button(okienko,text='Zatwierdź(Escape)',command=lambda:zamknij_okienko_zastosuj_zmiany(event))
        guzik_cofaj.config(font=self.czcionka_small)
        guzik_potwierdz.config(font=self.czcionka_small)

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
