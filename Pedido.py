from DataStructure.ListaEncadeada import *
from Livros.EstoqueDeLivros import *


class PedidoException(Exception):
    """Classe de exceção lançada quando uma violação no acesso aos elementos do pedido é identificada.
    """
    def __init__(self,msg):
        """ Construtor padrão da classe, que recebe uma mensagem que se deseja embutir na exceção.
        """
        super().__init__(msg)

class Pedido:
    """
    Classe referente ao processo de compra dos livros.
    """
    def __init__(self):
        self.__pedido = Lista()

    def getLista(self):
        return self.__pedido

    def inputISBN(self):
        while True:
            isbn = input("Digite o ISBN do livro: ")
            if isbn.isdigit():
                return isbn
            else:
                print("Entrada inválida. Digite apenas números.")

    def inputQtd(self):
        while True:
            qtdLivros = input("Digite a quantidade desejada: ")
            if qtdLivros.isdigit() and int(qtdLivros)>0:
                return qtdLivros
            else:
                print("Entrada inválida. Digite apenas números maiores que zero")  

    def livroExistente(self,isbn):
        """
        Verifica se um livro com o ISBN fornecido já está no pedido.
        Retorna True se encontrado, False caso contrário.
        """
        try:
            return self.obterLivroPorISBN(isbn) is not None
        except ListaException:
            return False
        
    def obterLivroPorISBN(self, isbn):
        '''
        Método que encontra o livro desejado pelo ISBN passado.
        '''
        if not self.__pedido.estaVazia():
            try:
                for i, pedidoLocal in enumerate(self.__pedido):
                    if pedidoLocal[0] == isbn:
                        livro = self.__pedido.elemento(i+1)
                        return livro
            except:
                print('Livro não encontrado')
                return None

        else:
            return None
            
    def obterQuantidadeDeLivroNoPedido(self, isbn):
        """
        Verifica a 'Quantidade' do livro com o ISBN fornecido
        """
        try:
            for i, pedidoLocal in enumerate(self.__pedido):
                if pedidoLocal[0] == isbn:
                    return pedidoLocal[3]
        except ListaException:
            return None
        
    def quantidadeISBNsDiferentes(self):
        """
        Retorna a quantidade de ISBNs diferentes na lista de pedidos.
        """
        isbn_set = set()
        for i, pedidoLocal in enumerate(self.__pedido):
            isbn = pedidoLocal[0]
            if isbn not in isbn_set:
                isbn_set.add(isbn)

        return len(isbn_set)

    def comprarLivro(self, isbn, titulo, preco, qtd, estoqueDisponivel):
        isbn = isbn
        titulo = titulo
        preco = preco
        qtd = qtd
        estoqueDisponivel = estoqueDisponivel
        # Verifica se o ISBN já existe na self.__pedido do pedido
        if self.livroExistente(isbn):
            # ISBN já existe na self.__pedido, incrementa a quantidade
            
            quantidade_atual = self.obterQuantidadeDeLivroNoPedido(isbn)

            if int(qtd) <= int(estoqueDisponivel):
                for i, pedidoLocal in enumerate(self.__pedido):
                    if pedidoLocal[0] == isbn:
                        pedidoLocal[3] = int(qtd)
            else:
                print("Quantidade desejada não disponível em estoque.")
                return
            
            info = [isbn, titulo, preco, qtd]
            self.__pedido.append(info)
            return self.__pedido
        else:                
            info = [isbn, titulo, preco, qtd]
            self.__pedido.append(info)
            return self.__pedido
    
    def removerLivroPorIsbn(self, isbn):
        '''
        Remove livro pelo ISBN passado.
        '''
        #Remove um livro do pedido com base no ISBN. Retorna True se removido com sucesso, False se o ISBN não for encontrado.
        for i, pedidoLocal in enumerate(self.__pedido):
            if pedidoLocal[0] == isbn:
                self.__pedido.remover(i+1)
                return True
        return False
    
    def alterarQuantidadeDoPedido(self, isbn, quantidade):
        '''
        Método que altera a quantidade desejada do livro.
        '''
        for i, pedidoLocal in enumerate(self.__pedido):
            if pedidoLocal[0] == isbn:
                pedidoLocal[3] = quantidade
                return True
        return False
    
    
    def calcularPrecoTotal(self):   
        '''
        Calcula o preco total do pedido feito.
        '''
        total = 0
        for pedidoLocal in self.__pedido:
            total += int(pedidoLocal[2]) * int(pedidoLocal[3])
        return total


    def __str__(self) -> str:
        return f'Pedidos: {self.__pedido}'
    
