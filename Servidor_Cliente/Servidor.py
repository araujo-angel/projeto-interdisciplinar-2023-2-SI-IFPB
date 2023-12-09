import socket
import threading
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Livros.EstoqueDeLivros import *
from DataStructure.ListaEncadeadaOrdenada import *
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

            # if msg_client.startswith("REGISTRAR"):
            #     cpf_registrado = self.registrar_cliente(client_socket, msg_client)

            if msg_client.startswith("GET_BOOKS"):
                self.exibirCatalogo(client_socket)

            if msg_client.startswith("COMPRAR"):
                 self.comprarLivro(client_socket, cpfCliente, msg_client)

            # Compra da rifa, é adicionada na tabela o numero da rifa e cpf do comprador
            # if msg_client.startswith("COMPRAR"):
            #     self.comprar_rifa(client_socket, cpf_registrado, msg_client)

            # Lista os números disponíveis para compra
            # elif msg_client == "DISPONIVEIS":
            #     self.verificar_disponiveis(client_socket)

            # Mostra os números comprados pelo cliente
            elif msg_client == "COMPRADOS":
                with self.__lock_rifas:
                    client_socket.send(f"208-{self.__clientes.buscar(cpf_registrado)}".encode())

            # Desconecta o cliente
            elif msg_client == "QUIT":
                self.desconectar_cliente(client_socket)
                break

            # Verifica se os números disponiveis já esgotaram
            elif msg_client == "ESGOTOU":
                self.validar_esgotou(client_socket)

            # Realiza o sorteio, caso não existam mais números disponiveis
            elif msg_client == "SORTEIO":
                self.sortear(client_socket)

        client_socket.close()

#ACRESCENTADO!
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
        

    def registrar_cliente(self, client_socket, msg_client):
        with self.__lock_clientes:
            _, cpf = msg_client.split()
            cliente = self.__clientes.buscar(cpf)
            if cliente is None:
                self.__clientes.inserir(cpf, [])
                resposta = "200"
                client_socket.send(resposta.encode())
                return cpf
            else:
                resposta = "201"
                client_socket.send(resposta.encode())
                return cpf

    def comprar_rifa(self, client_socket, cpf_registrado, msg_client):
        with self.__lock_rifas:
            _, numero = msg_client.split()
            if int(numero) < 0 or int(numero) >= self.__gerenciador.get_tamanho():
                resposta = "400"
            else:
                numero_comprado = self.__gerenciador.comprar(int(numero), cpf_registrado)
                if numero_comprado > -1:
                    numeros_comprados_por_cliente = self.__clientes.buscar(cpf_registrado)
                    numeros_comprados_por_cliente.append(numero_comprado)
                    self.__clientes.set_valor(cpf_registrado, numeros_comprados_por_cliente)
                    resposta = f"202"
                else:
                    resposta = f"401"
            client_socket.send(resposta.encode())

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
                    #novo_pedido = Pedido(cpfCliente, isbn, quantidade)

                    resposta = "201"  # Código para pedido criado com sucesso
                else:
                    resposta = "401"  # Código para quantidade insuficiente em estoque
            else:
                resposta = "406"  # Código para ISBN inválido
                client_socket.send(resposta.encode())
                return


            client_socket.send(resposta.encode())

    def comprarLivro2(self, client_socket, cpfCliente, msg_client):
        with self.__lock_livros:
            _, isbn = msg_client.split()
            if int(numero) < 0 or int(numero) >= self.__gerenciador.get_tamanho():
                resposta = "400"
            else:
                numero_comprado = self.__gerenciador.comprar(int(numero), cpf_registrado)
                if numero_comprado > -1:
                    numeros_comprados_por_cliente = self.__clientes.buscar(cpf_registrado)
                    numeros_comprados_por_cliente.append(numero_comprado)
                    self.__clientes.set_valor(cpf_registrado, numeros_comprados_por_cliente)
                    resposta = f"202"
                else:
                    resposta = f"401"
            client_socket.send(resposta.encode())

    def verificar_disponiveis(self, client_socket):
        with self.__lock_compradores:
            livros = self.__gerenciador.numeros_nao_comprados()
            resposta = f"203-" + ", ".join(map(str, numeros))
            client_socket.send(resposta.encode())

    def exibirCatalogo(self, client_socket):
        with self.__lock_livros:
            catalogo = self.__estoque.catalogo()
            resposta = f"203-" + "\n".join(catalogo)
            client_socket.send(resposta.encode())

    def desconectar_cliente(self, client_socket):
        print("Cliente", client_socket.getpeername(), "desconectou!")
        enviar = "204"
        client_socket.send(enviar.encode())

    def validar_esgotou(self, client_socket):
        with self.__lock_rifas:
            if self.__gerenciador.esgotou():
                enviar = "205"
                client_socket.send(enviar.encode())
            else:
                enviar = "206"
                client_socket.send(enviar.encode())

    def sortear(self, client_socket):
        if self.__gerenciador.esgotou():
            mensagem = self.__gerenciador.sorteio()
            client_socket.send(f"207-{mensagem}".encode())
        else:
            enviar = "402"
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

