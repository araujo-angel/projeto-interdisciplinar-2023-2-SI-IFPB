from DataStructure.ListaEncadeadaOrdenada import Lista

"""
Classe referente ao processo de compra dos livros.
"""
# class Pedido:
#     def __init__(self):
#         self.__pedido = Lista()
#         self.__id = 0

#     def getLista(self):
#         return self.__pedido
    
#     def getId(self):
#         return self.__id
    
#     def __str__(self) -> str:
#         return f'Pedido {self.__id}: {self.__pedido}'



def carrinho_pedidos(Lista):
    global v_total
    global cardapio
    global menu
    print("===Carrinho===\n")
    if Lista.estaVazia():
        print("Seu carrinho está vazio! Adicione um livro!")
        print("\n1 - Adicionar item")
        print("\n2 - Voltar")
    else:
        print(Lista)
        print(f'Total: {v_total:.2f}')
        print("\n1 - Remover item")
        print("\n2 - Adicionar item")
        print("\n3 - Voltar")
    
    escolha = input("\nEscolha uma opção: ").lower()
    if escolha == '1' and not Lista.estaVazia():
        item = input('Insira o ISBN do livro: ').capitalize()
        remove_quantidade = int(input('Quantidade a remover: '))
        try:
            if len(item) < 9:
                produto = Lista.elemento(int(item))
                quant = produto[1]
                if remove_quantidade >= quant: 
                    Lista.remover(int(item)) 
                    
                else:
                    new_quant = quant - remove_quantidade   
                    produto[1] = new_quant
                    
            
            for item in cardapio:
                if (item[0] == produto[0]) and (remove_quantidade < quant):
                    v_remove = remove_quantidade * float(item[1])
                    v_total -= v_remove
                elif(item[0] == produto[0]) and (remove_quantidade >= quant):
                    v_total -= (quant * float(item[1]))
                    
                                
            carrinho_pedidos(Lista)
        except ListaException as le:
            print(le)
            input()
            carrinho_pedidos(lista)
    elif (escolha == '2' and not Lista.estaVazia()) or (escolha == '1' and lista.estaVazia()):
        menu = '1'
        return menu
    elif (escolha == '3' and not lista.estaVazia()) or (escolha == '2' and lista.estaVazia()):
        menu = options()
        return menu