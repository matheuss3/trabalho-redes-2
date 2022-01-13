from socket import *
from mensagens import *
import util
import _thread
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
  
  #não tem permissão para acessar lista de pedidos
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
  
  #não tem permissão para acessar estoque
  if solListaEstoque.token != token: 
    conexao.close()
    print('Conexão encerrada')
    _thread.exit()

  #Pegando estoque 
  estoque = util.getEstoque()
  print(estoque)

  #Enviando lista de estoque para usuário
  for e in estoque:
    estoqueRes = EstoqueRes()
    flag = 0
    if e == estoque[-1]: #se for a última linha
      flag = 1
    conexao.send(estoqueRes.pack(e['item'], e['descricao'], e['quantidade'], e['valorUnitario'], flag))
  
  # Recebendo se o cliente deseja realizar um pedido
  criacaoPedidoReq = CriacaoPedidoReq()
  criacaoPedidoReq.unpack(conexao.recv(criacaoPedidoReq.tamanho))
  while criacaoPedidoReq.flag == 1: 
    listaItensPedido = []
    
    # Recebe pedidos do cliente
    while True: # Percorre itens do pedido até o pedido acabar
      pedidoClienteRes = PedidoClienteRes()
      pedidoClienteRes.unpack(conexao.recv(pedidoClienteRes.tamanho))

      itemPedido = {
        'item': pedidoClienteRes.item,
        'qtdPedida': pedidoClienteRes.quantidade
      }

      listaItensPedido.append(itemPedido) # Pedido do cliente
      
      #Imprimindo pedido do cliente
      print('Imprimindo pedido recebido: ')
      print(f'Item: {pedidoClienteRes.item}')
      print(f'Quantidade: {pedidoClienteRes.quantidade}')
      print(f'Valor Unitario: {pedidoClienteRes.valorUnitario}')
      print(f'Flag: {pedidoClienteRes.flag}')
      print('############################')

      if pedidoClienteRes.flag == 1:
        break
    
    #Verifica disponibilidade do pedido recebido
    pedido, estoqueAtualizado = util.atendePedidoCliente(listaItensPedido)

    #Informa cliente que pedido não tem disponibilidade
    if not pedido: # Não tem disponibilidade de estoque
      print('Pedido rejeitado')

      disponibilidadeRes = DisponibilidadeRes()
      msg = disponibilidadeRes.pack('Pedido rejeitado - Não há disponibilidade de estoque', -1)
      conexao.send(msg)

    # Informa cliente que pedido tem disponibilidade
    disponibilidadeRes = DisponibilidadeRes()
    msg = disponibilidadeRes.pack('Pedido aceito - Há disponibilidade de estoque', token)
    conexao.send(msg)
    print('Pedido efetuado com sucesso')
    print(pedido)

    #Salvando pedido realizado no arquivo de pedidos
    util.atualizaPedidos(pedido,idUsuario)

    #Enviando estoque atualizado para cliente
    for e in estoqueAtualizado:
      estoqueRes = EstoqueRes()
      flag = 0
      if e == estestoqueAtualizado[-1]: #se for a última linha
        flag = 1
      conexao.send(estoqueRes.pack(e['item'], e['descricao'], e['quantidade'], e['valorUnitario'], flag))
    #criar função recebe estoque (pq toda hora ele atualiza)
    
    criacaoPedidoReq.unpack(conexao.recv(criacaoPedidoReq.tamanho))
  else:  #Não quer criar novo pedido
    conexao.close()
    print('Conexão encerrada')
    _thread.exit()


# Configuração do socket tcp
tcp = socket(AF_INET, SOCK_STREAM)
tcp.bind((HOST, PORT))
tcp.listen(10)

while True:
  con, cliente = tcp.accept()  #aceita conexão
  _thread.start_new_thread(atendeCliente, (con, cliente))   #começa uma nova thread

