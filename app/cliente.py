"""
Disciplina de Redes de Computadores
Autor:  Matheus de Souza e Thaís de Souza
Matrícula: 20191bsi0301 e 20191bsi0263 
Trabalho: Loja de produtos esportivos - Trabalho 2
Semestre: 2021/2
Data de conclusão: 12/01/2022
"""

import sys
from socket import *
import random
import json
from time import sleep, time
import util
from mensagens import *

def encerraConexao(tcp):
  print('Conexão encerrada')
  tcp.close()
  exit()

def main(login, senha):

  # Dados da conexão
  HOST = 'localhost'
  PORT = 3333

  # Configurando socket TCP
  tcp = socket(AF_INET, SOCK_STREAM)

  # Solicitando nome do login e senha (já preenchendo)
  print('\nOlá! Informe dados de login e senha:\n')
  print(f'Usuário: {login}')
  print(f'Senha: {senha}')
  
  # Conectando no servidor
  tcp.connect((HOST, PORT))
  dest = (HOST, PORT)

  # Pedindo requisição de autenticação
  print('\nPedindo requisição de autenticação...')
  mensagemAutenticacao = AutenticacaoReq()
  msg = mensagemAutenticacao.pack(login, senha)
  tcp.send(msg)

  # token do servidor (token negativo caso: usuário não cadastrado ou senha incorreta)
  autenticacaoRes = AutenticacaoRes()
  msg = tcp.recv(autenticacaoRes.tamanho)
  autenticacaoRes.unpack(msg)
  token = autenticacaoRes.token
  print(autenticacaoRes.mensagem)
  print(f'{dest}: Token recebido : {token}')
  print()

  # Encerrando conexão caso token não tenha sido gerado
  if (token == -1):
    encerraConexao(tcp)

#LOOP------------------------
  while True:

    # Solicitando lista de pedidos
    print("\nSolicitando os pedidos que já fiz...")
    solListaPedidos = ListaPedidosReq()
    msg = solListaPedidos.pack(token)
    tcp.send(msg)

    # Recebe quantidade de pedidos feitos
    msgQtdPedidos = PossuiPedidos()
    msg = tcp.recv(msgQtdPedidos.tamanho)
    msgQtdPedidos.unpack(msg)
    print("Lista de pedidos recebida com sucesso!\n")
    print(f'{dest}Você possui {msgQtdPedidos.qtdPedidos} itens pedidos!')

    # Recebe pedidos
    print('-----------------Meus pedidos----------------')
    while True and msgQtdPedidos.qtdPedidos > 0:
      pedidoRes = PedidoRes()
      msg = tcp.recv(pedidoRes.tamanho)
      pedidoRes.unpack(msg)
      
      print(f'Pedido: {pedidoRes.idPedido}')
      print(f'Item: {pedidoRes.item}\tFlag: {pedidoRes.flag}')
      print(f'Quantidade: {pedidoRes.quantidade}\tValor Unitario: {pedidoRes.valorUnitario}')
      print()

      if pedidoRes.flag == 1:
        break
    print('---------------------------------------------\n')

    #Solicitando lista de estoque
    print("Solicitando estoque da loja...\n")
    solListaEstoque = EstoqueReq()
    msg = solListaEstoque.pack(token)
    tcp.send(msg)

    # Recebendo estoque
    print("Estoque recebido com sucesso!\n")
    print('--------------Estoque da loja----------------')
    estoque = []
    while True:
      estoqueRes= EstoqueRes()
      msg = tcp.recv(estoqueRes.tamanho)
      estoqueRes.unpack(msg)

      item = {
        'item' : estoqueRes.item,
        'descricao' : estoqueRes.descricao,
        'quantidade' : estoqueRes.quantidade,
        'valorUnitario' : estoqueRes.valorUnitario 
      }
      estoque.append(item)

      #Imprimindo estoque
      print(f'Item: {estoqueRes.item}\tDescrição: {estoqueRes.descricao}')
      print(f'Quantidade: {estoqueRes.quantidade}\tValor Unitario: {estoqueRes.valorUnitario}')
      print(f'Flag: {estoqueRes.flag}')
      print()

      if estoqueRes.flag == 1:
        break
    print('---------------------------------------------\n')

    # Escolhe de forma aleatória se deseja realizar pedido
    print('Deseja criar um pedido?', end=' ')
    escolha = random.randint(0,1)

    if (escolha == 1):
      
      print('Sim 😀')

      # Enviando pro servidor a escolha 
      criacaoPedidoReq = CriacaoPedidoReq() 
      msg = criacaoPedidoReq.pack(token)
      tcp.send(msg)

      # Cria pedido 
      print("Criando pedido...\n")
      pedidos = util.criaPedidoConsumidor(estoque)
      if (pedidos):
        print('------------Novo pedido------------')
        print(json.dumps(pedidos, indent=2))
        print('-----------------------------------\n')
      else:
        print('-----Loja sem estoque de itens-----')
        encerraConexao(tcp)

      # Enviando pedido pro servidor
      for pedido in pedidos:
        pedidoClienteRes = PedidoClienteRes()
        flag = 0
        if pedido == pedidos[-1]:
          flag = 1
        
        msg = pedidoClienteRes.pack(pedido['item'], pedido['qtdPedida'], pedido['valorUnitario'], flag)
        tcp.send(msg)

      # Recebe se pedido tem disponibilidade
      disponibilidadeRes = DisponibilidadeRes()
      msg = tcp.recv(disponibilidadeRes.tamanho)
      disponibilidadeRes.unpack(msg)
      token = disponibilidadeRes.token
      print(disponibilidadeRes.mensagem)
      
      # Conexão encerrada devido a falta de disponibilidade em estoque
      if token == -1: # Não tem disponibilidade
        print('Conexão encerrada')
        tcp.close()
        exit()

      print('Pedido gerado com sucesso!')
      print()
    else:
      encerrarConReq = EncerrarConexaoReq() 
      msg = encerrarConReq.pack()
      tcp.send(msg)
      print("Não 😢") 
      encerraConexao(tcp)
  
if __name__ == '__main__':
  if len(sys.argv) == 3:
    main(sys.argv[1], sys.argv[2])
  
  main('matheus', '1234')