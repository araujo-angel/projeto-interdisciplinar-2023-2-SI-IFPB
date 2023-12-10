from DataStructure.ListaEncadeadaOrdenada import Lista
from Livros.EstoqueDeLivros import *

"""
Classe referente ao processo de compra dos livros.
"""
class Pedido:
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

    
    def removerLivroPorISBN(self, lista, isbn):
        for pedido in lista:
            if isbn in pedido:
                del lista[lista.index(pedido)]
                print(f"Livro com ISBN {isbn} removido.")
                return lista

        print(f"Livro com ISBN {isbn} não encontrado.")
        return lista

    def obterLivroPorISBN(self, isbn):
        posicao = self.__pedido.busca(isbn)
        livro = self.__pedido.elemento(posicao)
        return livro
        #criar exceção


    def calcularPrecoTotal(self, lista):
        total = 0
        for pedido in lista:
            for info in pedido.values():
                total += int(info['Preço']) * int(info['Quantidade'])
        return total

    def menuCarrinho(self, enviar_mensagem, lista):
        print('*****Carrinho*****')
        if len(lista) == 0:
            print("Seu carrinho está vazio! Adicione um livro!")
            print("\n1 - Adicionar livro")
            print("\n2 - Voltar")
        else:
            for i, pedido in enumerate(lista, start=1):
                info = pedido[next(iter(pedido))]  
                
                print(f"{i}. 'ISBN': '{info['ISBN']}', 'Título': '{info['Título']}', 'Preço': '{info['Preço']}', 'Quantidade': '{info['Quantidade']}'")

            print(f'Total: {calcularPrecoTotal(lista)}')
            print("\n1 - Remover livro")
            print("\n2 - Adicionar livro")
            print("\n3 - Voltar")
        
        escolha = input("\nEscolha uma opção: ").lower()
        if escolha == '1' and len(lista) != 0:
            isbn = inputISBN()
            removerLivroPorISBN(lista, isbn)
            menuCarrinho(enviar_mensagem, lista)
        elif (escolha == '2' and len(lista) != 0) or (escolha == '1' and len(lista) == 0):
            cls()
            _, resposta = enviar_mensagem("GET_BOOKS").split("-", 1)
            print(f'Livros disponíveis:\n{resposta}')
            compra = comprarLivro(enviar_mensagem, lista)
        elif (escolha == '3' and len(lista) != 0) or (escolha == '2' and len(lista) == 0):
            return
    

    
    def comprarLivro(self, enviar_mensagem):
        isbn = self.inputISBN()
        qtd = self.inputQtd()

        # Verifica se o ISBN já existe na lista
        livro_existente = self.obterLivroPorISBN(isbn)

        resposta = enviar_mensagem(f"COMPRAR {isbn} {qtd}").split('-')
        codigo = resposta[0]
        
        if codigo == '201':
            titulo = resposta[1]
            preco = resposta[2]
            print(CODIGOS_SERVIDOR[codigo])

            if livro_existente:
                # ISBN já existe na lista, incrementa a quantidade
                estoque_disponivel = int(enviar_mensagem(f"QTLIVRO {isbn}"))
                quantidade_atual = int(livro_existente['Quantidade'])

                if quantidade_atual + int(quantidade) > estoque_disponivel:
                    print("Quantidade desejada não disponível em estoque.")
                    return

                livro_existente['Quantidade'] = int(quantidade) + quantidade_atual
                print(f"Quantidade do livro com ISBN {isbn} incrementada para {livro_existente['Quantidade']}.")
            else:
                info = {'ISBN': isbn, 'Título': titulo, 'Preço': preco, 'Quantidade': quantidade}
                item = isbn
                pedido = {item: info}
                lista.append(pedido)
                print(lista)
            return lista
        else:
            print(CODIGOS_SERVIDOR[codigo])

    def __str__(self) -> str:
        return f'Pedido {self.__id}: {self.__pedido}'
