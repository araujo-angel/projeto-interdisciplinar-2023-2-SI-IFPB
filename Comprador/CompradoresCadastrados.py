from DataStructure.ChainingHashTable import *
from Comprador.Comprador import *

class CompradoresCadastradosException(Exception):
    '''
    Classe referente ao tratamento de erros.
    '''
    def __init__(self, msg):
        super().__init__(msg)

class CompradoresCadastrados:
    def __init__(self):
        self.__compradores = ChainingHashTable()

    def cadastrarCompradorDoArquivo(self, nome_arquivo):
        try:
            with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
                linhas = arquivo.readlines()

                for linha in linhas:
                    # Dividir a linha usando a vírgula como delimitador
                    atributos = linha.strip().split(',')

                    # Remover as aspas dos atributos de string
                    cpf = atributos[0].strip(' "')
                    nome = atributos[1].strip(' "')
                    telefone = int(atributos[2].strip())
                    cep = int(atributos[3].strip())

                    # Chamar o método cadastrarLivro para cada linha
                    resultado = self.cadastrarComprador(cpf, nome, telefone, cep)
                    print(resultado)

            print("Cadastro de compradores concluído.")
        except FileNotFoundError:
            raise CompradoresCadastradosException(f"Erro ao ler o arquivo: {nome_arquivo}")
    
    def cadastrarComprador(self, cpf, nome, telefone, cep):
        novoComprador = Comprador(cpf, nome, telefone, cep)
        self.__compradores.put(novoComprador.getCpf(), novoComprador)

        return self.__compradores.get(cpf)
    
    def verificarClienteCadastrado(self, cpf):
        """
        Verifica se um cliente está cadastrado.
        Retorna True se o cliente estiver cadastrado e False caso contrário.
        """
        return cpf in self.__compradores.keys()
    
    def __str__(self):
        compradores_str = "\n".join(str(cliente) for cliente in self.__compradores.values())
        return f"\nCompradores cadastrados:\n{compradores_str}"
