from DataStructure.ChainingHashTable import *

class CompradorException(Exception):
    '''
    Classe referente ao tratamento de erros.
    '''
    def __init__(self, msg):
        super().__init__(msg)

class Comprador:
    """
    Classe referente aos dados do comprador.
    """
    def __init__(self, cpf:str, nome:str, telefone:int, cep:int):
        self.__cpf = cpf
        self.__nome = nome
        self.__telefone = telefone
        self.__cep = cep
        self.__pagamento = None
        self.__troco = None

    def getCpf(self):
        return self.__cpf

    def getNome(self):
        return self.__nome

    def getTelefone(self):
        return self.__telefone

    def getCep(self):
        return self.__pagamento

    def getPagamento(self):
        return self.__pagamento

    def getTroco(self):
        return self.__troco

    def setCpf(self, novoCpf):
        self.__cpf = novoCpf

    def setNome(self, novoNome):
        self.__nome = novoNome

    def setTelefone(self, novoTelefone):
        self.__telefone = novoTelefone

    def setCep(self, novoCep):
        self.__cep = novoCep

    def setPagamento(self, formaPagamento):
        if formaPagamento == '1':
            self.__pagamento = 'Cartão'
        elif formaPagamento == '2':
            self.__pagamento = 'Dinheiro'

    def setTroco(self, troco):
        self.__troco = troco

    def __str__(self):
        return f'CPF: {self.__cpf} | Nome: {self.__nome} | Telefone: {self.__telefone} | CEP: {self.__cep} | {self.__pagamento} | Troco: {self.__troco}'