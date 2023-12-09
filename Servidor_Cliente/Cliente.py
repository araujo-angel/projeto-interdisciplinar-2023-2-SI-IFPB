import socket
import os
import sys
import signal

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
            choice = mostrar_menu()

            if choice == '1':
                cls()
                _, resposta = enviar_mensagem("GET_BOOKS").split("-", 1)
                print(f'Livros disponíveis:\n{resposta}')
                comprarLivro(enviar_mensagem)

            elif choice == '2':
                cls()
                codigo, resposta = enviar_mensagem(f"COMPRADOS").split("-", 1)
                print(CODIGOS_SERVIDOR[codigo])
                print(resposta)

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


def comprarLivro(enviar_mensagem):
    isbn = inputISBN()
    quantidade = inputQtd()
    resposta = enviar_mensagem(f"COMPRAR {isbn} {quantidade}")
    # codigo, resposta = enviar_mensagem("VALIDAR").split("-", 1)
    if isbn != '':
        print(CODIGOS_SERVIDOR[resposta])
    else:
        print(CODIGOS_SERVIDOR[resposta])


def inputISBN():
    while True:
        isbn = input("Digite o ISBN do livro desejado: ")
        if isbn.isdigit():
            cls()
            return isbn
        else:
            print("Entrada inválida. Digite apenas números.")


def inputQtd():
    while True:
        qtdLivros = input("Digite a quantidade desejada: ")
        if qtdLivros.isdigit():
            cls()
            return qtdLivros
        else:
            print("Entrada inválida. Digite apenas números.")


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
    

def mostrar_menu():
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