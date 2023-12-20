import socket
import os
import sys
import signal
from time import sleep
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Pedido import *

MAX_MESSAGE_SIZE = 1024
HOST = 'localhost'
PORT = 8000

if len(sys.argv) == 2:
    HOST = sys.argv[1]
elif len(sys.argv) == 3:
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])

CODIGOS_SERVIDOR = {
    '200': 'Cliente encontrado com sucesso!',
    '201': 'Pedido adicionado ao carrinho com sucesso!',
    '203': 'Catálogo enviado.',
    '204': 'Desconexão efetuada com sucesso!',
    '206': 'Compra finalizada com sucesso!',
    '207': 'Compra cancelada.',
    '211': 'Confira seu pedido.',
    '400': 'Cliente não encontrado.',
    '401': 'Quantidade não disponível no estoque.',
    '405': 'Dados incorretos, tente novamente.',
    '406': 'ISBN inválido',
    '440': 'Seu carrinho está vazio.',
    '444': 'Não foi possível comprar a quantidade desejada. ',
}

#Onde o pedido é instanciado (Lista encadeada)
pedido = Pedido()


def cls():
    '''
    Método que limpa o terminal de execução.
    '''
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    mensagem_servidor = client_socket.recv(MAX_MESSAGE_SIZE).decode()
    print(mensagem_servidor)

    def enviar_mensagem(mensagem):
        client_socket.send(mensagem.encode())
        return client_socket.recv(MAX_MESSAGE_SIZE).decode()
    
    def ctrl_c_handler(signum, frame):
        print("\nEncerrando o programa.")
        client_socket.send("SAIR".encode())
        sys.exit(0)

    signal.signal(signal.SIGINT, ctrl_c_handler)

    resposta = enviar_mensagem(f"VALIDAR {inputCPF()}")
    print(CODIGOS_SERVIDOR[resposta])
    while CODIGOS_SERVIDOR[resposta] != 'Cliente encontrado com sucesso!':
        resposta = enviar_mensagem(f"VALIDAR {inputCPF()}")
        print(CODIGOS_SERVIDOR[resposta])

    if CODIGOS_SERVIDOR[resposta] == 'Cliente encontrado com sucesso!':
        while True:
            choice = mostrarMenu()

            if choice == '1':
                cls()
                _, resposta = enviar_mensagem("CATALOGO").split("-", 1)
                print(f'Livros disponíveis:\n{resposta}')
                isbn = pedido.inputISBN()
                qtd = pedido.inputQtd()

                resposta = enviar_mensagem(f"COMPRAR {isbn} {qtd}").split('-')
                codigo = resposta[0]
                if codigo == '201':
                    titulo = resposta[1]
                    preco = resposta[2]
                    print(CODIGOS_SERVIDOR[codigo])
                    estoque_disponivel = int(enviar_mensagem(f"QTLIVRO {isbn}"))
                    compra = pedido.comprarLivro(isbn, titulo, preco, qtd, estoque_disponivel)
                else:
                    print(CODIGOS_SERVIDOR[codigo])
                   

            elif choice == '2':
                cls()
                menuCarrinho(enviar_mensagem)


            elif choice == '3':
                resposta = enviar_mensagem(f"FINALIZAR-{pedido.quantidadeISBNsDiferentes()}-{str(pedido.getLista())}").split('-')
                
                codigo = resposta[0]
                
                # Analisa a resposta do servidor após selecionar "finalizar pedido"
                if codigo == "440" or codigo =="444":
                    # Carrinho vazio ou quantidade desejada não disponível
                    print(CODIGOS_SERVIDOR[codigo])
                    sleep(2)
                    continue
                elif codigo == "211":
                    print(CODIGOS_SERVIDOR[codigo])
                    
                    livros_disponiveis = resposta[1]
                    
                    # Mostra apenas os livros disponíveis para a compra
                    print("Livros disponíveis do seu carrinho:")
                    print(livros_disponiveis)

                    # Oferece escolha ao cliente para finalizar a compra
                    escolha = input("Deseja confirmar a compra? (s/n): ").lower()
                    
                    while escolha != 's' and escolha != 'n':
                        print('Opção inválida.')
                        escolha = input("Deseja confirmar a compra? (s/n): ").lower()
                    resposta_confirmar = enviar_mensagem(escolha)
                    if resposta_confirmar == "206":
                        #Compra finalizada com sucesso!
                        print(CODIGOS_SERVIDOR[resposta_confirmar])
                        total = client_socket.recv(MAX_MESSAGE_SIZE).decode()
                        print(f"Total: R${total}")
                        resposta = enviar_mensagem("SAIR")
                        if resposta == "204":
                            print('Volte sempre!')
                            break
                    elif resposta_confirmar == "207":
                        #Compra cancelada.
                        print(CODIGOS_SERVIDOR[resposta_confirmar])
                        sleep(2)
                        continue


            elif choice == '4':
                cls()
                resposta = enviar_mensagem("SAIR")
                if resposta == "204":
                    print('Volte sempre!')
                    break
        
            else:
                print("Opção inválida! Tente novamente.")

        client_socket.close()


