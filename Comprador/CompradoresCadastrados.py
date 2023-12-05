from DataStructure.ChainingHashTable import *
from Comprador.Comprador import *

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
        except Exception as e:
            print(f"Erro ao ler o arquivo: {e}")
    
    def cadastrarComprador(self, cpf, nome, telefone, cep):
        novoComprador = Comprador(cpf, nome, telefone, cep)
        self.__compradores.put(novoComprador.getCpf(), novoComprador)

        return self.__compradores.get(cpf)
    
    def __str__(self):
        compradores_str = "\n".join(str(cliente) for cliente in self.__compradores.values())
        return f"\nCompradores cadastrados:\n{compradores_str}"
