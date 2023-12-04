from typing import List, Any
import numpy as np

class Entry:
    """
    Classe privada utilizada para encapsular os pares chave/valor
    """
    def __init__( self, entryKey, entryValue ):
        self.__key = entryKey
        self.__value = entryValue
    
    @property
    def key( self ):
        return self.__key
    
    @property
    def value( self ):
        return self.__value
    
    @value.setter
    def value( self, newValue ):
        self.__value = newValue

    @key.setter
    def key( self, newKey ):
        self.__key = newKey
        
    def __str__( self ):
        return "(" + str( self.__key ) + ", " + str( self.__value ) + ")"
 
class ChainingHashTable:
    def __init__(self, size:int=100):
        '''
        Construtor da classe que recebe o tamanho para a tabela de dispersão.
        Utiliza um list de python como estrutura encadeda para armazenar os elementos mapeados para um slot correpondente.
        Argumentos:
            size(int): tamanho da tabela de dispersão. Se não informar, 
            o tamanho padrão é 100.
        '''
        self.__used = 0
        # inicializa a tabela de dispersão com todos os elementos iguais a None
        self.__table = np.full(size,None)
        self.__table = [[] for i in range(size)]

    def __len__(self)->int:
        count = 0
        for i in self.__table:
            count += len(i)
        return count

    def __hash(self, key:any)->int:
        ''' 
            Método que retorna a posição na tabela hashing conforme a chave.
            (hash modular)
        '''
        return hash(key) % len(self.__table)
    
    def keys(self)->List[any]:
        '''
            Método que retorna uma lista com todas as chaves da tabela de dispersão.
            Retorna:
                list: lista com todas as chaves da tabela de dispersão.
        '''
        lista = []
        for items in self.__table:
            if items == None:
                continue
            for entry in items:
                lista.append(entry.key)
        return lista
    
    def values(self)->List[any]:
        '''
            Método que retorna uma lista com todos os valores da tabela de dispersão.
            Retorna:
                list: lista com todos os valores da tabela de dispersão.
        '''
        lista = []
        for items in self.__table:
            if items == None:
                continue
            for entry in items:
                lista.append(entry.value)
        return lista


    def put(self, key:any, data:any)->int:
        ''' 
            Método que insere um novo elemento na tabela de dispersão.
            Argumentos:
                key(Any): chave do elemento a ser inserido.
                data(Any): valor do elemento a ser inserido.
            Retorna:
                int: índice na tabela de dispersão onde o elemento foi inserido.
        '''
        slot = self.__hash(key)
        for i in range(len(self.__table[slot])):
            if key == self.__table[slot][i].key:
                self.__table[slot][i].value = data
                return slot
        else:
            self.__table[slot].append(Entry(key,data))
            return slot

    def get(self, key:any)->any:
        '''
            Método que retorna a carga na tabela de dispersão
            correspondente a chave informada.
            Argumentos:
                key(Any): chave do elemento a ser buscado.
            Retorna:
                Any: valor do elemento buscado.
            Raises:
                KeyError: se a chave não for encontrada na tabela de dispersão.
        '''
        slot = self.__hash(key)
        for i in range(len(self.__table[slot])):
            if key == self.__table[slot][i].key:
                return self.__table[slot][i].value
        else:
            raise KeyError(f'key {key} not found')

    def remove(self, key:any)->any:
        '''
            Método que remove um elemento da tabela de dispersão.
            Argumentos:
                key(Any): chave do elemento a ser removido.
            Retorna:
                Any: valor do elemento removido.
            Raises:
                KeyError: se a chave não for encontrada na tabela de dispersão.
        '''
        slot = self.__hash(key)
        for i in range(len(self.__table[slot])):
            if key == self.__table[slot][i].key:
                return self.__table[slot].pop(i).value
        else:
            raise KeyError(f'key {key} not found')

    def items(self)->List[tuple]:
        '''
            Método que retorna uma lista com todos os pares chave/valor da tabela de dispersão.
            Retorna:
                list: lista com todos os pares chave/valor da tabela de dispersão.
        '''
        lista = []
        for items in self.__table:
            if items == None:
                continue
            for entry in items:
                lista.append((entry.key, entry.value))
        return lista

    def __getitem__(self, key):
        return self.get(key)
    
    def __setitem__(self, key, data):
        self.put(key, data)

    def __contains__(self, key):
        '''
            Método que verifica se uma chave está na tabela de dispersão.
            Argumentos:
                key(Any): chave do elemento a ser buscado.
            Retorna:
                bool: True se a chave estiver na tabela de dispersão e False caso contrário.
        '''
        slot = self.__hash(key)
        for i in range(len(self.__table[slot])):
            if key == self.__table[slot][i].key:
                return True
        else:
            return False
        
    def __str__(self):
        info = "{"
        for items in self.__table:
            if items == None:
                continue
            for entry in items:
                info += f'{entry.key}:{entry.value},'
        info = info.rstrip(',') + '}'
        return info

    def showHashTable(self):
        entrada = -1
        print('+--+')
        for items in self.__table:
            entrada += 1
            print(f'|{entrada:2d}| = ', end='') 
            if len(items) == 0:
                print(' None')
                continue
            for entry in items:
                print(f'[ {entry.key},{entry.value} ] ',end='')
            print()
        print('+--+')