import numpy as np

class FilaException(Exception):
    def __init__(self,mensagem):
        super().__init__(mensagem)


class Fila:
    def __init__(self, size:int=10):
        self.__array = np.full(size,None,dtype=object)
        self.__frente = 0
        self.__final  = -1
        self.__tamanho = 0
        
    def estaVazia(self)->bool:
        return self.__tamanho == 0

    def estaCheia(self)->bool:
        return self.__tamanho == len(self.__array)


    def __len__(self)->int:
        return self.__tamanho

    def elemento(self, posicao:int)->any:
        try:
            assert self.estaVazia() == False, 'Fila está vazia'
            assert posicao > 0 and posicao <= len(self), f'Posição {posicao} é inválida para a fila com {len(self)} elementos'
            
            index = self.__frente
            for i in range(posicao-1):
                index = (index + 1)%len(self.__array)
            

            return self.__array[index]
        except AssertionError as ae:
            raise FilaException(ae)
                
    def busca(self, key:any)->int:

        index = self.__frente
        for i in range(len(self)):
            if self.__array[index] == key:
                return i+1
            index = (index + 1)%len(self.__array)
        raise FilaException(f'A chave {key} não está presente na fila')


    def enfileira(self, carga:any):
        try:
            assert not self.estaCheia(), 'Fila está cheia'
            
            # if self.__final == len(self.__array)-1:
            #     self.__final = 0
            # else:
            #     self.__final += 1

            self.__final = (self.__final + 1)% len(self.__array)

            self.__array[self.__final] = carga
            
            self.__tamanho += 1

        except AssertionError as ae:
            raise FilaException(ae)


    def desenfileira(self)->any:
        try:
            assert not self.estaVazia(), 'Lista está vazia'

            carga = self.__array[self.__frente]

            self.__frente = (self.__frente + 1)% len(self.__array)
            self.__tamanho -= 1
            return carga
        except AssertionError as ae:
            raise FilaException(ae)

        

        
    def __str__(self)->str:
        """ Método que retorna a ordenação atual dos elementos da pilha, do
            topo em direção à base

        Returns:
           str: a carga dos elementos da pilha, do topo até a base
        """  
        s = 'frente->[ '
        index = self.__frente
        for i in range(len(self)):
            s += f'{self.__array[index]}, '
            index = (index + 1)%len(self.__array)
        s = s.rstrip(', ')
        s += ' ]'
        return s
