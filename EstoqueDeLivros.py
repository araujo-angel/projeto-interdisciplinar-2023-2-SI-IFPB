from Livros import Livros
from DataStructure.HashTable import *

class EstoqueDeLivros:
    def __init__(self):
        self.__qtdNoEstoque = 0
        self.__livros = HashTable()
 

    def cadastrarLivro(self, titulo, isbn, autor, qtdDeLivros):
        novoLivro = Livros(titulo, isbn, autor, qtdDeLivros)
        # titulo = novoLivro.setTitulo(titulo)
        # isbn = novoLivro.setIsbn(isbn)
        # autor = novoLivro.setAutor(autor)
        # qtdDeLivros = novoLivro.setQtdDeLivros(qtdDeLivros)

        self.__livros.put(novoLivro.getIsbn(), novoLivro)
        self.__qtdNoEstoque += qtdDeLivros


        return self.__livros




