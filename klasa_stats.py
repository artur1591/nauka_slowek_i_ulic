'''
obsługuje statystyki związane z dzienną ilością ćwiczonych słówek i ulic.
zapisuje je w pliku określonym w self.jaki_plik
'''
import datetime as DT
import os as OS

class Stats:
    "wymaga refaktoryzacji ale poczekam na lepsze określenie wymagań wobec niej"
    def __init__(self):
        ""
        self.jaki_plik='statystyki.nauka'
        self.biezace_statystyki_trojca=[]
        self.bylo_dzisiaj=False

    def kolejna_ulica(self):
        "inkrementacja dziennej ilości wylosowanych ulic"
        print('Stats.kolejna_ulica')
        self.biezace_statystyki_trojca[-1][1]+=1

    def kolejne_slowko(self):
        "inkrementacja dziennej ilości wylosowanych słówek"
        print('Stats.kolejne_slowko')
        self.biezace_statystyki_trojca[-1][2]+=1

    @staticmethod
    def _daj_date_():
        "tworzy 10znakową datę YYYY_MM_DD"
        dt_obj=DT.date.today()
        rok=str(dt_obj.year)
        mies=str(dt_obj.month)
        if int(mies)<10:
            mies='0'+mies
        dzien=str(dt_obj.day)
        if int(dzien)<10:
            dzien='0'+dzien

        return rok+'_'+mies+'_'+dzien

    def _zrob_linie_(self,*,kiedy,ile_u,ile_s):
        '''
        jak kiedy is False to robi dzisiejsza date
        jak nie to podac trzeba w formacie właściwym

        tworzy całą linia w formacie: YYYY_MC_DD U 000 S 000
        '''
        nowa_linia=''
        if kiedy is False:
            nowa_linia+=self._daj_date_()
        else:
            nowa_linia+=kiedy

        nowa_linia+=' U '
        nowa_linia+=str(ile_u).rjust(3,'0')+' S '
        nowa_linia+=str(ile_s).rjust(3,'0')+'\n'
        return nowa_linia

    def wczytaj(self):
        '''
        wypełnia self.biezace_statystyki_trojca która jest zawsze aktualne
        '''
        print('f.wczytaj statystyki')
        if not OS.path.exists(self.jaki_plik) or OS.stat(self.jaki_plik).st_size==0:
            print('---brak pliku lub pusty plik:',self.jaki_plik,'---')
            self.biezace_statystyki_trojca.append([self._daj_date_(),0,0])
            return False

        caly_plik=None
        with open(self.jaki_plik,'r') as plik:
            caly_plik=plik.readlines()

        self.biezace_statystyki_trojca=list()

        for linia in caly_plik:
            data=linia[:10]
            ile_u=int(linia[13:16])
            ile_s=int(linia[19:22])
            self.biezace_statystyki_trojca.append([data,ile_u,ile_s])

        #trojca mozna zwrocic i zbudowac z wykres jakis ładny
        print('biezace_statystyki_trojca',self.biezace_statystyki_trojca)

        #print('ostatnia_linia',self.wczytana_ostatnia_linia)
        data_z_ost_linii=self.biezace_statystyki_trojca[-1][0]
        data_dzisiejsza=self._daj_date_()

        #print('data z ost.linii:',data_z_ost_linii,'_')
        #print('__daj_date__()  :',data_dzisiejsza,'_')
        if data_z_ost_linii==data_dzisiejsza:
            print('---było dzisiaj już---')
            self.bylo_dzisiaj=True
        else:
            print('---pierwszy raz dzisiaj grasz---')
            self.biezace_statystyki_trojca.append([self._daj_date_(),0,0])

        return True


    def zapisz(self):
        '''
        zapisuje cały plik narazie
        '''
        print('f.zapisz: trojca',self.biezace_statystyki_trojca)
        if len(self.biezace_statystyki_trojca)==0:
            print('---przerywam zapis do biezace_statystyki_trojca PUSTY---')
            return
        with open(self.jaki_plik,'w') as plik:
            for kolejna_trojca in self.biezace_statystyki_trojca:
                print('kolejna_trojca',kolejna_trojca)
                linia=self._zrob_linie_(kiedy=kolejna_trojca[0],
                                ile_u=kolejna_trojca[1],ile_s=kolejna_trojca[2])
                print('linia do zapisu',linia,'_')
                plik.write(linia)
