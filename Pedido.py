#from DataStructure.ListaSimplesmenteEncadeada import *
from DataStructure.ListaEncadeada import *
#from DataStructure.ListaEncadeadaOrdenada import *
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
        self.__id = 0

    def getLista(self):
        return self.__pedido

    def getId(self):
        return self.__id

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
            
            # if int(quantidade_atual) + int(qtd) > int(estoqueDisponivel):
            #     print("Quantidade desejada não disponível em estoque.")
            #     return
            # for i, pedidoLocal in enumerate(self.__pedido):
            #     if pedidoLocal[0] == isbn:
            #         pedidoLocal[3] = int(qtd) + int(quantidade_atual)
            #         print(f"Quantidade do livro com ISBN {isbn} incrementada para {pedidoLocal[3]}.")
            # return self.__pedido
        else:
            info = [isbn, titulo, preco, qtd]
            self.__pedido.append(info)
            return self.__pedido
    
    def removerLivroPorIsbnFor(self, isbn):
        """
        Remove um livro do pedido com base no ISBN.
        Retorna True se removido com sucesso, False se o ISBN não for encontrado.
        """
        for i, pedidoLocal in enumerate(self.__pedido):
            if pedidoLocal[0] == isbn:
                self.__pedido.remover(i+1)
                return True
        return False
    
    def alterarQuantidadeDoPedido(self, isbn, quantidade):
        for i, pedidoLocal in enumerate(self.__pedido):
            if pedidoLocal[0] == isbn:
                pedidoLocal[3] = quantidade
                return True
        return False
    

    
    def calcularPrecoTotal(self):   
        total = 0
        for pedidoLocal in self.__pedido:
            total += int(pedidoLocal[2]) * int(pedidoLocal[3])
        return total



    # def menuCarrinho(self):
    #     print('*****Carrinho*****')
    #     if self.__pedido.estaVazia():
    #         print("Seu carrinho está vazio! Adicione um livro!")
    #         print("\n1 - Adicionar livro")
    #         print("\n2 - Voltar")
    #     else:
    #         for i, pedido in enumerate(self.__pedido, start=1):
    #             info = pedido[next(iter(pedido))]  
                
    #             print(f"{i}. 'ISBN': '{info['ISBN']}', 'Título': '{info['Título']}', 'Preço': '{info['Preço']}', 'Quantidade': '{info['Quantidade']}'")

    #         print(f'Total: {self.calcularPrecoTotal(self.__pedido)}')
    #         print("\n1 - Remover livro")
    #         print("\n2 - Adicionar livro")
    #         print("\n3 - Voltar")
        
    #     escolha = input("\nEscolha uma opção: ").lower()
    #     if escolha == '1' and len(self.__pedido) != 0:
    #         isbn = self.inputISBN()
    #         self.removerLivroPorISBN(self.__pedido, isbn)
    #         self.menuCarrinho(enviar_mensagem, self.__pedido)
    #     elif (escolha == '2' and len(self.__pedido) != 0) or (escolha == '1' and len(self.__pedido) == 0):
    #         _, resposta = enviar_mensagem("GET_BOOKS").split("-", 1)
    #         print(f'Livros disponíveis:\n{resposta}')
    #         compra = self.comprarLivro(enviar_mensagem, self.__pedido)
    #     elif (escolha == '3' and len(self.__pedido) != 0) or (escolha == '2' and len(self.__pedido) == 0):
    #         return

    def __str__(self) -> str:
        return f'Pedido {self.__id}: {self.__pedido}'
    
