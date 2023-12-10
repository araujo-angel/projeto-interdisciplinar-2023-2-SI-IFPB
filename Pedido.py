from DataStructure.ListaEncadeadaOrdenada import Lista
from Livros.EstoqueDeLivros import *

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
            if qtdLivros.isdigit():
                return qtdLivros
            else:
                print("Entrada inválida. Digite apenas números.")  

    def livroExistente(self,isbn):
        if not self.obterLivroPorISBN(isbn):
            return False  

    def obterLivroPorISBN(self, isbn):
        posicao = self.__pedido.busca(isbn)
        livro = self.__pedido.elemento(posicao)
        return livro
        #criar exceção

    def comprarLivro(self, isbn, titulo, preco, qtd, estoqueDisponivel):
        isbn = isbn
        titulo = titulo
        preco = preco
        qtd = qtd
        estoqueDisponivel = estoqueDisponivel
        # Verifica se o ISBN já existe na self.__pedido do pedido
        if self.livroExistente(isbn):
            # ISBN já existe na self.__pedido, incrementa a quantidade
            quantidade_atual = self.__pedido[isbn]['Quantidade']
            if quantidade_atual + int(qtd) > estoqueDisponivel:
                print("Quantidade desejada não disponível em estoque.")
                return
            self.__pedido[isbn]['Quantidade'] = int(qtd) + quantidade_atual
            print(f"Quantidade do livro com ISBN {isbn} incrementada para {self.__pedido[isbn]['Quantidade']}.")
        else:
            info = {'ISBN': isbn, 'Título': titulo, 'Preço': preco, 'Quantidade': qtd}
            item = isbn
            pedido = {item: info}
            self.__pedido.inserir(pedido)
            print(self.__pedido)
            return self.__pedido

    def removerLivroPorISBN(self, isbn):
        for pedido in self.__pedido:
            if isbn in pedido:
                del self.__pedido[self.__pedido.index(pedido)]
                print(f"Livro com ISBN {isbn} removido.")
                return self.__pedido

        print(f"Livro com ISBN {isbn} não encontrado.")
        return self.__pedido
    
    def calcularPrecoTotal(self):
        total = 0
        for pedido in self.__pedido:
            for info in pedido.values():
                total += int(info['Preço']) * int(info['Quantidade'])
        return total

    def menuCarrinho(self, enviar_mensagem):
        print('*****Carrinho*****')
        if len(self.__pedido) == 0:
            print("Seu carrinho está vazio! Adicione um livro!")
            print("\n1 - Adicionar livro")
            print("\n2 - Voltar")
        else:
            for i, pedido in enumerate(self.__pedido, start=1):
                info = pedido[next(iter(pedido))]  
                
                print(f"{i}. 'ISBN': '{info['ISBN']}', 'Título': '{info['Título']}', 'Preço': '{info['Preço']}', 'Quantidade': '{info['Quantidade']}'")

            print(f'Total: {self.calcularPrecoTotal(self.__pedido)}')
            print("\n1 - Remover livro")
            print("\n2 - Adicionar livro")
            print("\n3 - Voltar")
        
        escolha = input("\nEscolha uma opção: ").lower()
        if escolha == '1' and len(self.__pedido) != 0:
            isbn = self.inputISBN()
            self.removerLivroPorISBN(self.__pedido, isbn)
            self.menuCarrinho(enviar_mensagem, self.__pedido)
        elif (escolha == '2' and len(self.__pedido) != 0) or (escolha == '1' and len(self.__pedido) == 0):
            _, resposta = enviar_mensagem("GET_BOOKS").split("-", 1)
            print(f'Livros disponíveis:\n{resposta}')
            compra = self.comprarLivro(enviar_mensagem, self.__pedido)
        elif (escolha == '3' and len(self.__pedido) != 0) or (escolha == '2' and len(self.__pedido) == 0):
            return

    def __str__(self) -> str:
        return f'Pedido {self.__id}: {self.__pedido}'
