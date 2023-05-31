'''
obiekty klasy wpisulica i wpisslowko
'''
class WpisUlica:
    "do dziedziczenia"
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
        raise TypeError('porównuje wpisulica z typem',type(inny))

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


    def __repr__(self):
        return self.pierwszy+'|'+self.tryb+' '+str(self.ile_razy_wylos)


def str_do_wpis_ulica(napis):
    '''
    odwrotność __str__
    w razie niepowodzenia False

    warunki wstępne:
        musi być 1 znak |
        musi mieć przynajmniej 1 spacja
        zawierać jeden z '|A ', '|B ', '|C '
    '''
    if not isinstance(napis,str):
        raise TypeError('str->WpisUlica.miał być str a jest',type(napis),napis,'_')
    if not napis:
        print('str_do_wpis_ulica.napis jest pusty')
        return False
    if napis.count('|')!=1:
        print('str->WpisUlica.znak | musi być dokładnie 1',napis,'_')
        return False
    if napis.count(' ')==0:
        print('str->WpisUlica.brak spacji',napis,'_')
        return False
    if not any(napis.__contains__(wl) for wl in ['|A ','|B ','|C ']):
        print('str->WpisUlica.przed trybem potrzebny znak |, a po spacja',napis,'_')
        return False

    przerwa_po_pierwszy=napis.index('|')
    #print('przerwa_po_pierwszy',przerwa_po_pierwszy)
    pierwszy=napis[0:przerwa_po_pierwszy]
    tryb=napis[przerwa_po_pierwszy+1]
    ile_x=napis[przerwa_po_pierwszy+3:]
    #print('\nTUpierwszy1',pierwszy,'tryb',tryb,'ile_x',ile_x,'_')
    #print('Uile_x',type(ile_x),ile_x.isnumeric(),'_',ile_x,'_')

    if not ile_x.isnumeric():
        print('WpisUlic.str(ile_x) niedobry')
        return False
    if tryb not in ['A','B','C']:
        print('str->WpisUlica.zły tryb',tryb)
        return False
    if int(ile_x)<0:
        print('str->WpisUlica.zła ile_razy_wylos',ile_x)
        return False
    if not pierwszy:
        print('str->WpisUlica.pierwszy pusty',pierwszy,'_')
        return False

    #print('\nTUpierwszy2',pierwszy,'tryb',tryb,'ile_x',ile_x,'_')
    return WpisUlica(pierwszy,tryb,int(ile_x))

def czy_str_jest_klasy_wpis_ulica(napis):
    '''
    sprawdza tylko typ żeby DRY
    '''
    return type(str_do_wpis_ulica(napis)) is WpisUlica

class WpisSlowko(WpisUlica):
    "pochodna od WpisUlica"
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
        wykorzystywane do zapisywania slowek (taki operator wypisywania)
        po pierwszy jest znak |
        '''
        return self.pierwszy+'|'+self.drugi+' '+self.tryb+' '+str(self.ile_razy_wylos)

    def __repr__(self):
        return self.pierwszy+'|'+self.drugi+' '+self.tryb+' '+str(self.ile_razy_wylos)

def czy_str_jest_klasy_wpis_slowko(napis):
    '''
    sprawdza tylko typ żeby DRY
    '''
    return type(str_do_wpis_slowko(napis)) is WpisSlowko

def str_do_wpis_slowko(napis):
    '''
    odwrotność __str__
    w razie niepowodzenia False

    warunki wstępne:
        musi być 1 znak |
        musi mieć przynajmniej 2 spacje
        zawierać jeden z ' A ', ' B ', ' C '
    '''
    print('str->WpisSlowko.napis',napis,'_')
    if not isinstance(napis,str):
        raise TypeError('str->WpisSlowko.miał być str a jest',type(napis),napis,'_')

    if not napis:
        print('str_do_wpis_slowko.napis jest pusty')
        return False
    if napis.count('|')!=1:
        print('str->WpisSlowko.znak | musi być dokładnie 1',napis,'_')
        return False
    if napis.count(' ')<2:
        print('str->WpisSlowko.mają być chociaż 2 spacje',napis,'_')
        return False
    if not any(napis.__contains__(wl) for wl in [' A ',' B ',' C ']):
        print('str->WpisSlowko.przed trybem i po potrzebna spacja',napis,'_')
        return False

    przerwa_po_pierwszy=napis.index('|')
    #print('przerwa_po_pierwszy',przerwa_po_pierwszy)
    pierwszy=napis[0:przerwa_po_pierwszy]
    przerwa_po_trybie=napis.rindex(' ')
    #print('przerwa_po_trybie',przerwa_po_trybie)
    tryb=napis[przerwa_po_trybie-1:przerwa_po_trybie]
    ile_x=napis[przerwa_po_trybie+1:]
    drugi=napis[przerwa_po_pierwszy+1:przerwa_po_trybie-2]
    #print('\nSpierwszy',pierwszy,'drugi',drugi,'tryb',tryb,'ile_x',ile_x)
    #print('Sile_x',type(ile_x),ile_x.isnumeric(),'_',ile_x,'_')

    if not ile_x.isnumeric():
        print('WpisSlowko.str(ile_x) niedobry')
        return False
    if tryb not in ['A','B','C']:
        print('str->WpisSlowko.zły tryb',tryb)
        return False
    if int(ile_x)<0:
        print('str->WpisSlowko.zła ile_razy_wylos',ile_x)
        return False
    if not pierwszy or not drugi:
        print('str->WpisSlowko.pierwszy/drugi pusty',pierwszy,'_',drugi,'_')
        return False

    print('\nSpierwszy',pierwszy,'drugi',drugi,'tryb',tryb,'ile_x',ile_x)
    return WpisSlowko(pierwszy,drugi,tryb,int(ile_x))

if __name__=='__main__':
    print('---są testy dla tych klas---')
