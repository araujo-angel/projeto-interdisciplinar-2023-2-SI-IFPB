from EstoqueDeLivros import *

estoque = EstoqueDeLivros()
# estoque.cadastrarLivro("Assim que acaba", 43300245, "Collen Hover", 20)
# estoque.cadastrarLivro("A metamorfose", 8571646856, "Franz Kafka", 10)

estoque.cadastrarLivroDoArquivo('livros.txt')

print(estoque)

isbn_a_decrementar = 8535909559
quantidade_a_decrementar = 5

estoque.decrementarQuantidadeLivros(isbn_a_decrementar, quantidade_a_decrementar)
print(estoque)

estoque.atualizarArquivoLivros('livros.txt')