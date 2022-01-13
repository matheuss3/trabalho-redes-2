import sys
from socket import *
import random

import util
from mensagens import *

def main(login, senha):
  # Dados da conexão
  HOST = 'localhost'
  PORT = 3333

  tcp = socket(AF_INET, SOCK_STREAM)
  tcp.connect((HOST, PORT))
  dest = (HOST, PORT)

  # Realizando login
  # login = input('Informe o login: ') # 20 String 
  # senha = input('Digite sua senha: ') # 10 String

  mensagemAutenticacao = AutenticacaoReq()
  tcp.send(mensagemAutenticacao.pack(login, senha))

  # Recebendo token do servidor
  autenticacaoRes = AutenticacaoRes()
  autenticacaoRes.unpack(tcp.recv(autenticacaoRes.tamanho))
  token = autenticacaoRes.token
  print(autenticacaoRes.mensagem)
  print(f'Token recebido : {token}')

  if (token == -1):
    print('Conexão encerrada')
    tcp.close()
    exit()

  # Solicitando lista de pedidos
  solListaPedidos = ListaPedidosReq()
  tcp.send(solListaPedidos.pack(token))

  # Recebe pedidos
  while True:
    pedidoRes = PedidoRes()
    pedidoRes.unpack(tcp.recv(pedidoRes.tamanho))
    print(f'Pedido: {pedidoRes.idPedido}')
    print(f'Item: {pedidoRes.item}')
    print(f'Quantidade: {pedidoRes.quantidade}')
    print(f'Valor Unitario: {pedidoRes.valorUnitario}')
    print(f'Flag: {pedidoRes.flag}')
    print('############################')

    if pedidoRes.flag == 1:
      break

  #Solicitando lista de estoque
  solListaEstoque = EstoqueReq()
  tcp.send(solListaEstoque.pack(token))

  estoque = []
  # Recebe estoque
  while True:

    estoqueRes= EstoqueRes()
    estoqueRes.unpack(tcp.recv(estoqueRes.tamanho))
    item = {
      'item' : estoqueRes.item,
      'descricao' : estoqueRes.descricao,
      'quantidade' : estoqueRes.quantidade,
      'valorUnitario' : estoqueRes.valorUnitario 
    }
    estoque.append(item)

    print(f'Item: {estoqueRes.item}')
    print(f'Descrição: {estoqueRes.descricao}')
    print(f'Quantidade: {estoqueRes.quantidade}')
    print(f'Valor Unitario: {estoqueRes.valorUnitario}')
    print(f'Flag: {estoqueRes.flag}')
    print('############################')

    if estoqueRes.flag == 1:
      break

  # Cria pedidos
  print(dest, "Servidor: Deseja criar um pedido? \n")
  escolha = random.randint(0,1)
  criacaoPedidoReq = CriacaoPedidoReq()
  msg = criacaoPedidoReq.pack(escolha, token)
  tcp.send(msg)
  while (escolha == 1):
    pedidos = util.criaPedidoConsumidor(estoque)
    print(pedidos)

    #FALTA ENVIAR OS PEDIDOS PRO SERVER
    for pedido in pedidos:
      pedidoClienteRes = PedidoClienteRes()
      flag = 0
      if pedido == pedidos[-1]:
        flag = 1
      
      msg = pedidoClienteRes.pack(pedido['item'], pedido['qtdPedida'], pedido['valorUnitario'], flag)
      tcp.send(msg)
    
    print(dest, "Servidor: Deseja criar um pedido? \n")
    escolha = random.randint(0,1)
    msg = criacaoPedidoReq.pack(escolha, token)
    tcp.send(msg)
  else:
    print("não") 
    print('Conexão encerrada')
    tcp.close()
    exit()
  
  #FALTA VERIFICAR QTD EM ESTOQUE (DISPONIBILIDADE)

if __name__ == '__main__':
  if len(sys.argv) == 3:
    main(sys.argv[1], sys.argv[2])
  
  main('matheus', '1234')