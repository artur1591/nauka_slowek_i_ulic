'''
obiekty klasy WpisUlica i WpisSlowko
'''
class WpisUlica:
    "..."
    def __init__(self,one,tryb='A',ile_x=0):
        ""
        if not isinstance(one,str):
            raise TypeError('pierwszy ma być str.jest',type(one))

        if tryb not in ['A','B','C']:
            raise ValueError('tryb musi być A/B/C. jest',tryb)

        if ile_x<0:
            raise ValueError('ile_x musi być nieujemne.jest',ile_x)

        self.pierwszy=one
        self.tryb=tryb
        self.ile_razy_wylos=ile_x

    def __eq__(self,inny):
        '''
        pełne sprawdzanie. jak potrzeba tylko niektóre składowe to ręcznie zrób
        '''
        #print('operator eq ulicy')
        if isinstance(inny,WpisUlica):
            ile_true=0
            if self.pierwszy==inny.pierwszy:
                ile_true+=1
            if self.tryb==inny.tryb:
                ile_true+=1
            if self.ile_razy_wylos==inny.ile_razy_wylos:
                ile_true+=1

            return ile_true==3
        raise TypeError('porównuje WpisUlica z typem',type(inny))

    def __lt__(self,inny):
        '''
        do sortowania. zauważ że sprawdza tylko składową pierwszy
        '''
        return self.pierwszy<inny.pierwszy

    def __str__(self):
        '''
        wykorzystywane do zapisywania ulic(taki operator wypisywania)
        po pierwszy jest znak |
        '''
        return self.pierwszy+'|'+self.tryb+' '+str(self.ile_razy_wylos)

    def czy_str_jest_klasy_WpisUlica(napis):
        '''
        sprawdza tylko typ żeby DRY
        '''
        if isinstance(WpisUlica.str_do_WpisUlica(napis),WpisUlica):
            return True
        return False

    def str_do_WpisUlica(napis):
        '''
        odwrotność __str__
        w razie niepowodzenia False

        warunki wstępne:
            musi mieć przynajmniej 1 spacje
            zawierać jeden z '|A', '|B', '|C'
        '''
        #print('Unapis',napis)
        if not isinstance(napis,str):
            return False
        if napis.count(' ')==0:
            return False
        if not any([napis.__contains__(wl) for wl in ['|A','|B','|C']]):
            return False

        przerwa_po_pierwszy=napis.rindex('|')
        #print('przerwa_po_pierwszy',przerwa_po_pierwszy)
        pierwszy=napis[0:przerwa_po_pierwszy]
        przerwa_po_trybie=napis.rindex(' ')
        #print('przerwa_po_trybie',przerwa_po_trybie)
        tryb=napis[przerwa_po_pierwszy+1]
        ile_x=napis[przerwa_po_pierwszy+3:]
        #print('\nTUpierwszy',pierwszy,'tryb',tryb,'ile_x',ile_x)

        if tryb not in ['A','B','C']:
            return False
        if int(ile_x)<0:
            return False
        if not isinstance(pierwszy,str):
            return False

        return WpisUlica(pierwszy,tryb,int(ile_x))

    def __repr__(self):
        return self.pierwszy+'|'+self.tryb+' '+str(self.ile_razy_wylos)

class WpisSlowko(WpisUlica):
    "rozszerza WpisUlica"
    def __init__(self,one,two,tryb='A',ile_x=0):
        if not isinstance(one,str) or not isinstance(two,str):
            raise ValueError('pierwszy i drugi musi być str.jest',type(one),type(two))

        WpisUlica.__init__(self,one,tryb,ile_x)
        self.drugi=two

    def __eq__(self,inny):
        '''
        pełne sprawdzanie. jak potrzeba tylko niektóre składowe to ręcznie zrób
        '''
        #print('operator eq slowka')
        if isinstance(inny,WpisSlowko):
            ile_true=0
            if self.pierwszy==inny.pierwszy:
                ile_true+=1
            if self.drugi==inny.drugi:
                ile_true+=1
            if self.tryb==inny.tryb:
                ile_true+=1
            if self.ile_razy_wylos==inny.ile_razy_wylos:
                ile_true+=1

            return ile_true==4
        raise TypeError('porównuje WpisSlowko z typem',type(inny))

    def __lt__(self,inny):
        '''
        do sortowania. zauważ że sprawdza tylko składową pierwszy
        '''
        return self.pierwszy<inny.pierwszy

    def __str__(self):
        '''
        wykorzystywane do zapisywania slowek (takie operator wypisywania)
        po pierwszy jest znak |
        '''
        return self.pierwszy+'|'+self.drugi+' '+self.tryb+' '+str(self.ile_razy_wylos)

    def czy_str_jest_klasy_WpisSlowko(napis):
        '''
        sprawdza tylko typ żeby DRY
        '''
        if isinstance(WpisSlowko.str_do_WpisSlowko(napis),WpisSlowko):
            return True
        return False

    def str_do_WpisSlowko(napis):
        '''
        odwrotność __str__
        w razie niepowodzenia False

        warunki wstępne:
            musi mieć przynajmniej 2 spacje
            zawierać jeden z ' A ', ' B ', ' C '
        '''
        #print('Snapis',napis)
        if not isinstance(napis,str):
            return False
        if napis.count(' ')<2:
            return False
        if not any([napis.__contains__(wl) for wl in [' A ',' B ',' C ']]):
            return False

        przerwa_po_pierwszy=napis.rindex('|')
        #print('przerwa_po_pierwszy',przerwa_po_pierwszy)
        pierwszy=napis[0:przerwa_po_pierwszy]
        przerwa_po_trybie=napis.rindex(' ')
        #print('przerwa_po_trybie',przerwa_po_trybie)
        tryb=napis[przerwa_po_trybie-1:przerwa_po_trybie]
        ile_x=napis[przerwa_po_trybie+1:]
        drugi=napis[przerwa_po_pierwszy+1:przerwa_po_trybie-2]
        #print('\nSpierwszy',pierwszy,'drugi',drugi,'tryb',tryb,'ile_x',ile_x)

        if tryb not in ['A','B','C']:
            return False
        if int(ile_x)<0:
            return False
        if not isinstance(pierwszy,str) or not isinstance(drugi,str):
            return False

        #print('przed return')
        return WpisSlowko(pierwszy,drugi,tryb,int(ile_x))

    def __repr__(self):
        return self.pierwszy+'|'+self.drugi+' '+self.tryb+' '+str(self.ile_razy_wylos)

if __name__=='__main__':
    print('---są testy dla tych klas---')
