import socket
import os
import sys
import signal
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Pedido import *

MAX_MESSAGE_SIZE = 1024
HOST = 'localhost'
PORT = 40000

if len(sys.argv) == 2:
    HOST = sys.argv[1]
elif len(sys.argv) == 3:
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])

CODIGOS_SERVIDOR = {
    '200': 'Cliente encontrado com sucesso!',
    '201': 'Pedido registrado com sucesso!',
    '204': 'Desconexão efetuada com sucesso!',
    '400': 'Cliente não encontrado.',
    '401': 'Quantidade não disponível no estoque.',
    '405': 'Número inválido.',
    '406': 'ISBN inexistente'
}

#PEDIDO
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
        client_socket.send("QUIT".encode())
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
                _, resposta = enviar_mensagem("GET_BOOKS").split("-", 1)
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
                pedido.menuCarrinho(enviar_mensagem, lista)

            elif choice == '3':
                cls()
                resposta = enviar_mensagem(f"FINALIZAR")
                if resposta == "201":
                    print(CODIGOS_SERVIDOR['201'])
                else:
                    _, ganhador = resposta.split("-", 1)
                    numero_sorteado, cpfComprador = comprador.split("-", 1)
                    print(f'\nSORTEIO!\n\nNumero sorteado: {numero_sorteado}\nCPF do ganhador: {cpf_ganhador}\n')

            elif choice == '4':
                resposta = enviar_mensagem("QUIT")
                if resposta == "204":
                    print('Volte sempre!')
                    break

            else:
                cls()
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
        1 - Exibir catálogo de livros
        2 - Abrir carrinho
        3 - Finalizar pedido
        4 - Encerrar
    ''')
    choice = input("Digite a opção desejada: ")
    return choice


if __name__ == '__main__':
    main()