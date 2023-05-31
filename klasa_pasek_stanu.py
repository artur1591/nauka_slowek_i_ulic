'''
własny Pasekstanu.
pamiętaj o zamknij przed zamykaniem okna głównego
(wcześniej było __del__ ale wywoływało się 2x:niejawnie + jawnie).
'''
import tkinter as tk
import threading as TH

class Pasekstanu(tk.Frame):
    '''
    klasa Pasekstanu. 3 Labele(lewy: ktory=0 , środkowy: ktory=1, prawy: ktory=2)
    '''
    def zamknij(self):
        '''
        to trzeba w zamykaniu klasy Interfejs żeby cancel() ewentualne Timery
        ponieważ trzeba mu wskazać moment zakończenia
        '''
        for ktory in range(3):
            if not self.timer[ktory] is None:
                self.timer[ktory].cancel()
                self.timer[ktory]=None

    def __init__(self,_jakie_okno,czcionka):
        '''
        Pasekstanu
        '''
        super().__init__()

        self.szer=[0,0,0]
        for ktory in range(3):
            self.szer[ktory]=33

        for ktory in range(3):
            self.columnconfigure(ktory,weight=self.szer[ktory])

        self.napis=[]

        for ktory in range(3):
            self.napis.append(tk.Label(self,text=" ".center(self.szer[ktory]),bd=1,
                                        relief=tk.SUNKEN,font=czcionka,bg='grey'))
        for ktory in range(3):
            self.napis[ktory].grid(row=0,column=ktory,sticky='EW')

        self.timer=[0,0,0]
        for ktory in range(3):
            self.timer[ktory]=None

    def ustaw(self,*,ktory,tresc=None,na_ile_sek=0):
        '''
        ktory może być albo 0 albo 1 albo 2
        '''
        #print('ustaw:',ktory,'_',tresc,'=',na_ile_sek)
        self.napis[ktory].config(text=tresc.center(self.szer[ktory]))

        if self.timer[ktory] is None:
            #print('timer[',ktory,']=none na_ile_sek',na_ile_sek)
            if na_ile_sek!=0:
                #print('na_ile_sek=',na_ile_sek,'ktory',ktory)
                self.timer[ktory]=TH.Timer(na_ile_sek,self.czysc,(ktory,))
                self.timer[ktory].start()
        else:
            self.timer[ktory].cancel()
            self.timer[ktory]=None
            self.ustaw(ktory=ktory,tresc=tresc,na_ile_sek=na_ile_sek)

    def czysc(self,ktory):
        '''
        kasowanie tresci lewego lub środkowego lub prawego paska
        '''
        if not ktory==0 and not ktory==1 and not ktory==2:
            raise ValueError('ktory ma być 0 lub 1 lub 2. jest',ktory)
        self.napis[ktory].config(text=' '*self.szer[ktory])
        #print('czysc',ktory)
        if not self.timer[ktory] is None:
            self.timer[ktory].cancel()
            self.timer[ktory]=None

    def config(self,**kwargs):
        "co z tym?"
        print('vars=',vars())
        print('arg przekazane',kwargs)
        for ktory in range(3):
            self.napis[ktory].config(**kwargs)
