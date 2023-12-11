import socket
import threading
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Livros.EstoqueDeLivros import *
from DataStructure.ListaEncadeada import *
from Comprador.CompradoresCadastrados import *
from Pedido import *


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
        print(f"Servidor aguardando conexões em {self.__host}:{self.__port}")
        
        try:
            self.accept_connections()
        except KeyboardInterrupt:
            self.__server_socket.close() # Fecha socket do servidor quando clicar CTRL C

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
                print("Cliente", client_socket.getpeername(), "desconectou!")
                break

            if msg_client.startswith("VALIDAR"):
                cpfCliente = self.validarCliente(client_socket, msg_client)

            if msg_client.startswith("GET_BOOKS"):
                self.exibirCatalogo(client_socket)

            if msg_client.startswith("COMPRAR"):
                self.comprarLivro(client_socket, cpfCliente, msg_client)

            if msg_client.startswith("QTLIVRO"):
                self.quantidadeLivro(client_socket, cpfCliente, msg_client)

            if msg_client.startswith("FINALIZAR"):
                self.finalizarPedido(cpfCliente, client_socket, msg_client)

            # Desconecta o cliente
            elif msg_client == "QUIT":
                self.desconectar_cliente(client_socket)
                break

        client_socket.close()


    def validarCliente(self, client_socket, msg_client):
        with self.__lock_compradores:
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
            print(f'Cliente do CPF {cpfCliente} quer comprar {quantidade} livro(s) do ISBN {isbn}')
            try:
                isbn = int(isbn)
                quantidade = int(quantidade)
            except ValueError:
                print(f'Cliente do CPF {cpfCliente} tentou comprar {quantidade} livro(s) do ISBN {isbn}')
                resposta = "405"  # Código para quantidade ou ISBN inválido
                client_socket.send(resposta.encode())
                return
            
            if self.__estoque.verificarLivroCadastrado(isbn):
                if self.__estoque.verificarDisponibilidade(isbn, quantidade):
                    # Criar um pedido para o cliente
                    livro = self.__estoque.obterLivro(isbn)
                    titulo = livro.getTitulo()
                    preco = livro.getPreco()
                    resposta = f"201-{titulo}-{preco}"  # Código para pedido criado com sucesso
                else:
                    resposta = "401"  # Código para quantidade insuficiente em estoque
            else:
                print(f'Cliente do CPF {cpfCliente} digitou um ISBN inválido: {isbn}')
                resposta = "406"  # Código para ISBN inválido
                client_socket.send(resposta.encode())
                return


            client_socket.send(resposta.encode())

    def quantidadeLivro(self, client_socket, cpfCliente, msg_client):
        with self.__lock_livros:
            _, isbn = msg_client.split()

            print(f'Cliente do CPF {cpfCliente} quer verificar a quantidade em estoque do livro do ISBN {isbn}')
            try:
                isbn = int(isbn)
            except ValueError:
                resposta = "405"  # Código para quantidade ou ISBN inválido
                client_socket.send(resposta.encode())
                return
            
            if self.__estoque.verificarLivroCadastrado(isbn):
                    qtLivro = self.__estoque.obterQuantidadeLivro(isbn)
                    resposta = str(qtLivro)
                
            else:
                print(f'Cliente do CPF {cpfCliente} digitou um ISBN inválido: {isbn}')
                resposta = "406"  # Código para ISBN inválido
                client_socket.send(resposta.encode())
                return


            client_socket.send(resposta.encode())

    def exibirCatalogo(self, client_socket):
        with self.__lock_livros:
            catalogo = self.__estoque.catalogo()
            resposta = f"203-" + "\n".join(catalogo)
            client_socket.send(resposta.encode())


    def finalizarPedido(self, cpfCliente, client_socket, msg_client):
        if ' ' in msg_client:  # Verifica se há um espaço na mensagem
            _, listaDePedidos = msg_client.split(' ', 1)  # Faz a divisão em duas partes no primeiro espaço encontrado
            self.__pedidos.append(listaDePedidos)
            print("Cliente do CPF: ", cpfCliente, "finalizou sua compra!")
            enviar = "205-"
            client_socket.send(enviar.encode())
        else:
            # Caso a mensagem não esteja no formato esperado
            print("Formato de mensagem inválido para finalizar pedido:", msg_client)
   



        

    def desconectar_cliente(self, client_socket):
        print("Cliente", client_socket.getpeername(), "desconectou!")
        enviar = "204"
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
    PORT = 40000
    servidor = Server(HOST, PORT, MESSAGE_SIZE)
    servidor.start()

