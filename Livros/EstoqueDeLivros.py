from Livros.Livro import *
from DataStructure.ChainingHashTable import *

"""
Classe que controla a quantidade de livros da aplicação.
"""

class EstoqueDeLivros:
    def __init__(self):
        self.__livros = ChainingHashTable()
        #self.__qtdNoEstoque = 0

    def cadastrarLivroDoArquivo(self, nome_arquivo):
        try:
            with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
                linhas = arquivo.readlines()

                for linha in linhas:
                    # Dividir a linha usando a vírgula como delimitador
                    atributos = linha.strip().split(',')

                    # Remover as aspas dos atributos de string
                    titulo = atributos[0].strip(' "')
                    isbn = int(atributos[1].strip())
                    autor = atributos[2].strip(' "')
                    preco = int(atributos[3].strip())
                    qtdDeLivros = int(atributos[4].strip())

                    # Chamar o método cadastrarLivro para cada linha
                    resultado = self.cadastrarLivro(titulo, isbn, autor, preco, qtdDeLivros)
                    print(resultado)

            print("Cadastro de livros concluído.")
        except Exception as e:
            print(f"Erro ao ler o arquivo: {e}")
 

    def cadastrarLivro(self, titulo, isbn, autor, preco, qtdDeLivros):
        novoLivro = Livros(titulo, isbn, autor, preco, qtdDeLivros)
        self.__livros.put(novoLivro.getIsbn(), novoLivro)
        #self.__qtdNoEstoque += qtdDeLivros

        return self.__livros.get(isbn)
    
    def decrementarQuantidadeLivros(self, isbn, quantidade):
        try:
            livro = self.__livros.get(isbn)

            if livro:
                quantidade_atual = livro.getQtdDeLivros()
                if quantidade_atual >= quantidade:
                    livro.setQtdDeLivros(quantidade_atual - quantidade)
                    #self.__qtdNoEstoque -= quantidade
                    print(f"Quantidade de '{livro.getTitulo()}' decrementada em {quantidade}. Nova quantidade: {livro.getQtdDeLivros()}")
                else:
                    print(f"Erro: Não há quantidade suficiente de '{livro.getTitulo()}' para decrementar.")
            else:
                print(f"Livro com ISBN {isbn} não encontrado no estoque.")

        except Exception as e:
            print(f"Erro ao decrementar a quantidade de livros: {e}")

    def atualizarArquivoLivros(self, nome_arquivo):
        try:
            with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
                for isbn, livro in self.__livros.items():
                    linha = f'"{livro.getTitulo()}", {isbn}, "{livro.getAutor()}", "{livro.getPreco()}", {livro.getQtdDeLivros()}\n'
                    arquivo.write(linha)

            print(f"Arquivo {nome_arquivo} atualizado com sucesso.")
        except Exception as e:
            print(f"Erro ao atualizar o arquivo: {e}")

    
    def __str__(self):
        livros_str = "\n".join(str(livro) for livro in self.__livros.values())
        return f"Quantidade no Estoque: {self.__livros.__len__()}\nLivros no Estoque:\n{livros_str}"