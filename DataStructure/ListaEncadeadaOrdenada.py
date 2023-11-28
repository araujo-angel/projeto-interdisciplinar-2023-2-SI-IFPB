class ListaException(Exception):
    """Classe de exceção lançada quando uma violação de ordem genérica
       da lista é identificada.
    """

    def __init__(self,msg):
        """ Construtor padrão da classe, que recebe uma mensagem que se deseja
            embutir na exceção
        """
        super().__init__(msg)



class Node:
    '''
    Classe de objetos para criação de um nó dinâmico na memória
    '''
    def __init__(self,data):
        self.__data = data
        self.__next = None
    
    @property
    def data(self):
        return self.__data
    
    @data.setter
    def data(self, newData):
        self.__data = newData

    @property
    def next(self):
        return self.__next
    
    @next.setter
    def next(self, newNext):
        self.__next = newNext

    def hasNext(self):
        return self.__next != None
    
    def __str__(self):
        return str(self.__data)

   
	    
class Lista:
    '''
    Classe de objetos para armazenamento e gerenciamento de elementos
    de uma lista simplesmente encadeada ordenada.
    Nesse tipo de lista, os elementos são inseridos de forma ordenada
    de acordo com a chave de ordenação.
    '''
    def __init__(self):
        self.__head = None
        self.__tamanho = 0

    def estaVazia(self)->bool:
        '''
        Verifica se a lista está vazia
        Retorno:
          True se a lista estiver vazia e False caso contrário
        '''
        return self.__tamanho == 0 

    def __len__(self)->int:
        '''
        Retorna o número de elementos armazenados na lista
        '''
        return self.__tamanho

    def elemento(self, posicao:int)->any:
        '''
        Retorna a carga armazenada em um elemento especificado pela posição
        indicada como parâmetro.
        Parâmetros:
          posicao(int): a posição do elemento desejado
        Retorno:
          o elemento armazenado na posição especificada
        Raises:
            ListaException: se a posição for inválida ou a lista estiver vazia
        '''
        try:
            assert not self.estaVazia(), 'Lista vazia'
            assert posicao > 0 and posicao <= len(self), f'Posicao invalida. Lista contém {self.__tamanho} elementos'

            cursor = self.__head
            contador = 1
            while( cursor != None  and contador < posicao):
                cursor = cursor.next
                contador += 1

            return cursor.data

        except AssertionError as ae:
            raise ListaException(ae)



    def modificar(self, posicao:int, carga: any):
        '''
        Modifica a carga de um elemento especificado pela posição
        indicada como parâmetro.
        Parâmetros:
          posicao(int): a posição do elemento desejado
          carga(any): a nova carga do elemento
        Raises:
            ListaException: se a posição for inválida ou a lista estiver vazia
        '''
        try:
            assert not self.estaVazia(), 'Lista vazia'
            assert posicao > 0 and posicao <= len(self), f'A posicao deve ser um inteiro > 0 e menor igual a {self.__tamanho}'

            cursor = self.__head
            contador = 1
            while( cursor != None and contador < posicao ):
                cursor = cursor.next
                contador += 1

            cursor.data = carga
        except TypeError:
            raise ListaException(f'A posição deve ser um número do tipo inteiro')            
        except AssertionError as ae:
            raise ListaException(ae.__str__())
   
    
    def busca(self, chave:any)->int:
        '''
        Busca um elemento na lista a partir de uma chave fornecida 
        como argumento.
        Parâmetros:
            chave(any): a chave de busca 
        Retorno:
            a posição do elemento na lista
        Raises:
            ListaException: se a chave não for encontrada ou a lista estiver vazia
        '''
        if (self.estaVazia()):
            raise ListaException(f'Lista vazia')

        cursor = self.__head
        contador = 1

        while( cursor != None ):
            if( cursor.data == chave):
                return contador
            cursor = cursor.next
            contador += 1
            
        raise ListaException(f'A chave {chave} não está armazenado na lista')

    def inserir(self, carga:any ):
        '''
        Insere um elemento na lista de forma ordenada.
        Parâmetros:
            carga(any): a carga do elemento a ser inserido
        '''
        # CONDICAO 1: insercao se a lista estiver vazia
        novoNo = Node(carga)
        if (self.estaVazia()):
            self.__head = novoNo
        elif (carga < self.__head.data):
            # CONDICAO 2: insercao na primeira posicao em uma lista nao vazia
            novoNo.next = self.__head
            self.__head = novoNo
        else:
            # CONDICAO 3: insercao apos a primeira posicao em lista nao vazia
            cursor = self.__head
            while (cursor.next is not None and cursor.next.data < carga):
                cursor = cursor.next

            novoNo.next = cursor.next
            cursor.next = novoNo
        self.__tamanho += 1

    def remover(self, posicao:int)->any:
        '''
        Remove um elemento da lista a partir de uma posição fornecida
        como argumento.
        Parâmetros:
            posicao(int): a posição do elemento a ser removido
        Retorno:
            a carga do elemento removido
        Raises:
            ListaException: se a posição for inválida ou a lista estiver vazia
        '''
        try:
            if( self.estaVazia() ):
                raise ListaException(f'Não é possível remover de uma lista vazia')
            
            assert posicao > 0 and posicao <= len(self), f'Posicao invalida. Lista contém {self.__tamanho} elementos'

            cursor = self.__head
            contador = 1

            while( contador <= posicao-1 ) :
                anterior = cursor
                cursor = cursor.next
                contador+=1

            data = cursor.data

            if( posicao == 1):
                self.__head = cursor.next
            else:
                anterior.next = cursor.next

            self.__tamanho -= 1
            return data
        
        except TypeError:
            raise ListaException(f'A posição deve ser um número inteiro')            
        except AssertionError:
            raise ListaException(f'A posicao não pode ser um número negativo')
      
              
    def __str__(self):
        '''
        Retorna uma representação em string da lista
        '''
        str = 'Lista: [ '
        if self.estaVazia():
            str+= ']'
            return str

        cursor = self.__head

        while( cursor != None ):
            str += f'{cursor.data}, '
            cursor = cursor.next

        str = str[:-2] + " ]"
        return str

    # Métodos para implementação do protocolo "Iterator"
    def __iter__(self)->any:
        self.__ponteiro = self.__head
        return self
    
    def __next__(self)->any:
        if (self.__ponteiro == None):
            raise StopIteration
        else:
            carga = self.__ponteiro.data
            self.__ponteiro = self.__ponteiro.next
            return carga
