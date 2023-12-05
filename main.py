from Livros.EstoqueDeLivros import *
from Comprador.CompradoresCadastrados import *

estoque = EstoqueDeLivros()
#estoque.cadastrarLivro("Assim que acaba", 43300245, "Collen Hover", 20)
#estoque.cadastrarLivro("A metamorfose", 8571646856, "Franz Kafka", 10)
#estoque.cadastrarLivro("O mundo de Sofia", 1234567890, "Jostien Gaarder", 20)
#estoque.cadastrarLivro("Fundação", 2345678901, "Isaac Asimov", 30)
#estoque.cadastrarLivro("A hora da Estrela", 4567890234, "Clarice Lispector", 11)


estoque.cadastrarLivroDoArquivo('Livros\Livros.txt')

print(estoque)

isbn_a_decrementar = 7439874262
quantidade_a_decrementar = 2

estoque.decrementarQuantidadeLivros(isbn_a_decrementar, quantidade_a_decrementar)
print(estoque)

estoque.atualizarArquivoLivros('Livros\Livros.txt')

cliente = CompradoresCadastrados()

cliente.cadastrarCompradorDoArquivo('Comprador\Compradores.txt')

print(cliente)

#cpf_a_verificar = "12345678901"
cpf_a_verificar = "87654325666"

if cliente.verificarClienteCadastrado(cpf_a_verificar):
    print("Cliente cadastrado.")
    # Faça outras operações relacionadas a clientes
else:
    print("Cliente não cadastrado.")
    # Realize operações apropriadas para lidar com clientes não cadastrados
