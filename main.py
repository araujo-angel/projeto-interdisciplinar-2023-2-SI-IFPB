from Livros.EstoqueDeLivros import *
from Comprador.CompradoresCadastrados import *

estoque = EstoqueDeLivros()
#estoque.cadastrarLivro("Assim que acaba", 43300245, "Collen Hover", 20)
#estoque.cadastrarLivro("A metamorfose", 8571646856, "Franz Kafka", 10)
#estoque.cadastrarLivro("O mundo de Sofia", 1234567890, "Jostien Gaarder", 20)
#estoque.cadastrarLivro("Fundação", 2345678901, "Isaac Asimov", 30)
#estoque.cadastrarLivro("A hora da Estrela", 4567890234, "Clarice Lispector", 11)


estoque.cadastrarLivroDoArquivo('livros.txt')

print(estoque)

isbn_a_decrementar = 8535909559
quantidade_a_decrementar = 5

estoque.decrementarQuantidadeLivros(isbn_a_decrementar, quantidade_a_decrementar)
print(estoque)

estoque.atualizarArquivoLivros('Livros\Livros.txt')

cliente = CompradoresCadastrados()

cliente.cadastrarCompradorDoArquivo('Comprador\Compradores.txt')

print(cliente)
