from enum import Flag
from socket import *

from mensagens import AutenticacaoReq, AutenticacaoRes, ListaPedidosReq, PedidoRes

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

# Realizando login
login = input('Informe o login: ') # 20 String 
senha = input('Digite sua senha: ') # 10 String
mensagemAutenticacao = AutenticacaoReq()
tcp.send(mensagemAutenticacao.pack(login, senha))

# Recebendo token do servidor
autenticacaoRes = AutenticacaoRes()
autenticacaoRes.unpack(tcp.recv(autenticacaoRes.tamanho))
token = autenticacaoRes.token
print(f'Token recebido - {token}')


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