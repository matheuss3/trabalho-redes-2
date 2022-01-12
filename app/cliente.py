from socket import *
import util
import random

from mensagens import AutenticacaoReq, AutenticacaoRes, EstoqueReq, EstoqueRes, ListaPedidosReq, PedidoRes

# Exemplo de cliente
cliente = {
  'id': 1,
  'nome': 'Matheus',
  'login': 'matheus',
  'senha': '1234'
}

# Dados da conexão
HOST = 'localhost'
PORT = 3333

tcp = socket(AF_INET, SOCK_STREAM)
tcp.connect((HOST, PORT))
dest = (HOST, PORT)  

# Realizando login
login = input('Informe o login: ') # 20 String 
senha = input('Digite sua senha: ') # 10 String
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
escolha = random.choice(0,1)
while (escolha == 1):
  pedidos = util.criaPedidoConsumidor(estoque)

  #FALTA ENVIAR OS PEDIDOS PRO SERVER
  #FALTA VERIFICAR QTD EM ESTOQUE (DISPONIBILIDADE)

  print(dest, "Servidor: Deseja criar um pedido? \n")
  escolha = random.choice(0,1)
else:
  print("não") 
  print('Conexão encerrada')
  tcp.close()
  exit()



