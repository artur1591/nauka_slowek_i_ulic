#!/usr/bin/python3.9
'''
oddzielenie klasy Okno od klasy Logika
'''
import os as OS
import threading as TH
import time as TI
import random as RA
import tkinter as TK
import tkinter.font as FO
import tkinter.messagebox as TMS
import tkinter.ttk as TTK
import matplotlib.backends.backend_tkagg as MTLB
import matplotlib.pyplot as PPL
OS.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as PG
import klasa_pasek_stanu as KPS
import klasa_logika as KL

class Okno:
    "dlaczego ta klasa nie dziedziczy po jakieś tkinter? co mi to da?"
    def __init__(self, procent_slowek=None):
        ""
        self.rozm_x = None
        self.rozm_y = None
        self.czcionka_big = None
        self.czcionka_middle = None
        self.czcionka_small = None
        self.czcionka_family = None
        self.alarm_po_ilu_sek = None
        self.plik_minutnika = ''
        self.watki_zakoncz = False
        self.pasekstanu = None

        self.losowa_kolejnosc_slowka=False
        self.indeks_pierwszego=0

        #main
        self.komunikaty_poczatkowe()
        ust_okn,ust_log=self.wczytaj_ustawienia_programu()
        self.okno=TK.Tk()
        self.wpisz_ustawienia_w_klase_okno(ust_okn)

        if not procent_slowek is None:
            ust_log[3]=procent_slowek
        self.logika=KL.Logika(ust_log)

        self.zbuduj_okno(self.logika.komunikat_bledu)

        self.fun_spacja()

        self.okno.mainloop()


    def komunikaty_poczatkowe(self):
        "czasem coś chce się powiedzieć na początku programu"
        print('---Aby zobaczyć listę skrótów klawiszowych naciśnij F1---')
        #print('import Pmw sprawdzić widżety')

    def komunikaty_koncowe(self):
        "czasem coś chce się powiedzieć na końcu programu"
        #print('...koniec programu nauka_slowek_i_ulic')

        if not self.logika.dopiski.ulice_status==KL.dopiski_status.UKRYJ_LABEL:
            print('---są ulice do dopisania. sprawdź plik:',self.logika.dopiski.ulice_plik)
        if not self.logika.dopiski.slowka_status==KL.dopiski_status.UKRYJ_LABEL:
            print('---są słówka do dopisania. sprawdź plik:',self.logika.dopiski.slowka_plik)


    def zamknij(self,_=None):
        "pyta czy zamknąć i zamyka"
        if TMS.askyesno(title="--uwaga--",message="Zamknąć?"):
            self.watki_zakoncz=True
            if not self.logika.komunikat_bledu:
                self.zapisz_ustawienia_programu()
            self.logika.zamknij()
            self.pasekstanu.zamknij()
            self.okno.quit()
            self.komunikaty_koncowe()

    @staticmethod
    def wczytaj_ustawienia_programu():
        '''
        będzie z pliku ustawienia.xml

        alarm_po_ilu_sek jeśli 0 to minutnik nie startuje
        ostatni argument(9ty) ust_okn określa:
            czy losować kolejność pierwszy/drugi słówek
                (True- losuje, False pokazuje pierwszy najpierw)
        '''
        #return ust.zwroc_ustawienia_programu()
        #ust_okn=[1920,600,70,23,16,'Arial',3,'kimwilde.mp3',False]
        #ust_okn=[1920,600,70,23,16,'Arial',0,'',False]
        #ust_okn=[1920,600,70,23,16,'Arial',30,'kimwilde.mp3',True]
        #ust_okn=[1920,600,70,23,16,'Arial',3,'data-scaner.wav',True]
        #ust_okn=[1920,600,70,23,16,'Arial',3,'data-scaner.wav',True]
        #ust_okn=[1920,560,70,23,16,'Arial',120,'kimwilde.mp3',False]
        #ust_okn=[1920,560,70,23,16,'Arial',0,'dwsample.ogg',False]
        ust_okn=[1920,560,70,23,16,'Arial',1200,'dwsample.ogg',True]
        ust_log=['ulice.nauka','slowka.nauka','A',50,'dopiski_ulice','dopiski_slowka']
        return [ust_okn,ust_log]

    def zapisz_ustawienia_programu(self):
        "do pliku ustawienia.xml"
        roz_x=self.okno.winfo_width()
        roz_y=self.okno.winfo_height()
        czc_roz_b=self.czcionka_big['size']
        czc_roz_m=self.czcionka_middle['size']
        czc_roz_s=self.czcionka_small['size']
        czc_fam=self.czcionka_big['family']
        ala_ile=self.alarm_po_ilu_sek
        ala_pli=self.plik_minutnika
        los_kol=self.losowa_kolejnosc_slowka

        ust_okn_lista=[roz_x,roz_y,
                    czc_roz_b,czc_roz_m,czc_roz_s,czc_fam,
                    ala_ile,ala_pli,los_kol]

        plik_uli=self.logika.plik_ulice
        plik_slo=self.logika.plik_slowka
        tryb=self.logika.biezacy_tryb
        procent=self.logika.procent_slowek_reszta_ulic

        ust_log_lista=[plik_uli,plik_slo,tryb,procent]

        wynik=[ust_okn_lista,ust_log_lista]
        print(wynik)

    def sprawdz_obecnosc_pliku_minutnika(self):
        '''
        jeśli brakuje:
            return False

        jeśli jest:
            return True

        sprytniej to zrobić. domknięciem?
        '''
        #print('f.sprawdz_obecnosc_pliku_minutnika:',self.plik_minutnika)
        if KL.OS.path.exists(self.plik_minutnika):
            return True
        return False

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
        self.losowa_kolejnosc_slowka =ust_okn[8]

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
        self.okno.rowconfigure(2,weight=2)
        self.okno.rowconfigure(3,weight=1)
        self.okno.rowconfigure(4,weight=2)
        self.okno.columnconfigure(0,weight=1)

        self.dopiski_ulice_sa=TK.Label(font=self.czcionka_small,bg='red')
        self.dopiski_ulice_sa.grid(row=0,sticky='NW',ipady=0,ipadx=0,pady=0,padx=0)
        if len(self.logika.dopiski.ulice_lista)==0:
            self.dopiski_ulice_sa.grid_forget()
        self.dopiski_ulice_sa.bind("<Button-1>",self.klikniety_dopiski_ulice)

        najechany_u=lambda e:self.dopiski_ulice_sa.config(bg='white',
                        text='---kliknij aby dopisać---')
        opuszczanie_u=lambda e:self.dopiski_ulice_sa.config(bg='red')
        self.dopiski_ulice_sa.bind("<Enter>",func=najechany_u)
        self.dopiski_ulice_sa.bind("<Leave>",func=opuszczanie_u)

        self.dopiski_slowka_sa=TK.Label(font=self.czcionka_small,bg='red')
        self.dopiski_slowka_sa.grid(row=1,sticky='NW',ipady=0,ipadx=0,pady=0,padx=0)
        if len(self.logika.dopiski.slowka_lista)==0:
            self.dopiski_slowka_sa.grid_forget()
        self.dopiski_slowka_sa.bind("<Button-1>",self.klikniety_dopiski_slowka)

        najechany_s=lambda e:self.dopiski_slowka_sa.config(bg='white',
                        text='---kliknij aby dopisać---')
        opuszczanie_s=lambda e:self.dopiski_slowka_sa.config(bg='red')
        self.dopiski_slowka_sa.bind("<Enter>",func=najechany_s)
        self.dopiski_slowka_sa.bind("<Leave>",func=opuszczanie_s)

        self.napis_ilosc_slowek_ulic=TK.Label(font=self.czcionka_small)
        self.aktualizuj_napis_ilosc_wpisow()
        self.napis_ilosc_slowek_ulic.grid(row=0,sticky='NE',ipady=0,ipadx=0,pady=0,padx=0)

        self.napis1=TK.Label(text="słowo1",font=self.czcionka_small)
        self.napis1.grid(row=1,sticky='N',ipady=0,pady=0)

        self.entry1_tresc=TK.StringVar()
        self.entry2_tresc=TK.StringVar()

        self.entry1=TK.Entry(width=70,font=self.czcionka_big,textvariable=self.entry1_tresc,
                    state=TK.DISABLED,disabledbackground='green',disabledforeground='black')
        self.entry1.grid(row=2)
        self.napis2=TK.Label(text="słowo2",font=self.czcionka_small)
        self.napis2.grid(row=3)

        self.entry2=TK.Entry(width=70,font=self.czcionka_big,textvariable=self.entry2_tresc,
                    state=TK.DISABLED,disabledbackground='green',disabledforeground='black')
        self.entry2.grid(row=4)

        self.pasekstanu=KPS.Pasekstanu(self.okno,self.czcionka_small)
        self.pasekstanu.grid(row=5,sticky='SWE')
        self.sajzgrip=TTK.Sizegrip(self.okno)
        self.sajzgrip.grid(row=5,sticky='SE')
        self.pasekstanu.ustaw(ktory=1,tresc="Jestem",na_ile_sek=3)
        #print('tryb=',self.logika.biezacy_tryb)
        self.pasekstanu.ustaw(ktory=0,tresc="Tryb: "+self.logika.biezacy_tryb)

        if potencjalny_blad!='':
            #jest komunikat_bledu więc niestartuj programu
            self.entry1_tresc.set(potencjalny_blad)
            self.entry1_tresc.set(potencjalny_blad)
            print('---komunikat_bledu:',potencjalny_blad,'---')
        else:
            if self.alarm_po_ilu_sek>0 and self.sprawdz_obecnosc_pliku_minutnika():
                self.wlacz_minutnik()
            elif self.plik_minutnika=='' or self.sprawdz_obecnosc_pliku_minutnika():
                self.pasekstanu.ustaw(ktory=2,tresc="---minutnik wyłączony---")
            else:
                self.pasekstanu.ustaw(ktory=2,tresc="---brakuje pliku minutnika---")

        self.fun_dopiski_okno()

        #bindy:
        self.okno.bind("<space>",self.fun_spacja)
        self.okno.bind("<KeyPress-Escape>",self.zamknij)
        self.okno.protocol("WM_DELETE_WINDOW",self.zamknij)
        self.okno.bind("<KeyPress-F1>",self.pokaz_pomoc)
        self.okno.bind("<Control-Key-0>",self.confnij_ilosc_wylos_biez_wpisu_okno)

        self.okno.bind("<KeyPress-F2>",self.szukaj_wpisow_okno)
        self.okno.bind("<KeyPress-F3>",self.dodaj_wpis_okno)
        self.okno.bind("<KeyPress-F4>",self.edytuj_wpis_okno)

        self.okno.bind("<Control-Key-a>",lambda event:self.ustaw_tryb_biezacego_wpisu('A'))
        self.okno.bind("<Control-Key-b>",lambda event:self.ustaw_tryb_biezacego_wpisu('B'))
        self.okno.bind("<Control-Key-c>",lambda event:self.ustaw_tryb_biezacego_wpisu('C'))
        self.okno.bind("<Control-Key-t>",self.zmien_biezacy_tryb)
        self.okno.bind("<Control-Key-p>",self.eksportuj_jako_pdf_okno)
        self.okno.bind("<Control-Key-s>",self.pokaz_wykres_statystyk)
        #też Escape
        self.okno.bind("<Control-Key-q>",self.zamknij)
        self.okno.bind("<Control-Key-z>",self.zerowanie_wpisow)

        self.okno.bind("<Control-KP_Add>",lambda event:self.czcionke_zmien('+'))
        self.okno.bind("<Control-KP_Subtract>",lambda event:self.czcionke_zmien('-'))
        self.okno.bind("<Control-KP_Multiply>",lambda event:self.czcionke_zmien('*'))

    def klikniety_dopiski_ulice(self,_):
        ""
        ile_pominietych=0
        status=self.logika.dopiski.ulice_status
        #print('f.klikniety_dopiski_ulice',status)

        if status==KL.dopiski_status.WCZYTALEM_W_LISTE_DOPISKI:
            #print('można dopisywać do lista_ulic i skasować dopiski_ulice')
            ulice_lista=self.logika.dopiski.ulice_lista
            #print('ulice_lista:',ulice_lista)
            for ulica in ulice_lista:
                nowa=KL.KWU(ulica)
                if self.logika.szukaj_wpis(ulica,typ='u') is False:
                    #print('dodaje brakujący wpis:',nowa)
                    self.logika.dodaj_wpis(nowa)
                else:
                    print('---jest już ulica:',nowa,'pomijam ją')
                    ile_pominietych+=1

            #print('teraz kasuje plik:',self.logika.dopiski.ulice_plik)
            OS.remove(self.logika.dopiski.ulice_plik)

            self.logika.dopiski.ulice_status=KL.dopiski_status.DOPISALEM_DO_LISTY_WPISOW
            self.pasekstanu.ustaw(ktory=1,tresc='pominąłem ulic:'+str(ile_pominietych),na_ile_sek=5)

    def klikniety_dopiski_slowka(self,_):
        ""
        ile_pominietych=0
        status=self.logika.dopiski.slowka_status
        print('f.klikniety_dopiski_slowka',status)

        if status==KL.dopiski_status.JEZYK_WYKRYTY:
            #print('można dopisywać do lista_slowek i skasować dopiski_slowka')
            slowka_lista=self.logika.dopiski.slowka_lista
            print('slowka_lista:',slowka_lista)
            for slowko in slowka_lista:
                #print('slowko',slowko[1],' jezyk=',slowko[0])
                nowe=None
                if slowko[0]=='en':
                    nowe=KL.KWS(slowko[1],'...')
                else:
                    nowe=KL.KWS('...',slowko[1])
                #print('nowe',nowe)

                if self.logika.szukaj_wpis(slowko[1],typ='s') is False:
                    print('dodaje brakujący wpis:',nowe)
                    self.logika.dodaj_wpis(nowe)
                else:
                    print('---jest już słówko:',nowe,'pomijam je')
                    ile_pominietych+=1

            #print('teraz kasuje plik:',self.logika.dopiski.slowka_plik)
            OS.remove(self.logika.dopiski.slowka_plik)

            self.logika.dopiski.slowka_status=KL.dopiski_status.DOPISALEM_DO_LISTY_WPISOW
            self.pasekstanu.ustaw(ktory=1,
                        tresc='pominąłem słówek:'+str(ile_pominietych),na_ile_sek=5)

    def fun_dopiski_okno(self):
        '''
        jeśli istnieje plik dopiski z niezerową zawartością to:
            pokaz ikonkę do kliknięcia w oknie
        '''
        #print('f.fun_dopiski_okno')
        def fun_dopiski_okno_watek():
            ""
            #print('f.fun_dopiski_okno_watek')
            while not self.logika.dopiski.zakoncz_watki:
                uli_sta=self.logika.dopiski.ulice_status
                slo_sta=self.logika.dopiski.slowka_status
                #print('ulice_status=',uli_sta,'slowka_status=',slo_sta)

                if uli_sta==KL.dopiski_status.WCZYTALEM_W_LISTE_DOPISKI:
                    napis='Jest ulic do dopisania: '+str(len(self.logika.dopiski.ulice_lista))
                    self.dopiski_ulice_sa.config(text=napis)

                if slo_sta==KL.dopiski_status.WCZYTALEM_W_LISTE_DOPISKI:
                    napis='Jest słówek do dopisania: '+str(len(self.logika.dopiski.slowka_lista))
                    self.dopiski_slowka_sa.config(text=napis)

                if slo_sta==KL.dopiski_status.WYKRYWAM_JEZYK:
                    napis='Wykrywam język dla nowych słówek...'
                    self.dopiski_slowka_sa.config(text=napis)

                if slo_sta==KL.dopiski_status.JEZYK_WYKRYTY:
                    ile_eng=0
                    ile_pol=0

                    for ktory in self.logika.dopiski.slowka_lista:
                        if ktory[0]=='en':
                            ile_eng+=1
                        else:
                            ile_pol+=1

                    napis='Nowych słówek:'+str(len(self.logika.dopiski.slowka_lista))+' '
                    napis+='ENG:'+str(ile_eng)+' '
                    napis+='POL:'+str(ile_pol)
                    self.dopiski_slowka_sa.config(text=napis)

                #jak są wpisy dodane. pokazuje info na 3sek i ukrywa
                if uli_sta==KL.dopiski_status.DOPISALEM_DO_LISTY_WPISOW:
                    napis='Dopisałem Nowe Ulice'
                    self.dopiski_ulice_sa.config(text=napis)
                    TI.sleep(3)
                    uli_sta=KL.dopiski_status.UKRYJ_LABEL

                if slo_sta==KL.dopiski_status.DOPISALEM_DO_LISTY_WPISOW:
                    napis='Dopisałem Nowe Słówka'
                    self.dopiski_slowka_sa.config(text=napis)
                    TI.sleep(3)
                    slo_sta=KL.dopiski_status.UKRYJ_LABEL

                #ukrywanie Labelów
                if uli_sta==KL.dopiski_status.UKRYJ_LABEL:
                    self.dopiski_ulice_sa.grid_forget()

                if slo_sta==KL.dopiski_status.UKRYJ_LABEL:
                    self.dopiski_slowka_sa.grid_forget()

                if slo_sta==KL.dopiski_status.UKRYJ_LABEL and uli_sta==KL.dopiski_status.UKRYJ_LABEL:
                    self.logika.dopiski.zakoncz_watki=True
                    #print('dopiski.zakoncz_watki=',self.logika.dopiski.zakoncz_watki)
                TI.sleep(1)

        watek=TH.Thread(target=fun_dopiski_okno_watek,daemon=True).start()
        #koniec f.fun_dopiski_okno

    def eksportuj_jako_pdf_okno(self,_):
        '''
        3 argumenty:
            lista wpisów,
            nazwa dla danych
            nazwa pliku wynikowego

        zwraca True jak czcionka jest i udalo sie
        zwraca komunikat bledu jak nieposzlo
        '''
        def wykonaj_pdfa(ktory):
            "jako zewnętrzna funkcja bo argumenty daje i wynik pobiera"
            wynik=True

            if ktory==plik_ulice_nazwa:
                wynik=self.logika.eksportuj_jako_pdf(self.logika.lista_ulic,
                                    plik_ulice_podtytul,plik_ulice_nazwa)
            elif ktory==plik_slowka_nazwa:
                wynik=self.logika.eksportuj_jako_pdf(self.logika.lista_slowek,
                                    plik_slowka_podtytul,plik_slowka_nazwa)

            if not wynik is True:
                print('komunikat_bledu: ',wynik)
                dlugosc_bledu=len('BŁĄD: '+wynik)
                guzik_ulice.config(text='BŁĄD: '+wynik)
                guzik_ulice.config(width=dlugosc_bledu)
                guzik_slowka.config(text='BŁĄD: '+wynik)
                guzik_slowka.config(width=dlugosc_bledu)


        plik_ulice_nazwa='ulice.pdf'
        plik_ulice_podtytul='ulice.nauka'

        plik_slowka_nazwa='slowka.pdf'
        plik_slowka_podtytul='slowka.nauka'

        okienko=TK.Toplevel(self.okno,bg='grey')
        okienko.title('Generowanie plików pdf')
        okienko.rowconfigure(0,weight=1)
        okienko.columnconfigure(0,weight=1)
        okienko.bind("<KeyPress-Escape>",lambda event:okienko.destroy())
        okienko.geometry('+350+300')
        okienko.wm_iconphoto(False,TK.PhotoImage(file='logo2.png'))
        okienko.protocol("WM_DELETE_WINDOW",lambda:okienko.destroy())

        guzik_ulice=TK.Button(okienko,text='Generuj: '+plik_ulice_nazwa,width=20,
            font=self.czcionka_middle)
        guzik_ulice['command']=lambda co=plik_ulice_nazwa:wykonaj_pdfa(co)

        guzik_slowka=TK.Button(okienko,text='Generuj: '+plik_slowka_nazwa,width=20,
            font=self.czcionka_middle)
        guzik_slowka['command']=lambda co=plik_slowka_nazwa:wykonaj_pdfa(co)

        guzik_ulice.grid()
        guzik_slowka.grid()


    def pokaz_wykres_statystyk(self,_):
        "w klasie Statystyki jest m.zwracająca dane do wykresu"

        def przygotuj_dane_dla_wykresy():
            ""
            daty_wej=list()
            ilosci_wej_u=list()
            ilosci_wej_s=list()
            ile_dat_bedzie=len(self.logika.stats.biezace_statystyki_trojca)

            for trojca in self.logika.stats.biezace_statystyki_trojca:
                ilosci_wej_u.append(trojca[1])
                ilosci_wej_s.append(trojca[2])
                if ile_dat_bedzie>=12:
                    daty_wej.append(trojca[0][8:])
                elif ile_dat_bedzie>6 and ile_dat_bedzie<12:
                    daty_wej.append(trojca[0][5:])
                else:
                    #jak do 6sztuk to cały format daty
                    daty_wej.append(trojca[0])

            return daty_wej,ilosci_wej_u,ilosci_wej_s

        wspolny_kolor_tla='seagreen'
        okienko=TK.Toplevel(self.okno,bg=wspolny_kolor_tla)
        okienko.rowconfigure(0,weight=1)
        okienko.columnconfigure(0,weight=1)
        okienko.rowconfigure(1,weight=1)
        okienko.columnconfigure(1,weight=1)
        okienko.rowconfigure(2,weight=1)
        okienko.columnconfigure(2,weight=1)
        okienko.bind("<KeyPress-Escape>",lambda event:okienko.destroy())
        okienko.geometry('740x672+350+300')
        ile_dni=len(self.logika.stats.biezace_statystyki_trojca)
        okienko.title('ile dni na wykresie: '+str(ile_dni))
        okienko.wm_iconphoto(False,TK.PhotoImage(file='logo2.png'))
        okienko.protocol("WM_DELETE_WINDOW",okienko.destroy)

        napis_tresc=self.logika.stats.podsumowanie()
        #print('napis_tresc',napis_tresc)

        napis=TK.Label(okienko,font=self.czcionka_small,text=napis_tresc,bg=wspolny_kolor_tla)
        napis.pack()

        PPL.figure(edgecolor='red')

        fig,osie=PPL.subplots()
        fig.patch.set_facecolor(wspolny_kolor_tla)

        fig.text(0.55,0.35,'Nauka Słówek',fontsize=65,
                    color='white',ha='center',alpha=0.25,rotation=25)

        plotno=MTLB.FigureCanvasTkAgg(fig,master=okienko)
        plotno.get_tk_widget().pack(side="top",fill="both",expand=True)

        toolbar=MTLB.NavigationToolbar2Tk(plotno,okienko,pack_toolbar=False)
        toolbar.update()
        toolbar.pack(side='left')

        guzik=TK.Button(okienko,text="Zamknij (lub klawisz Escape)",command=okienko.destroy)
        guzik.pack(side='right')

        daty_wej,ilosci_wej_u,ilosci_wej_s=przygotuj_dane_dla_wykresy()

        osie.plot(daty_wej,ilosci_wej_u,'-',marker='D',color='black',lw=3)
        osie.plot(daty_wej,ilosci_wej_s,'-',marker='H',color='green',lw=3)
        osie.set_xlabel('Daty')
        osie.set_ylabel('Ilości dzienne')
        osie.legend(['Ulice','Słówka'])
        osie.set_facecolor('grey')


    def aktualizuj_napis_ilosc_wpisow(self):
        '''
        w prawym górnym rogu pokazuje ile jest słówek i ile ulic wraz z liczebnością w trybach
        aktualizowane po: dodaj_wpis,kasuj_wpis i ustaw_tryb_biezacego_wpisu
        '''
        print('f.aktualizuj_napis_ilosc_wpisow')

        dane_slowek='ilość słówek: '+str(len(self.logika.lista_slowek))+' ('
        ile_slowek_a=str(len([wpis for wpis in self.logika.lista_slowek if wpis.tryb=='A' ]))
        ile_slowek_b=str(len([wpis for wpis in self.logika.lista_slowek if wpis.tryb=='B' ]))
        ile_slowek_c=str(len([wpis for wpis in self.logika.lista_slowek if wpis.tryb=='C' ]))
        dane_slowek+='A:'+ile_slowek_a+',B:'+ile_slowek_b+',C:'+ile_slowek_c+')'


        dane_ulic='ilość ulic: '+str(len(self.logika.lista_ulic))+' ('
        ile_ulic_a=str(len([wpis for wpis in self.logika.lista_ulic if wpis.tryb=='A' ]))
        ile_ulic_b=str(len([wpis for wpis in self.logika.lista_ulic if wpis.tryb=='B' ]))
        ile_ulic_c=str(len([wpis for wpis in self.logika.lista_ulic if wpis.tryb=='C' ]))
        dane_ulic+='A:'+ile_ulic_a+',B:'+ile_ulic_b+',C:'+ile_ulic_c+')'


        self.napis_ilosc_slowek_ulic.config(text=dane_slowek+' | '+dane_ulic)

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

        guzik_zamknij=TK.Button(okienko,font=self.czcionka_small,
                            text=" Zamknij (Escape)",width=52,
                            command=lambda:anulowanie(event))

        okienko.bind("<KeyPress-Escape>",anulowanie)
        okienko.wm_iconphoto(False,TK.PhotoImage(file='logo2.png'))

        guzik1.grid(row=0,column=0)
        guzik2.grid(row=0,column=1)
        guzik3.grid(row=1,column=0)
        guzik4.grid(row=1,column=1)
        guzik_zamknij.grid(row=2,columnspan=2)

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

    @staticmethod
    def alarmuj_dzwiekiem(jaki_utwor):
        "daemon True powoduje wyłączenie dźwięku przy szybkim zamknięciu programu"
        def wlacz_play():
            "radzi sobie z wav,mp3,ogg na debianie"
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
            elif jaki_utwor.endswith('.ogg'):
                print('---plik_minutnika jest w formacie ogg---')
                PG.mixer.init()
                PG.mixer.music.load(jaki_utwor)
                PG.mixer.music.play()
            else:
                print('---plik inny niż mp3, wav, ogg---')

        watek=TH.Thread(target=wlacz_play,daemon=True)
        watek.start()

    def fun_spacja(self,_=None):
        '''
        jak jest błąd fun_spacja niewykonuje się

        jeśli self.losowa_kolejnosc_slowka włączona:
            self.indeks_pierwszego=0 mówi żeby Wpis.pierwszy był pokazany w gornym oknie
                jeśli =1 Wpis.drugi idzie w górne okno

        self.logika.rodzaj_biezacego_wpisu przyjmuje wartości:  '' 'u' 's1' 's2' False

        '''
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
            if self.losowa_kolejnosc_slowka:
                #print('losuje indeks_pierwszego')
                self.indeks_pierwszego=RA.randint(0,1)
                #print('s1.los_kol_slo',self.losowa_kolejnosc_slowka,
                #    'indeks_pierwszego',self.indeks_pierwszego)
                #print('s1.indeks_pierwszego',self.indeks_pierwszego)

            self.logika.biezacy_wpis=self.logika.wylosuj_slowko_z_inkrem()
            if self.logika.biezacy_wpis is False:
                self.ustaw_pole_tekstowe(0,"---brak słówek w trybie "+
                                            self.logika.biezacy_tryb+"---")
                self.ustaw_pole_tekstowe(1,"---brak słówek w trybie "+
                                            self.logika.biezacy_tryb+"---")
                self.logika.rodzaj_biezacego_wpisu=''
            else:
                #tutaj ustawic ktory pierwszy
                if self.indeks_pierwszego==0:
                    self.ustaw_pole_tekstowe(0,self.logika.biezacy_wpis.pierwszy)
                else:
                    self.ustaw_pole_tekstowe(0,self.logika.biezacy_wpis.drugi)
                self.czysc_pole_tekstowe(1)
                self.logika.rodzaj_biezacego_wpisu='s2'

        elif self.logika.rodzaj_biezacego_wpisu=='s2':
            #print('s2.indeks_pierwszego=',self.indeks_pierwszego)
            #tutaj ustawic ktory pierwszy
            if self.indeks_pierwszego==0:
                self.ustaw_pole_tekstowe(1,self.logika.biezacy_wpis.drugi)
            else:
                self.ustaw_pole_tekstowe(1,self.logika.biezacy_wpis.pierwszy)
            self.logika.rodzaj_biezacego_wpisu=''

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

    def confnij_ilosc_wylos_biez_wpisu_okno(self,_):
        "czasem można chcieć powtórzyć dany wpis w najbliższym obiegu losowania"
        print('cofnij_ilosc_wylos_biez_wpisu_Ok')
        print('biezacy',self.logika.biezacy_wpis)
        self.logika.cofnij_ilosc_wylos_biez_wpisu_lo()
        print('poprawiony',self.logika.biezacy_wpis)

    def zmien_biezacy_tryb(self,_):
        "przechodzi po kolej: A->B->C i powtarza"
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
            self.aktualizuj_napis_ilosc_wpisow()
        else:
            self.pasekstanu.ustaw(ktory=1,tresc='już jest ten tryb',na_ile_sek=3)

    def pokaz_pomoc(self,_):
        "taki szybki help"
        print('''-Skróty klawiszowe:
            spacja - następny wpis(lub znaczenie)
            ctrl+q/Escape - wyjście z potwierdzeniem
            ctrl+z zerowanie ilości wylosowań/trybów dla słówek/ulic
            CRUD:
                F2 szukanie wpisów
                F3 dodawanie nowych wpisów
                F4 edycja bieżącego wpisu
                ctrl+a/b/c ustaw tryb bieżącego wpisu
                ctrl+0 - cofnij ilość wylosowań bieżącego wpisu
            ctrl+p eksportuj jako pdf ulice/słówka
            ctrl+s pokaż statystyki
            ctrl+t zmień bieżący tryb
            ctrl+*/+/- zerowanie/powiększanie/zmniejszanie rozmiaru czcionki
            F1 - pokaż tą pomoc
        ''')

    @staticmethod
    def czcionke_zmien(jaka_operacja):
        "operacje to +  -   *"
        print('czcionke_zmien.operacja',jaka_operacja)


    #4 metody zarządzające wpisami
    def szukaj_wpisow_okno(self,_):
        '''
        wykorzystuje metode szukaj_wpis klasy Logika
        realizuje również kasowanie metodą kasuj_wpis klasy Logika
        oraz edycja metodą zmien_wpis klasy Logika

        '''
        print('f.szukaj_wpisow_okno. dodaj ilość wyszukanych')
        def __czysc_wyniki_szukania__():
            "po edycji potrzeba czyscic wyniki_szukania"
            print('f. __czysc_wyniki_szukania__')
            wyniki_szukania.delete(0,TK.END)

        def zamknij_okienko(_=None):
            "zamykanie Escape lub ręcznie"
            okienko.destroy()

        def edytowanie_wpisu_guzikiem():
            ""
            print('f.edytowanie_wpisu_guzikiem')
            ktory=wyniki_szukania.curselection()
            #print(wyniki_szukania.get(ktory))
            do_edycji_str=wyniki_szukania.get(ktory)[3:]
            print('do edycji:',do_edycji_str)
            print('typ',wybor_ulica.get(),wybor_slowko.get())
            wynik=self.edytuj_wpis_okno(do_edycji_str)
            print('wynik=',wynik)
            if wynik=='czysc_wyniki_szukania':
                print('ma czyscic wyniki_szukania')
                __czysc_wyniki_szukania__()

        def kasowanie_wpisu_guzikiem():
            "po skasowaniu: aktualizuj_napis_ilosc_wpisow()"
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
                    __czysc_wyniki_szukania__()
                    self.aktualizuj_napis_ilosc_wpisow()
            else:
                do_skasowania_wpis=KL.KW.str_do_wpis_slowko(do_skasowania_str)
                if do_skasowania_wpis:
                    self.logika.kasuj_wpis(do_skasowania_wpis)
                    guzik_kasuj.config(state=TK.DISABLED)
                    wyniki_szukania.delete(0,TK.END)
                    self.aktualizuj_napis_ilosc_wpisow()

            if wybrany_typ=='u':
                okienko.title('Szukanie Ulic')
            elif wybrany_typ=='s':
                okienko.title('Szukanie Słówek')

        def ustaw_szukanie_ulic():
            #print('ulica do szukania')
            wybor_ulica.set('ulice')
            wybor_slowko.set('')
            okienko.title('Szukanie Ulic')
            guzik_kasuj.config(state=TK.DISABLED)
            guzik_edytuj.config(state=TK.DISABLED)
            wyniki_szukania.delete(0,TK.END)

        def ustaw_szukanie_slowek():
            #print('slowko do szukania')
            wybor_ulica.set('')
            wybor_slowko.set('slowka')
            okienko.title('Szukanie Słówek')
            guzik_kasuj.config(state=TK.DISABLED)
            guzik_edytuj.config(state=TK.DISABLED)
            wyniki_szukania.delete(0,TK.END)

        def zaznaczony_wpis(_):
            ktory=wyniki_szukania.curselection()
            #print('zaznaczony_wpis',ktory)
            print('zaznaczony_wpis',wyniki_szukania.get(ktory))
            uzyskany_wpis=wyniki_szukania.get(ktory)[3:]
            print('uzyskany_wpis',uzyskany_wpis)
            guzik_kasuj.config(state=TK.NORMAL)
            guzik_edytuj.config(state=TK.NORMAL)

        def szukanie(_):
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
                if wybrany_typ=='u':
                    okienko.title('Szukanie Ulic')
                elif wybrany_typ=='s':
                    okienko.title('Szukanie Słówek')
            else:
                co_znalazl=self.logika.szukaj_wpis(szukany_str=pole_szukania.get(),typ=wybrany_typ)
                #print('co_znalazl',co_znalazl)
                if not co_znalazl:
                    wyniki_szukania.delete(0,TK.END)
                    wyniki_szukania.insert(TK.END,'---nic się nie znalazło---')
                    if wybrany_typ=='u':
                        okienko.title('Szukanie Ulic')
                    elif wybrany_typ=='s':
                        okienko.title('Szukanie Słówek')
                else:
                    wyniki_szukania.delete(0,TK.END)
                    #print('co_znalazl',co_znalazl)
                    if isinstance(co_znalazl,list):
                        #jak jest więcej niż 1 znalezionych
                        for ktory in enumerate(co_znalazl):
                            #print('ktory',ktory)
                            #wyniki_szukania.insert(TK.END,'---'+str(co_znalazl[ktory])+'\n')
                            wyniki_szukania.insert(ktory[0]+1,'---'+str(ktory[1]))
                            if wybrany_typ=='u':
                                okienko.title('Szukanie Ulic ('+str(len(co_znalazl))+')')
                            elif wybrany_typ=='s':
                                okienko.title('Szukanie Słówek ('+str(len(co_znalazl))+')')
                    else:
                        #jak tylko 1 jest
                        wyniki_szukania.insert(1,'---'+str(co_znalazl))
                        if wybrany_typ=='u':
                            okienko.title('Szukanie Ulic (1)')
                        elif wybrany_typ=='s':
                            okienko.title('Szukanie Słówek (1)')

        okienko=TK.Toplevel(self.okno)
        okienko.geometry('+350+300')
        okienko.wm_iconphoto(False,TK.PhotoImage(file='logo2.png'))
        okienko.bind('<KeyPress-Escape>',zamknij_okienko)
        okienko.protocol("WM_DELETE_WINDOW",zamknij_okienko)

        wybor_ulica=TK.StringVar('')
        wybor_slowko=TK.StringVar('')

        radio1=TK.Radiobutton(okienko,text='Ulice',variable=wybor_ulica,
                        command=ustaw_szukanie_ulic,value='ulice',font=self.czcionka_small)
        radio2=TK.Radiobutton(okienko,text='Słówka',variable=wybor_slowko,
                        command=ustaw_szukanie_slowek,value='slowka',font=self.czcionka_small)
        guzik_kasuj=TK.Button(okienko,text='Kasuj Wpis',state=TK.DISABLED,width=14,
                        command=kasowanie_wpisu_guzikiem,font=self.czcionka_small)
        guzik_edytuj=TK.Button(okienko,text='Edytuj Wpis',state=TK.DISABLED,width=14,
                        command=edytowanie_wpisu_guzikiem,font=self.czcionka_small)


        if self.logika.procent_slowek_reszta_ulic==0:
            wybor_slowko.set('')
            wybor_ulica.set('ulice')
            #print('szukanie ulic')
        else:
            wybor_slowko.set('slowka')
            wybor_ulica.set('')
            #print('szukanie slowek')

        napis1=TK.Label(okienko,text="Wpisz tutaj (przynajmniej 3 znaki):",font=self.czcionka_small)

        pole_szukania=TK.Entry(okienko,font=self.czcionka_small,width=40)
        pole_szukania.bind("<Return>",szukanie)
        pole_szukania.focus_set()

        wyniki_szukania=TK.Listbox(okienko,font=self.czcionka_small,width=56,height=17)
        wyniki_szukania.bind("<<ListboxSelect>>",zaznaczony_wpis)

        if type(self.logika.biezacy_wpis) is KL.KWU:
            ustaw_szukanie_ulic()
        else:
            ustaw_szukanie_slowek()

        #grid-y okienka szukania
        radio1.grid(row=0,column=0,columnspan=2)
        radio2.grid(row=0,column=1,columnspan=2)
        guzik_kasuj.grid(row=0,column=3,sticky='E')
        napis1.grid(row=1,columnspan=3)
        guzik_edytuj.grid(row=1,column=3,sticky='E')
        pole_szukania.grid(row=2,columnspan=3,sticky='E')
        wyniki_szukania.grid(row=3,rowspan=9,columnspan=4)
        #koniec f.szukaj_wpisow_okno

    def dodaj_wpis_okno(self,_):
        '''
        wykorzystuje metodę dodaj_wpis klasy Logika

        rozumiem że jest błąd w Radiobutton. donosili o tym w necie
        dlatego użyłem podwójnego StringVar(wybor_ulica i wybor_slowko)

        po dodaniu wpisu: aktualizuj_napis_ilosc_wpisow()
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
                    self.aktualizuj_napis_ilosc_wpisow()
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
                    self.aktualizuj_napis_ilosc_wpisow()
                else:
                    print('---nieudane dodanie nowego słówka---')

        okienko=TK.Toplevel(self.okno)
        okienko.geometry('+350+300')
        okienko.wm_iconphoto(False,TK.PhotoImage(file='logo2.png'))
        okienko.bind("<KeyPress-Escape>",zamknij_okienko)
        okienko.protocol("WM_DELETE_WINDOW",zamknij_okienko)

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
        #koniec f.dodaj_wpis_okno

    def edytuj_wpis_okno(self,str_do_edycji):
        '''
        '''
        def zamiana_kolejnosci(_=None):
            '''
            ang->pol + pol->ang. czyli dla EDYCJA_SLOWKA i WYSZUKANE_SLOWKO
            robi to na wpisie ustawionym w wpis_slowko/wpis_ulica
            '''
            print('f.zamiana_kolejnosci.tryb_edycji=',tryb_edycji)

            #zamien w GUI
            komp.wpis1.delete(0,TK.END)
            komp.wpis1.insert(0,wpis_slowko.drugi)
            komp.wpis2.delete(0,TK.END)
            komp.wpis2.insert(0,wpis_slowko.pierwszy)

            #zamien w logika.lista_slowek
            tmp_pierwszy=wpis_slowko.pierwszy
            wpis_slowko.pierwszy=wpis_slowko.drugi
            wpis_slowko.drugi=tmp_pierwszy


        def zamknij_okienko_bez_zmian(_=None):
            '''jak chcesz tylko zamknąć okno
                czyli porzuca zmiany z wpis_slowko/wpis_ulica
            '''
            print('zamknij_okienko_bez_zmian')
            okienko.destroy()

        def zamknij_okienko_zastosuj_zmiany(_=None):
            '''
            '''
            print('f.zamknij_okienko_zastosuj_zmiany',tryb_edycji)

            if tryb_edycji is tryb_edycji.EDYCJA_ULICY:
                if komp.wpis1.get()!='':
                    wpis_ulica=KL.KWU(komp.wpis1.get(),komp.wpis3.get(),int(komp.wpis4.get()))
                    print('Unowszy',wpis_ulica)
                else:
                    print('---Uniemożna podmienić na puste---',tryb_edycji)

            elif tryb_edycji is tryb_edycji.EDYCJA_SLOWKA:
                if komp.wpis1.get()!='' and komp.wpis2.get()!='':
                    wpis_slowko=KL.KWS(komp.wpis1.get(),komp.wpis2.get(),
                                komp.wpis3.get(),int(komp.wpis4.get()))
                    print('Snowszy=',wpis_slowko)
                else:
                    print('---Sniemożna podmienić na puste---',tryb_edycji)

            elif tryb_edycji is tryb_edycji.WYSZUKANA_ULICA:
                if komp.wpis1.get()!='':
                    wpis_ulica=KL.KWU(komp.wpis1.get(),komp.wpis3.get(),int(komp.wpis4.get()))
                    print('Unowszy',wpis_ulica)
                else:
                    print('---Uniemożna podmienić na puste---',tryb_edycji)

            elif tryb_edycji is tryb_edycji.WYSZUKANE_SLOWKO:
                if komp.wpis1.get()!='' and komp.wpis2.get()!='':
                    wpis_slowko=KL.KWS(komp.wpis1.get(),komp.wpis2.get(),
                                komp.wpis3.get(),int(komp.wpis4.get()))
                    print('Snowszy=',wpis_slowko)
                else:
                    print('---Sniemożna podmienić na puste---',tryb_edycji)


            if tryb_edycji in [tryb_edycji.EDYCJA_ULICY,tryb_edycji.WYSZUKANA_ULICA]:
                self.logika.zmien_wpis(starszy,wpis_ulica)

            elif tryb_edycji in [tryb_edycji.EDYCJA_SLOWKA,tryb_edycji.WYSZUKANE_SLOWKO]:
                self.logika.zmien_wpis(starszy,wpis_slowko)

            elif tryb_edycji in [tryb_edycji.EDYCJA_SLOWKA,tryb_edycji.EDYCJA_ULICY]:
                self.entry1_tresc.set(wpis_slowko.pierwszy)
                self.entry1_tresc.set(wpis_slowko.drugi)

            okienko.destroy()
            if tryb_edycji in [tryb_edycji.WYSZUKANE_SLOWKO,tryb_edycji.WYSZUKANA_ULICA]:
                return 'czysc_wyniki_szukania'
            return False


        def okresl_tryb_edycji():
            ""
            tryb_edycji=KL.EN.Enum('tryb_edycji',['EDYCJA_SLOWKA',
                                               'EDYCJA_ULICY',
                                               'WYSZUKANE_SLOWKO',
                                               'WYSZUKANA_ULICA'])

            if type(str_do_edycji) is TK.Event:
                #print('jest event. czyli normalna edycja',self.logika.biezacy_wpis,'=')
                if type(self.logika.biezacy_wpis) is KL.KWU:
                    #print('mówię że to EDYCJA_ULICY')
                    tryb_edycji=tryb_edycji.EDYCJA_ULICY
                else:
                    #print('mówię że to EDYCJA_SLOWKA')
                    tryb_edycji=tryb_edycji.EDYCJA_SLOWKA
            elif KL.KW.czy_str_jest_klasy_wpis_ulica(str_do_edycji):
                #print('mówię że to WYSZUKANA_ULICA')
                tryb_edycji=tryb_edycji.WYSZUKANA_ULICA
            elif KL.KW.czy_str_jest_klasy_wpis_slowko(str_do_edycji):
                #print('mówię że to WYSZUKANE_SLOWKO')
                tryb_edycji=tryb_edycji.WYSZUKANE_SLOWKO

            print('---określony tryb_edycji',tryb_edycji)
            return tryb_edycji

        def tworz_komponenty_okienka_bez_ustawiania_ich():
            "tworzenie komponentow tylko(bez wartosci ustawionych)"
            class Komp:
                pass
            komp=Komp()

            komp.podpis1=TK.Label(okienko,font=self.czcionka_small)
            komp.wpis1=TK.Entry(okienko,font=self.czcionka_middle,width=30)

            komp.podpis2=TK.Label(okienko,font=self.czcionka_small)
            komp.wpis2=TK.Entry(okienko,font=self.czcionka_middle,width=30)

            komp.podpis3=TK.Label(okienko,text='Tryb:',font=self.czcionka_small)
            komp.wpis3=TTK.Combobox(okienko,font=self.czcionka_middle,width=30,state='readonly')
            tryby=('A','B','C')
            komp.wpis3['values']=tryby

            komp.podpis4=TK.Label(okienko,text='Ile Razy Wylosowany:',font=self.czcionka_small)
            komp.wpis4=TTK.Combobox(okienko,font=self.czcionka_middle,width=30,state='readonly')

            komp.guzik_cofaj=TK.Button(okienko,text='Rezygnuj ze zmian',font=self.czcionka_small,
                                        command=zamknij_okienko_bez_zmian)
            komp.guzik_zamien=TK.Button(okienko,text='Zamień kolejność',font=self.czcionka_small,
                                        command=zamiana_kolejnosci)
            komp.guzik_potwierdz=TK.Button(okienko,text='Zatwierdź(Escape)',
                        font=self.czcionka_small,command=zamknij_okienko_zastosuj_zmiany)

            #gridowanie
            komp.podpis1.grid(row=0,columnspan=3)
            komp.wpis1.grid(row=1,columnspan=3)
            komp.podpis2.grid(row=2,columnspan=3)
            komp.wpis2.grid(row=3,columnspan=3)
            komp.podpis3.grid(row=4,columnspan=3)
            komp.wpis3.grid(row=5,columnspan=3)
            komp.podpis4.grid(row=6,columnspan=3)
            komp.wpis4.grid(row=7,columnspan=3)
            komp.guzik_cofaj.grid(row=8,column=0)
            komp.guzik_zamien.grid(row=8,column=1)
            komp.guzik_potwierdz.grid(row=8,column=2)

            return komp

        def ustaw_komponenty_wg_trybu_edycji(jaki_tryb_edycji,wpis_slowko,wpis_ulica):
            '''
            zrobione dla każdego trybu oddzielnie. chciałem uniknąć duplikowania
            ale czytelność jest ważniejsza
            '''

            #print('---f.ustaw_komponenty_wg_trybu_edycji. tryb_edycji=',tryb_edycji)

            if tryb_edycji is tryb_edycji.EDYCJA_ULICY:
                #bez danych
                okienko.title('Edycja Ulicy')
                komp.podpis1.config(text='Nazwa Ulicy:')
                komp.podpis2.config(text='')
                komp.wpis2.config(state=TK.DISABLED)
                komp.wpis1.delete(0,TK.END)
                komp.wpis2.delete(0,TK.END)
                komp.wpis4.delete(0,TK.END)
                komp.guzik_zamien.config(state=TK.DISABLED)

                #teraz ustawianie danymi
                komp.wpis1.insert(0,self.logika.biezacy_wpis.pierwszy)
                komp.wpis3.current(ord(self.logika.biezacy_wpis.tryb)-65)

                ilosci=tuple(range(0,self.logika.biezacy_wpis.ile_razy_wylos+11))
                komp.wpis4['values']=ilosci
                komp.wpis4.current(self.logika.biezacy_wpis.ile_razy_wylos)

                #poszerzanie dla dużego wpisu
                dlugosc=len(self.logika.biezacy_wpis.pierwszy)
                if dlugosc>30:
                    print('poszerzamU')
                    komp.wpis1.config(width=dlugosc+3)


            if tryb_edycji is tryb_edycji.EDYCJA_SLOWKA:
                #bez danych
                okienko.title('Edycja Słówka')
                komp.podpis1.config(text='Angielski:')
                komp.podpis2.config(text='Polski:')
                komp.wpis2.config(state=TK.NORMAL)
                komp.wpis1.delete(0,TK.END)
                komp.wpis2.delete(0,TK.END)
                komp.wpis4.delete(0,TK.END)
                komp.guzik_zamien.config(state=TK.NORMAL)

                #teraz ustawianie danymi
                komp.wpis1.insert(0,self.logika.biezacy_wpis.pierwszy)
                komp.wpis2.insert(0,self.logika.biezacy_wpis.drugi)
                komp.wpis3.current(ord(self.logika.biezacy_wpis.tryb)-65)

                ilosci=tuple(range(0,self.logika.biezacy_wpis.ile_razy_wylos+11))
                komp.wpis4['values']=ilosci
                komp.wpis4.current(self.logika.biezacy_wpis.ile_razy_wylos)

                #poszerzanie dla dużego wpisu
                dlugosc=max(len(self.logika.biezacy_wpis.pierwszy),
                            len(self.logika.biezacy_wpis.drugi))
                if dlugosc>30:
                    print('poszerzamS')
                    komp.wpis1.config(width=dlugosc+3)
                    komp.wpis2.config(width=dlugosc+3)


            if tryb_edycji is tryb_edycji.WYSZUKANE_SLOWKO:
                #bez danych
                okienko.title('Edycja Słówka')
                komp.podpis1.config(text='Angielski:')
                komp.podpis2.config(text='Polski:')
                komp.wpis2.config(state=TK.NORMAL)
                komp.wpis1.delete(0,TK.END)
                komp.wpis2.delete(0,TK.END)
                komp.wpis4.delete(0,TK.END)
                komp.guzik_zamien.config(state=TK.NORMAL)

                #teraz ustawianie danymi
                wpis_slowko=KL.KW.str_do_wpis_slowko(str_do_edycji)
                komp.wpis1.insert(0,wpis_slowko.pierwszy)
                komp.wpis2.insert(0,wpis_slowko.drugi)
                komp.wpis3.current(ord(wpis_slowko.tryb)-65)

                ilosci=tuple(range(0,wpis_slowko.ile_razy_wylos+11))
                komp.wpis4['values']=ilosci
                komp.wpis4.current(wpis_slowko.ile_razy_wylos)

                #poszerzanie dla dużego wpisu
                dlugosc=max(len(wpis_slowko.pierwszy),len(wpis_slowko.drugi))
                if dlugosc>30:
                    print('poszerzamS')
                    komp.wpis1.config(width=dlugosc+3)
                    komp.wpis2.config(width=dlugosc+3)

            if tryb_edycji is tryb_edycji.WYSZUKANA_ULICA:
                #bez danych
                okienko.title('Edycja Ulicy')
                komp.podpis1.config(text='Nazwa Ulicy:')
                komp.podpis2.config(text='')
                komp.wpis2.config(state=TK.DISABLED)
                komp.wpis1.delete(0,TK.END)
                komp.wpis2.delete(0,TK.END)
                komp.wpis4.delete(0,TK.END)
                komp.guzik_zamien.config(state=TK.DISABLED)

                #teraz ustawianie danymi
                wpis_ulica=KL.KW.str_do_wpis_ulica(str_do_edycji)
                komp.wpis1.insert(0,wpis_ulica.pierwszy)
                komp.wpis3.current(ord(wpis_ulica.tryb)-65)

                ilosci=tuple(range(0,wpis_ulica.ile_razy_wylos+11))
                komp.wpis4['values']=ilosci
                komp.wpis4.current(wpis_ulica.ile_razy_wylos)

                #poszerzanie dla dużego wpisu
                dlugosc=len(wpis_ulica.pierwszy)
                if dlugosc>30:
                    print('poszerzamS')
                    komp.wpis1.config(width=dlugosc+3)
                    komp.wpis2.config(width=dlugosc+3)

            komp.wpis1.focus_set()
            #ustaw_komponenty_wg_trybu_edycji

        #tu się zaczyna f.edytuj_wpis_okno
        if self.logika.komunikat_bledu!='':
            print('---jest błąd:',self.logika.komunikat_bledu,'---')
            return

        tryb_edycji=okresl_tryb_edycji()
        wpis_slowko=None
        wpis_ulica=None
        starszy=None
        #nowszy=None

        if tryb_edycji is tryb_edycji.EDYCJA_SLOWKA:
            wpis_slowko=self.logika.biezacy_wpis
            starszy=wpis_slowko

        if tryb_edycji is tryb_edycji.WYSZUKANE_SLOWKO:
            wpis_slowko=KL.KW.str_do_wpis_slowko(str_do_edycji)
            starszy=wpis_slowko

        if tryb_edycji is tryb_edycji.EDYCJA_ULICY:
            wpis_ulica=self.logika.biezacy_wpis
            starszy=wpis_ulica

        if tryb_edycji is tryb_edycji.WYSZUKANA_ULICA:
            wpis_ulica=KL.KW.str_do_wpis_ulica(str_do_edycji)
            starszy=wpis_ulica


        okienko=TK.Toplevel(self.okno)
        okienko.geometry('+350+300')
        okienko.wm_iconphoto(False,TK.PhotoImage(file='logo2.png'))
        okienko.bind("<KeyPress-Escape>",zamknij_okienko_zastosuj_zmiany)
        okienko.protocol("WM_DELETE_WINDOW",zamknij_okienko_bez_zmian)

        komp=tworz_komponenty_okienka_bez_ustawiania_ich()

        ustaw_komponenty_wg_trybu_edycji(tryb_edycji,wpis_slowko,wpis_ulica)

        #koniec f.edytuj_wpis_okno
