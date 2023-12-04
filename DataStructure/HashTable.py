import numpy as np

class HashTable:
    '''
    Tabela Hash usando a tecnica de sondagem linear para
    tratamento de colisão
    '''
    def __init__(self,size = 10):
        self.__ocupados = 0
        self.__table = np.full(size,None)

    def __hash(self, key:any)->int:
        '''
        calculo do hash modular
        '''
        return hash(key) % len(self.__table)
        

    def __rh(self, index:int):
        return (index+1) % len(self.__table)
    
    def estaCheia(self)->bool:
        return self.__ocupados == len(self.__table)

    def put(self, key:any, data:any):
        if self.estaCheia():
            return False
        hashValor = self.__hash(key)

        while self.__table[hashValor] != None:
            hashValor = self.__rh(hashValor)
            print(hashValor)

        self.__table[hashValor] = data
        self.__ocupados += 1        

    def get(sefl, key:any)->any:
        pass

    def __str__(self):
        info = "{"
        for items in self.__table:
            if items == None:
                continue
            for entry in items:
                info += f'{entry.key}:{entry.value},'
        info = info.rstrip(',') + '}'
        return info

