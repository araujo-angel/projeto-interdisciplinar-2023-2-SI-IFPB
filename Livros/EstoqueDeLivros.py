from Livros.Livro import *
from DataStructure.ChainingHashTable import *


class EstoqueDeLivrosException(Exception):
    '''
    Classe referente ao tratamento de erros.
    '''
    def __init__(self, msg):
        super().__init__(msg)

class EstoqueDeLivros:
    """
    Classe que controla a quantidade de livros da aplicação.
    """
    def __init__(self):
        self.__livros = ChainingHashTable()

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
                    qtdDeLivros = int(atributos[3].strip())
                    preco = int(atributos[4].strip())

                    # Chamar o método cadastrarLivro para cada linha
                    resultado = self.cadastrarLivro(titulo, isbn, autor, qtdDeLivros, preco)
                    print(resultado)

            print("Cadastro de livros concluído.\n")
        except FileNotFoundError:
            raise EstoqueDeLivrosException(f"Erro ao ler o arquivo: {nome_arquivo}")
 

    def cadastrarLivro(self, titulo, isbn, autor, qtdDeLivros, preco):
        novoLivro = Livros(titulo, isbn, autor, qtdDeLivros, preco)
        self.__livros.put(novoLivro.getIsbn(), novoLivro)
        return self.__livros.get(isbn)
    
    def verificarLivroCadastrado(self, isbn):
        """
        Verifica se um livro está cadastrado.
        Retorna True se o livro estiver cadastrado e False caso contrário.
        """
        return isbn in self.__livros.keys()
    
    def verificarDisponibilidade(self, isbn, quantidadeDesejada):
        livro = self.__livros.get(isbn)

        if livro:
            quantidadeDisponivel = livro.getQtdDeLivros()

            if quantidadeDisponivel >= quantidadeDesejada:
                print(f"Quantidade desejada de '{livro.getTitulo()}' disponível no estoque.")
                return True
            else:
                print(f"Não há quantidade suficiente de '{livro.getTitulo()}' no estoque.")
                return False
        else:
            print(f"Livro com ISBN {isbn} não encontrado no estoque.")
            return False

    def decrementarQuantidadeLivros(self, isbn, quantidade):
        try:
            livro = self.__livros.get(isbn)

            quantidade_atual = livro.getQtdDeLivros()

            livro.setQtdDeLivros(quantidade_atual - quantidade)
            print(f"Quantidade de '{livro.getTitulo()}' decrementada em {quantidade}. Nova quantidade: {livro.getQtdDeLivros()}")

        except:
            raise EstoqueDeLivros(f"Erro ao decrementar a quantidade de livros.")

    def atualizarArquivoLivros(self, nome_arquivo):
        try:
            with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
                for isbn, livro in self.__livros.items():
                    linha = f'"{livro.getTitulo()}", {isbn}, "{livro.getAutor()}", {livro.getQtdDeLivros()}, {livro.getPreco()}\n'
                    arquivo.write(linha)

            print(f"Arquivo {nome_arquivo} atualizado com sucesso.")
        except:
            raise EstoqueDeLivrosException(f"Erro ao atualizar o arquivo: {nome_arquivo}")

    def catalogo(self):
        # Lista para armazenar as strings representando cada livro no catálogo
        catalogo = []
        for livro in self.__livros.values():
            info_livro = f"ISBN: {livro.getIsbn()}, Título: {livro.getTitulo()}, Autor: {livro.getAutor()}, Preço: {livro.getPreco()}\n"
            catalogo.append(info_livro)

        return catalogo
    
    def obterLivro(self, isbn):
        livro = self.__livros.get(isbn)
        return livro
    
    def obterQuantidadeLivro(self, isbn):
        livro = self.__livros.get(isbn)

        if livro:
            return livro.getQtdDeLivros()
        else:
            print(f"Livro com ISBN {isbn} não encontrado no estoque.")
            return 0  
    
    def __str__(self):
        livros_str = "\n".join(str(livro) for livro in self.__livros.values())
        return f"Títulos no Estoque: {self.__livros.__len__()}\nLivros no Estoque:\n{livros_str}"