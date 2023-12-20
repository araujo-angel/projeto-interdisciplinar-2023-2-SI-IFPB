import socket
import threading
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Livros.EstoqueDeLivros import *
from DataStructure.ListaEncadeada import *
from Comprador.CompradoresCadastrados import *
from Pedido import *
import ast

class Server:
    '''
    Classe responsável por gerenciar as conexões dos clientes
    '''    
    def __init__(self, host, port, message_size):
        self.__host = host
        self.__port = port
        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__estoque = EstoqueDeLivros()
        self.__max_message_size = message_size
        self.__lock_compradores = threading.Lock()
        self.__lock_livros = threading.Lock()
        self.__compradores = CompradoresCadastrados()
        self.__pedidos = Lista()

    # Inicia o servidor
    def start(self):
        self.prepararEstoque()
        self.prepararCompradores()

        self.__server_socket.bind((self.__host, self.__port))
        self.__server_socket.listen(1)
        print(f"\nServidor aguardando conexões em {self.__host}:{self.__port}")
        
        try:
            self.accept_connections()
        except KeyboardInterrupt:
            self.__server_socket.close()

    # Trata as conexões dos clientes
    def accept_connections(self):
        while True:
            client_socket, address = self.__server_socket.accept()
            print("Cliente conectado:", address)

            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    # Comunicação com o cliente/ respostas para o cliente
    def handle_client(self, client_socket):
        client_socket.send("Bem-vindo à Livraria Biblion!".encode())
        cpfCliente = ''

        while True:
            # Tratamento para quando o cliente desconectar
            try:
                msg_client = client_socket.recv(self.__max_message_size).decode()
            except ConnectionResetError:
                print("Cliente", client_socket.getpeername(), "desconectou!\n")
                break

            if msg_client.startswith("VALIDAR"):
                cpfCliente = self.validarCliente(client_socket, msg_client)

            if msg_client.startswith("CATALOGO"):
                self.exibirCatalogo(client_socket)

            if msg_client.startswith("COMPRAR"):
                self.comprarLivro(client_socket, cpfCliente, msg_client)

            if msg_client.startswith("QTLIVRO"):
                self.quantidadeLivro(client_socket, cpfCliente, msg_client)

            if msg_client.startswith("FINALIZAR"):
                self.finalizarPedido(cpfCliente, client_socket, msg_client)

            # Desconecta o cliente
            elif msg_client == "SAIR":
                self.desconectar_cliente(client_socket)
                break

        client_socket.close()


    def validarCliente(self, client_socket, msg_client):
        _, cpf = msg_client.split()
        if self.__compradores.verificarClienteCadastrado(cpf):
            print(f'Cliente conseguiu validar o CPF: {cpf}')
            resposta = "200"
            client_socket.send(resposta.encode())
            return cpf
        else:
            print(f'Cliente não conseguiu validar o CPF: {cpf}')
            resposta = "400"
            client_socket.send(resposta.encode())
            return cpf

    def comprarLivro(self, client_socket, cpfCliente, msg_client):
        with self.__lock_livros:
            _, isbn, quantidade = msg_client.split()
            
            try:
                isbn = int(isbn)
                quantidade = int(quantidade)
            except ValueError:
                print(f'Cliente do CPF {cpfCliente} tentou comprar {quantidade} livro(s) do ISBN {isbn}')
                resposta = "405"  # Dados incorretos, tente novamente.
                client_socket.send(resposta.encode())
                return
            
            if self.__estoque.verificarLivroCadastrado(isbn):
                if self.__estoque.verificarDisponibilidade(isbn, quantidade):
                    livro = self.__estoque.obterLivro(isbn)
                    titulo = livro.getTitulo()
                    preco = livro.getPreco()
                    resposta = f"201-{titulo}-{preco}"  # Pedido adicionado ao carrinho com sucesso!
                    print(f'Cliente do CPF {cpfCliente} adicionou ao carrinho {quantidade} livro(s) do ISBN {isbn}')
                else:
                    resposta = "401"  # Quantidade insuficiente em estoque
            else:
                print(f'Cliente do CPF {cpfCliente} digitou um ISBN inválido: {isbn}')
                resposta = "406"  # ISBN inválido
                client_socket.send(resposta.encode())
                return

            client_socket.send(resposta.encode())

    def quantidadeLivro(self, client_socket, cpfCliente, msg_client):
        _, isbn = msg_client.split()

        try:
            isbn = int(isbn)
        except ValueError:
            resposta = "405"  # Dados incorretos, tente novamente.
            client_socket.send(resposta.encode())
            return
        
        if self.__estoque.verificarLivroCadastrado(isbn):
                with self.__lock_livros:
                    qtLivro = self.__estoque.obterQuantidadeLivro(isbn)
                    resposta = str(qtLivro)
            
        else:
            print(f'Cliente do CPF {cpfCliente} digitou um ISBN inválido: {isbn}')
            resposta = "406"  # ISBN inválido
            client_socket.send(resposta.encode())
            return

        client_socket.send(resposta.encode())

    def exibirCatalogo(self, client_socket):
        catalogo = self.__estoque.catalogo()
        resposta = f"203-" + "\n".join(catalogo)
        client_socket.send(resposta.encode())

    def finalizarPedido(self, cpfCliente, client_socket, msg_client):
        with self.__lock_compradores:
            msg = msg_client.split('-')
            listaDePedidos = msg[2]
            tamLista = msg[1]
            tam = int(tamLista)

            if listaDePedidos:
                listaPedidos = ast.literal_eval(listaDePedidos)
            else:
                listaPedidos = ''

            if not listaPedidos or tam <= 0:
                # Lista de pedidos está vazia
                enviar = "440"
                client_socket.send(enviar.encode())
                return

            # Lista para armazenar os livros que o cliente conseguiu comprar
            livros_disponiveis = []
            livros_indisponiveis = []
            livros_disponiveis_decrementar = []
            
            total = 0

            if tam > 1:
                for i, pedidoLocal in enumerate(listaPedidos):

                    isbn = pedidoLocal[0]
                    titulo = pedidoLocal[1]
                    preco = pedidoLocal[2]
                    quantidade = pedidoLocal[3]

                    try:
                        isbn = int(isbn)
                        quantidade = int(quantidade)
                        preco = int(preco)
                    except ValueError:
                        resposta = "405"  # Dados incorretos, tente novamente.
                        client_socket.send(resposta.encode())
                        return
                    
                    # Verificar se o livro está cadastrado e se há quantidade disponível
                    if self.__estoque.verificarLivroCadastrado(isbn) and self.__estoque.verificarDisponibilidade(isbn, quantidade):
                        livros_disponiveis.append(f"\nISBN: {isbn}, Título: {titulo}, Quantidade: {quantidade}, Preço: R${preco}")
                        livros_disponiveis_decrementar.append([isbn, quantidade])

                        total += quantidade*preco
                    else:
                        # Livro não disponível
                        livros_indisponiveis.append(isbn)
            else:
                #Entra neste else, se a lista de pedidos do cliente só possuir um único título (ISBN)
                isbn = listaPedidos[0]
                titulo = listaPedidos[1]
                preco = listaPedidos[2]
                quantidade = listaPedidos[3]

                try:
                    isbn = int(isbn)
                    quantidade = int(quantidade)
                    preco = int(preco)
                except ValueError:
                    resposta = "405"  # Dados incorretos, tente novamente.
                    client_socket.send(resposta.encode())
                    return

                # Verificar se o livro está cadastrado e se há quantidade disponível
                if self.__estoque.verificarLivroCadastrado(isbn) and self.__estoque.verificarDisponibilidade(isbn, quantidade):
                    livros_disponiveis.append(f"\nISBN: {isbn}, Título: {titulo}, Quantidade: {quantidade}, Preço: R${preco}")
                    livros_disponiveis_decrementar.append([isbn, quantidade])

                    total += quantidade*preco
                else:
                    # Livro não disponível
                    livros_indisponiveis.append(isbn)

            if livros_disponiveis:
                livros_disponiveis.append(f"\nTotal: R${total}")
                # Pelo menos um livro está disponível, perguntar se cliente quer continuar
                enviar = f"211-{', '.join([str(livro) for livro in livros_disponiveis])}"
                client_socket.send(str(enviar).encode())

                # Aguardar escolha do cliente ('s' para confirmar, 'n' para cancelar)
                escolha = client_socket.recv(self.__max_message_size).decode()

                if escolha == 's':
                    # Cliente confirmou a compra
                    # Adicionar livros comprados à lista de pedidos no servidor
                    self.__pedidos.append(listaDePedidos)

                    # Atualizar estoque (elemento[0] é o ISBN e elemento[1] é a quantidade)
                    for elemento in livros_disponiveis_decrementar:
                        self.__estoque.decrementarQuantidadeLivros(elemento[0], elemento[1])
                    print(self.__estoque)

                    #Atualizar arquivo de texto do estoque
                    self.__estoque.atualizarArquivoLivros('Livros\Livros.txt')

                    print(f"\nCliente do CPF: {cpfCliente} finalizou sua compra!")
                    print(f"Pedidos realizados hoje:\n{self.__pedidos}")
                    enviar = "206" # Compra finalizada com sucesso!
                    client_socket.send(enviar.encode())
                    client_socket.send(str(total).encode())

                elif escolha == 'n':
                    # Cliente escolheu cancelar a compra
                    enviar = "207" # Compra cancelada.
                    client_socket.send(enviar.encode())
                    return
            else:
                # A quantidade do livro não está disponível, enviar código 444
                enviar = "444" #Não foi possível comprar a quantidade desejada.
                client_socket.send(enviar.encode())
 

    def desconectar_cliente(self, client_socket):
        print("Cliente", client_socket.getpeername(), "desconectou!")
        enviar = "204" # Desconexão efetuada com sucesso!
        client_socket.send(enviar.encode())

    def prepararEstoque(self):
        self.__estoque.cadastrarLivroDoArquivo('Livros\Livros.txt')

    def prepararCompradores(self):
        self.__compradores.cadastrarCompradorDoArquivo('Comprador\Compradores.txt')

    def atualizarEstoque(self):
        self.__estoque.atualizarArquivoLivros('Livros\Livros.txt')

if __name__ == '__main__':
    MESSAGE_SIZE = 1024
    HOST = '0.0.0.0'
    PORT = 8000
    servidor = Server(HOST, PORT, MESSAGE_SIZE)
    servidor.start()

