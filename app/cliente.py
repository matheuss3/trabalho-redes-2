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

import util
from mensagens import *

def main(login, senha):
  # Dados da conexão
  HOST = 'localhost'
  PORT = 3333
  # Configurando socket TCP
  tcp = socket(AF_INET, SOCK_STREAM)
  tcp.connect((HOST, PORT))
  dest = (HOST, PORT)

  # Realizando login
  print('Dados do usuário')
  print(f'Usuário: {login}')
  print(f'Senha: {senha}')
  print()

  # Autenticando usuário
  mensagemAutenticacao = AutenticacaoReq()
  msg = mensagemAutenticacao.pack(login, senha)
  tcp.send(msg)

  # Recebendo token do servidor
  autenticacaoRes = AutenticacaoRes()
  msg = tcp.recv(autenticacaoRes.tamanho)
  autenticacaoRes.unpack(msg)
  token = autenticacaoRes.token
  print('Token do servidor')
  print(autenticacaoRes.mensagem)
  print(f'Token recebido : {token}')
  print()

  # Encerrando conexão caso token não tenha sido gerado
  if (token == -1):
    print('Conexão encerrada')
    tcp.close()
    exit()

  # Solicitando lista de pedidos
  solListaPedidos = ListaPedidosReq()
  msg = solListaPedidos.pack(token)
  tcp.send(msg)

  # Recebe quantidade de pedidos feitos
  msgQtdPedidos = PossuiPedidos()
  msg = tcp.recv(msgQtdPedidos.tamanho)
  msgQtdPedidos.unpack(msg)
  print(f'Você possui {msgQtdPedidos.qtdPedidos} itens pedidos!')

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
  solListaEstoque = EstoqueReq()
  msg = solListaEstoque.pack(token)
  tcp.send(msg)

  print('--------------Estoque da loja----------------')
  # Recebendo estoque
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

  # Escolhe se deseja realizar pedido
  print('Deseja criar um pedido?', end=' ')
  escolha = random.randint(0,1)
  #Enviando pro servidor a escolha 
  criacaoPedidoReq = CriacaoPedidoReq() 
  msg = criacaoPedidoReq.pack(escolha, token)
  tcp.send(msg)

  while (escolha == 1):
    print('Sim 😀')
    # Cria pedido 
    pedidos = util.criaPedidoConsumidor(estoque)

    print('------------Novo pedido------------')
    print(json.dumps(pedidos, indent=2))
    print('-----------------------------------\n')
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

    # Recebendo estoque
    print('--------------Estoque atualizado-----------')
    estoque = []
    while True:
      estoqueRes = EstoqueRes()
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
    print('----------------------------------------\n')
    
    print('Deseja criar um novo pedido?', end=' ')
    escolha = random.randint(0,1)
    msg = criacaoPedidoReq.pack(escolha, token)
    tcp.send(msg)
  else:
    print("Não") 
    print('Conexão encerrada 😢')
    tcp.close()
    exit()
  
if __name__ == '__main__':
  if len(sys.argv) == 3:
    main(sys.argv[1], sys.argv[2])
  
  main('matheus', '1234')