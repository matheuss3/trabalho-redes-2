from socket import *
from mensagens import AutenticacaoReq, AutenticacaoRes, EstoqueReq, EstoqueRes, ListaPedidosReq, PedidoRes
import util
import _thread
import uuid
import random

# Dados da conexão
HOST = 'localhost'
PORT = 3333
BYTES_BY_MSG = 1024
CODING = 'UTF-8'

def autenticaClientes(login, senha):
  usuario = util.getUsuario(login)
  print(usuario)
  if usuario:
    if util.comparaStrings(usuario['senha'], senha):
      print('Gerando token para o cliente')
      return random.randint(0, 999999), usuario['id']
  
  return None,None


def atendeCliente(conexao, cliente):

  #recebendo mensagem de requisição de autenticação
  autenticacaoReq = AutenticacaoReq()
  msg = conexao.recv(autenticacaoReq.tamanho)
  autenticacaoReq.unpack(msg)

  token, idUsuario = autenticaClientes(autenticacaoReq.login, autenticacaoReq.senha)
  
  if not token:

    #enviando msgm para usuário informando login não cadastrado
    autenticacaoRes = AutenticacaoRes()
    msg = autenticacaoRes.pack('Acesso negado', -1)
    conexao.send(msg)

    #Encerrando conexão
    conexao.close()
    print('Conexão encerrada')
    _thread.exit()

  #Enviando token e mensagem de sucesso para usuário
  print(f'Token gerado para o usuário - {token}')
  autenticacaoRes = AutenticacaoRes()
  msg = autenticacaoRes.pack('Login efetuado com sucesso!',token)
  conexao.send(msg)

  #Recebendo solicitação da lista de pedidos do usuário
  solListaPedidos = ListaPedidosReq()
  solListaPedidos.unpack(conexao.recv(solListaPedidos.tamanho))
  
  #não tem permissão
  if solListaPedidos.token != token: 
    conexao.close()
    print('Conexão encerrada')
    _thread.exit()
  
  #Acessando lista de pedidos cadastrados
  pedidos = util.getPedidosUsuario(idUsuario)
  print(pedidos)
  
  #Enviando lista de pedidos para usuário
  for pedido in pedidos:
    pedidoRes = PedidoRes()
    flag = 0
    if pedido == pedidos[-1]:
      flag = 1
    conexao.send(pedidoRes.pack(pedido['id'], pedido['idItem'], pedido['quantidade'], pedido['valorUnitario'], flag))

  #Recebendo solicitação de estoque 
  solListaEstoque = EstoqueReq()
  solListaEstoque.unpack(conexao.recv(solListaEstoque.tamanho))
  
  #não tem permissão
  if solListaEstoque.token != token: 
    conexao.close()
    print('Conexão encerrada')
    _thread.exit()

  #Acessando estoque 
  estoque = util.getEstoque()
  print(estoque)

  #Enviando lista de estoque para usuário
  for e in estoque:
    estoqueRes = EstoqueRes()
    flag = 0
    if e == estoque[-1]: #se for a última linha
      flag = 1
    conexao.send(estoqueRes.pack(e['item'], e['descricao'], e['quantidade'], e['valorUnitario'], flag))


# Configuração do socket tcp
tcp = socket(AF_INET, SOCK_STREAM)
tcp.bind((HOST, PORT))
tcp.listen(10)

while True:
  con, cliente = tcp.accept()
  _thread.start_new_thread(atendeCliente, (con, cliente))