def inputCPF():
    print('Para desfrutar de nossos serviços, é preciso estar cadastrado.')
    cpf = input("Digite o CPF ou ctrl+c para sair: ")
    while not validaCPF(cpf):
        cls()
        print("CPF inválido! Tente novamente.")
        cpf = input("Digite o CPF ou ctrl+c para sair: ")
    return cpf


def validaCPF(_cpf):
    if len(_cpf) == 11 and _cpf.isdigit():
        return True
    else:
        return False
    

def mostrarMenu():
    print('''
        ***MENU***
        1 - Comprar livros
        2 - Abrir carrinho
        3 - Finalizar pedido
        4 - Encerrar
    ''')
    choice = input("Digite a opção desejada: ")
    return choice

def menuCarrinho(enviar_mensagem):
        print('*****Carrinho*****')
        if pedido.getLista().estaVazia():
            print("Seu carrinho está vazio! Adicione um livro!")
            print("\n1 - Adicionar livro")
            print("\n2 - Voltar")
        else:
            for i, pedidoLocal in enumerate(pedido.getLista(), start=1):
                isbn = pedidoLocal[0]
                titulo = pedidoLocal[1]
                preco = pedidoLocal[2]
                quantidade = pedidoLocal[3]
                            
                print(f"{i}. 'ISBN': '{isbn}', 'Título': '{titulo}', 'Preço': '{preco}', 'Quantidade': '{quantidade}'")

            print(f'Total: R${pedido.calcularPrecoTotal()}')
            print("\n1 - Remover livro")
            print("\n2 - Alterar quantidade")
            print("\n3 - Voltar")
        
        escolha = input("\nEscolha uma opção: ").lower()

        # Se escolher "Remover livro"
        if escolha == '1' and not pedido.getLista().estaVazia():
            isbn = pedido.inputISBN()
            pedido.removerLivroPorIsbn(isbn)
            menuCarrinho(enviar_mensagem)

        # Se escolher "Adicionar livro" quando o carrinho está vazio
        elif (escolha == '1' and pedido.getLista().estaVazia()):
            cls()
            _, resposta = enviar_mensagem("CATALOGO").split("-", 1)
            print(f'Livros disponíveis:\n{resposta}')
            isbn = pedido.inputISBN()
            qtd = pedido.inputQtd()

            resposta = enviar_mensagem(f"COMPRAR {isbn} {qtd}").split('-')
            codigo = resposta[0]
            if codigo == '201':
                titulo = resposta[1]
                preco = resposta[2]
                print(CODIGOS_SERVIDOR[codigo])
                estoque_disponivel = int(enviar_mensagem(f"QTLIVRO {isbn}"))
                compra = pedido.comprarLivro(isbn, titulo, preco, qtd, estoque_disponivel)
            else:
                print(CODIGOS_SERVIDOR[codigo])

        # Se escolher "Alterar quantidade" no carrinho
        elif (escolha == '2' and not pedido.getLista().estaVazia()):
            isbn = pedido.inputISBN()
            qtd = pedido.inputQtd()

            estoque_disponivel = int(enviar_mensagem(f"QTLIVRO {isbn}"))
            if int(qtd) > estoque_disponivel:
                #quantidade não disponível no estoque
                print(CODIGOS_SERVIDOR['401'])
            else:
                if pedido.alterarQuantidadeDoPedido(isbn, qtd):
                    print('Quantidade alterada com sucesso')
                else:
                    print('Este livro não está no seu carrinho')

        # Se escolher "Voltar" para o menu inicial
        elif (escolha == '3' and not pedido.getLista().estaVazia()) or (escolha == '2' and pedido.getLista().estaVazia()):
            return

if __name__ == '__main__':
    main()