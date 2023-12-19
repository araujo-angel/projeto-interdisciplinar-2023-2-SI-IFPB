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

    def getCpf(self):
        return self.__cpf

    def getNome(self):
        return self.__nome

    def getTelefone(self):
        return self.__telefone

    def getCep(self):
        return self.__cep

    def setCpf(self, novoCpf):
        self.__cpf = novoCpf

    def setNome(self, novoNome):
        self.__nome = novoNome

    def setTelefone(self, novoTelefone):
        self.__telefone = novoTelefone

    def setCep(self, novoCep):
        self.__cep = novoCep


    def __str__(self):
        return f'CPF: {self.__cpf} | Nome: {self.__nome} | Telefone: {self.__telefone} | CEP: {self.__cep}'