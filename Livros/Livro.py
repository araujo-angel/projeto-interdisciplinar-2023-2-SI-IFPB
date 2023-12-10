class Livros:
    def __init__(self, titulo:str, isbn:int, autor:str, qtdDeLivros:int, preco:int):
        self.__titulo = titulo
        self.__isbn = isbn
        self.__autor = autor
        self.__qtdDeLivros = qtdDeLivros
        self.__preco = preco

    def getTitulo(self):
        return self.__titulo
    
    def getIsbn(self):
        return self.__isbn
    
    def getAutor(self):
        return self.__autor
    
    def getQtdDeLivros(self):
        return self.__qtdDeLivros
    
    def getPreco(self):
        return self.__preco
    
    def setTitulo(self, novoTitulo):
        self.__titulo = novoTitulo

    def setIsbn(self, novoIsbn):
        self.__isbn = novoIsbn

    def setAutor(self, novoAutor):
        self.__autor = novoAutor

    def setQtdDeLivros(self, novoQtdDeLivros):
        self.__qtdDeLivros = novoQtdDeLivros

    def setPreco(self, novoPreco):
        self.__preco = novoPreco

    def __str__(self):
        return f"{self.__titulo} (ISBN: {self.__isbn}, Autor: {self.__autor}, Quantidade: {self.__qtdDeLivros}, Preço: {self.__preco})"
