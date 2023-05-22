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
        self.watek_zakoncz_minutnika=False
        self.pasekstanu=None

        #main
        print('okna readonly')
        print('sprawdzić czy pokazuje tylko najrzadziej losowane')
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
        self.zapisz_ustawienia_programu()
        self.logika.zamknij()
        self.pasekstanu.zamknij()
        self.okno.destroy()

    def wczytaj_ustawienia_programu(self):
        "z pliku ustawienia.xml"
        #ust=KU.Ustawienia()
        #ust.wczytaj_z_pliku()

        #return ust.zwroc_ustawienia_programu()
        return [[1920,600,70,23,16,'Arial',120],['slowka.nauka','ulice.nauka','A',100]]

    def zapisz_ustawienia_programu(self):
        "do pliku ustawienia.xml"
        roz_x=self.okno.winfo_width()
        roz_y=self.okno.winfo_height()
        czc_fam=self.czcionka_big['family']
        czc_roz_b=self.czcionka_big['size']
        czc_roz_m=self.czcionka_middle['size']
        czc_roz_s=self.czcionka_small['size']

        ust_okn_lista=[roz_x,roz_y,czc_roz_b,czc_roz_m,czc_roz_s,czc_fam,self.alarm_po_ilu_sek]

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
        #self.entry1=TK.Entry(width=70,font=self.czcionka_big,state="readonly",bg='green') #,height=20)
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
        self.okno.bind("<KeyPress-F1>",self.pokaz_pomoc)
        self.okno.bind("<Control-Key-0>",self.cofnij_ilosc_wylos_biez_wpisu_ok)

        self.okno.bind("<Control-Key-s>",self.szukaj_wpisow_ok)
        self.okno.bind("<Control-Key-e>",self.edytuj_wpis_ok)
        self.okno.bind("<Control-Key-d>",self.dodaj_wpis_ok)
        self.okno.bind("<Control-Key-k>",self.kasuj_wpis_ok)
        self.okno.bind("<Control-Key-o>",self.okienko_wpisy_ok)

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
                if self.watek_zakoncz_minutnika:
                    return
                #self.pasek.ustaw(ktory=2,tresc='Zacząłem '+str(odliczone)+' sekund temu')
                self.pasekstanu.ustaw(ktory=2,tresc='Zacząłem '+konwertuj(odliczone))
                if self.alarm_po_ilu_sek==odliczone:
                    self.pasekstanu.ustaw(ktory=1,tresc='--KONIEC JUŻ--',na_ile_sek=5)
                    self.alarmuj_dzwiekiem("clock-strike.wav")
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
        print('fun_spacja',self.logika.biezacy_wpis)
        print('fun_spacja2',self.logika.rodzaj_biezacego_wpisu)
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


    def okienko_wpisy_ok(self,event):
        "wspólne okienko dla f.edytujących"
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

    def szukaj_wpisow_ok(self,event):
        "szukanie wpisów"
        print('f.szukaj_wpisow_ok')

    def kasuj_wpis_ok(self,event):
        "kasuj wpis"
        print('f.kasuj_wpis_ok')

    def edytuj_wpis_ok(self,event):
        "edycja wpisu"
        def zamknij_okienko_zastosuj(event):
            "anulowanie zmian lub zastosowanie i zamykanie okna"
            if self.logika.rodzaj_biezacego_wpisu=='' and self.entry2.get()=='':
                #print('stwierdzam ze ulica')
                #print('KONU',wpis1.get(),wpis3.get(),wpis4.get())
                if wpis1.get()!='' and wpis3.get()!='' and wpis4.get()!='':
                    #print('U są !=')
                    nowszy=KL.KWU(wpis1.get(),wpis3.get(),int(wpis4.get()))
                    #print('Unowszy=',nowszy)
                    if starszy!=nowszy:
                        print('--- udana podmiana---')
                        #print('Unowszy',nowszy)
                        self.logika.zmien_wpis(starszy,nowszy)
                        self.logika.biezacy_wpis=nowszy
                    #print('Upoprawiony wpis to',wpis1.get()) #KL.KWU(wpis1.get()
                    self.entry1.delete(0,TK.END)
                    self.entry1.insert(0,self.logika.biezacy_wpis.pierwszy)
                    self.entry2.delete(0,TK.END)
                    self.logika.rodzaj_biezacego_wpisu=''
                else:
                    print('---niemożna podmienić na puste---')
            else:
                #print('stwierdzam ze slowko')
                #print('KONS',wpis1.get(),wpis2.get(),wpis3.get(),wpis4.get())
                if wpis1.get()!='' and wpis2.get()!='' and wpis3.get()!='' and wpis4.get()!='':
                    #print('S są !=')
                    nowszy=KL.KWS(wpis1.get(),wpis2.get(),wpis3.get(),int(wpis4.get()))
                    #print('Snowszy=',nowszy)
                    #print('Spoprawiony wpis to',wpis1.get()) #KL.KWU(wpis1.get()
                    if starszy!=nowszy:
                        print('--- udana podmiana---')
                        #print('Snowszy',nowszy)
                        self.logika.zmien_wpis(starszy,nowszy)
                        self.logika.biezacy_wpis=nowszy
                    #wczytaj w wpis12
                    self.entry1.delete(0,TK.END)
                    self.entry1.insert(0,self.logika.biezacy_wpis.pierwszy)
                    self.entry2.delete(0,TK.END)
                    self.entry2.insert(0,self.logika.biezacy_wpis.drugi)
                    self.logika.rodzaj_biezacego_wpisu=''
                else:
                    print('---niemożna podmienić na puste---')

            #print()
            okienko.destroy()

        okienko=TK.Toplevel(self.okno)
        okienko.title('Edycja wpisu')
        okienko.geometry('+350+300')
        okienko.bind("<KeyPress-Escape>",zamknij_okienko_zastosuj)

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

        ilosci=tuple(range(0,self.logika.biezacy_wpis.ile_razy_wylos+1))
        wpis4['values']=ilosci
        #print('ilosci',ilosci)
        wpis4.current(self.logika.biezacy_wpis.ile_razy_wylos)

        #print('biezacy',self.logika.biezacy_wpis)
        starszy=self.logika.biezacy_wpis

        if self.logika.rodzaj_biezacego_wpisu=='' and self.entry2.get()=='':
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

        podpis1.grid()
        wpis1.grid()
        podpis2.grid()
        wpis2.grid()
        podpis3.grid()
        wpis3.grid()
        podpis4.grid()
        wpis4.grid()
        #koniec f.edytuj_wpis_ok


    def dodaj_wpis_ok(self,event):
        "dodaj wpis"
        print('f.dodaj_wpis_ok')


    '''
        def anulowanie(event=None):
            okienko.destroy()
        def aktualizacja_wpisu(ktory,zm_wpisow):
            ""
            print('aktualizacja_wpisu',ktory,zm_wpisow.get())
            print('aktualny wpis=',wpis1.get(),wpis2.get(),wpis3.get(),wpis4.get())
            nowy_wpis=KL.KWS(wpis1.get(),wpis2.get(),wpis3.get(),int(wpis4.get()))
            print('nowy_wpis',nowy_wpis)
            ktory_stary=wyniki_szukania.curselection()
            stary_wpis=wyniki_szukania.get(ktory_stary)[3:]
            stary_wpis=KL.KWS.str_do_WpisSlowko(stary_wpis)
            print('stary_wpis',stary_wpis)
            #podmieniony
            print('TYPY',type(stary_wpis),type(nowy_wpis))
            print('nowy_wpis2',type(nowy_wpis),nowy_wpis)
            #print('podmiana',self.logika.zmien_wpis(stary_wpis,nowy_wpis))
            #pokaz w wyniki_szukania
            #wyniki_szukania.delete(0,TK.END)
            #wyniki_szukania.insert(1,'---'+str(nowy_wpis))

        def zaznaczony_wpis(event):
            '''
        #jeśli wybor_slowko_ulica.get=='slowka':
        #    pokaz aktualny we wpis1-4
        #jeśli wybor_slowko_ulica.get=='ulice':
            #    pokaz aktualny w wpis1,3,4
    '''
            print('zaznaczony_wpis')
            ktory=wyniki_szukania.curselection()
            wpis_tmp=wyniki_szukania.get(ktory)
            wpis_tmp=wpis_tmp[3:]
            print('wpis_tmp=',wpis_tmp,'_')

            if wybor_slowko_ulica.get()=='slowka':
                jak=KL.KWS.czy_str_jest_klasy_WpisSlowko(wpis_tmp)
                print('jakS',jak)
                wpis=KL.KWS.str_do_WpisSlowko(wpis_tmp)
                print('wpisS',wpis)
                print('wpis.pierwszy=',wpis.pierwszy,'_')
                wpis1.delete(0,TK.END)
                wpis1.insert(0,wpis.pierwszy)
                wpis2.delete(0,TK.END)
                wpis2.insert(0,wpis.drugi)
                wpis3.delete(0,TK.END)
                wpis3.insert(0,wpis.tryb)
                wpis4.delete(0,TK.END)
                wpis4.insert(0,wpis.ile_razy_wylos)

            elif wybor_slowko_ulica.get()=='ulice':
                jak=KL.KWU.czy_str_jest_klasy_WpisUlica(wpis_tmp)
                print('jakU',jak)
                wpis=KL.KWU.str_do_WpisUlica(wpis_tmp)
                print('wpisU',wpis)
                wpis1.delete(0,TK.END)
                wpis1.insert(0,wpis.pierwszy)
                wpis2.delete(0,TK.END)
                wpis3.delete(0,TK.END)
                wpis3.insert(0,wpis.tryb)
                wpis4.delete(0,TK.END)
                wpis4.insert(0,wpis.ile_razy_wylos)

            else:
                raise Exception('coś innego?')

        def zmiana_radio(event=None):
            '''
            #jak ulice:
            #    czyść i wylacz wpis2
            #    podpis1:Nazwa Ulicy
            #    podpis2:""
            #jak slowka:
            #    wlacz wpis2
            #    podpis1:Angielskie
            #    podpis2:Polskie
            #zawsze:
            #    czysc wyniki_szukania
            #    czysc wpis1-4
    '''
            #print("zmiana_radio",wybor_slowko_ulica.get(),'_')
            if wybor_slowko_ulica.get()=='ulice':
                wpis2.config(text='')
                wpis2.config(state=TK.DISABLED)
                podpis1.config(text='Nazwa Ulicy:')
                podpis2.config(text='')
            else:
                wpis2.config(state=TK.NORMAL)
                podpis1.config(text='Angielskie:')
                podpis2.config(text='Polskie:')
            wyniki_szukania.delete(0,TK.END)
            wpis1.delete(0,TK.END)
            wpis2.delete(0,TK.END)
            wpis3.delete(0,TK.END)
            wpis4.delete(0,TK.END)

        def kasowanie(event=None):
            '''
            #warunki kasowania:
            #    jeśli są w wpis1-4(slowko) lub wpis1,3-4(ulica)

            #po skasowaniu:
            #    czysc wpis1-4
            #    aktualizacja wyniki_szukania
    '''
            ktory=wyniki_szukania.curselection()
            print('ktoryKASUJ',ktory)
            if ktory!=():
                wpis_tmp=wyniki_szukania.get(ktory[0])
                wpis_tmp=wpis_tmp[3:]
                print('kasuj_wpis',wpis_tmp,'_')
                print('wybor_slowko_ulica',wybor_slowko_ulica.get())
                if wybor_slowko_ulica.get()=='slowka':
                    wynik=self.logika.kasuj_wpis(KL.KWS.str_do_WpisSlowko(wpis_tmp))
                    if wynik:
                        print('skasowane słówko. sprawdź')
                        print('aktualizujS wyniki_szukania')
                    else:
                        print('nieudało się skasować słówka')
                elif wybor_slowko_ulica.get()=='ulice':
                    wynik=self.logika.kasuj_wpis(KL.KWU.str_do_WpisUlica(wpis_tmp))
                    if wynik:
                        print('skasowana ulica. sprawdź')
                        print('aktualizujU wyniki_szukania')
                    else:
                        print('nieudało się skasować ulicy')

            else:
                print('---brak zaznaczeń do kasowania---')

        def aktualizuj_wyniki_szukania(event):
            ""
            wyniki_szukania.delete(0,TK.END)

            wyniki_szukania.insert(1,'9859438598345')

        def szukanie(event=None):
            '''
            #wielkość znaków ustandaryzować jakoś
    '''
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

        def dodawanie(event=None):
            '''
            #warunki:
            #    wyniki_szukania puste
            #    wybor_slowko_ulica=='slowka':
            #        wpisanie we wpis1,3-4
            #    wybor_slowko_ulica=='ulice':
            #        wpisanie we wpis1-4
    '''
            print('dodawanie')
            if wybor_slowko_ulica.get()=='slowka':
                a=wpis1.get()
                b=wpis2.get()
                c=wpis3.get()
                d=wpis4.get()
                print('dodaj',a,b,c,d)
                udane=self.logika.dodaj_wpis(KL.KWS(a,b,c,int(d)))
                if udane:
                    print('dodało się.sprawdz')
                    wpis1.delete(0,TK.END)
                    wpis2.delete(0,TK.END)
                    wpis3.delete(0,TK.END)
                    wpis4.delete(0,TK.END)
                else:
                    print('no coś nie')


        okienko=TK.Toplevel(self.okno,)
        okienko.title('Dodawanie/Edycja/Szukanie/Kasowanie')
        okienko.geometry('+350+300')
        wybor_slowko_ulica=TK.StringVar(okienko)
        if self.logika.procent_slowek_reszta_ulic==0:
            wybor_slowko_ulica.set('ulice')
        else:
            wybor_slowko_ulica.set('slowka')

        radio1=TK.Radiobutton(okienko,text='Słówka',variable=wybor_slowko_ulica,value='slowka',font=self.czcionka_small)
        radio2=TK.Radiobutton(okienko,text='Ulica',variable=wybor_slowko_ulica,value='ulice',font=self.czcionka_small)
        okienko.bind_class("Radiobutton","<ButtonRelease>",zmiana_radio)
        #print('wybor_slowko_ulica',wybor_slowko_ulica.get(),'_')

        napis1=TK.Label(okienko,text="Wpisz tutaj (przynajmniej 3 znaki):",font=self.czcionka_small)

        pole_szukania=TK.Entry(okienko,font=self.czcionka_small,width=30)
        pole_szukania.bind("<Return>",szukanie)
        pole_szukania.focus_set()

        wyniki_szukania=TK.Listbox(okienko,font=self.czcionka_small,width=50,height=17)
        wyniki_szukania.bind("<<ListboxSelect>>",zaznaczony_wpis)


        zm_wpisow0=TK.StringVar()
        zm_wpisow0.trace("w",lambda name,index,mode,zm_wpisow0=zm_wpisow0:aktualizacja_wpisu(0,zm_wpisow0))
        zm_wpisow1=TK.StringVar()
        zm_wpisow1.trace("w",lambda name,index,mode,zm_wpisow1=zm_wpisow1:aktualizacja_wpisu(1,zm_wpisow1))
        zm_wpisow2=TK.StringVar()
        zm_wpisow2.trace("w",lambda name,index,mode,zm_wpisow2=zm_wpisow2:aktualizacja_wpisu(2,zm_wpisow0))
        zm_wpisow3=TK.StringVar()
        zm_wpisow3.trace("w",lambda name,index,mode,zm_wpisow3=zm_wpisow3:aktualizacja_wpisu(3,zm_wpisow1))
        podpis1=TK.Label(okienko,text='Angielskie:',font=self.czcionka_small)
        wpis1=TK.Entry(okienko,font=self.czcionka_small,textvariable=zm_wpisow0)
        podpis2=TK.Label(okienko,text='Polskie:',font=self.czcionka_small)
        wpis2=TK.Entry(okienko,font=self.czcionka_small,textvariable=zm_wpisow1)
        podpis3=TK.Label(okienko,text='Tryb:',font=self.czcionka_small)
        wpis3=TTK.Combobox(okienko,font=self.czcionka_small,textvariable=zm_wpisow2)
        podpis4=TK.Label(okienko,text='ile_razy_wylosowany:',font=self.czcionka_small)
        wpis4=TK.Entry(okienko,font=self.czcionka_small,textvariable=zm_wpisow3)

        guzik1=TK.Button(okienko,text="Dodaj Wpis",width=25,command=lambda:dodawanie(event))
        guzik1.config(font=self.czcionka_small)
        guzik2=TK.Button(okienko,text="Zamknij (Escape)",width=25,command=lambda:anulowanie(event))
        guzik2.config(font=self.czcionka_small)
        guzik3=TK.Button(okienko,text="Kasuj Wpis",width=25,command=lambda:kasowanie(event))
        guzik3.config(font=self.czcionka_small)

        okienko.bind("<KeyPress-Escape>",anulowanie)

        #grid-y okienka:
        radio1.grid(row=0,column=0)
        radio2.grid(row=0,column=1)
        napis1.grid(row=1,columnspan=2)
        pole_szukania.grid(row=2,column=0)
        guzik1.grid(row=2,column=1)
        wyniki_szukania.grid(row=3,rowspan=9,column=0)
        podpis1.grid(row=4,column=1)
        wpis1.grid(row=5,column=1)
        podpis2.grid(row=6,column=1)
        wpis2.grid(row=7,column=1)
        podpis3.grid(row=8,column=1)
        wpis3.grid(row=9,column=1)
        podpis4.grid(row=10,column=1)
        wpis4.grid(row=11,column=1)
        guzik2.grid(row=12,column=0)
        guzik3.grid(row=12,column=1)'''
