"""
Disciplina de Redes de Computadores
Autor:  Matheus de Souza e Thaís de Souza
Matrícula: 20191bsi0301 e 20191bsi0263 
Trabalho: Loja de produtos esportivos - Trabalho 2
Semestre: 2021/2
Data de conclusão: 12/01/2022
"""

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

def encerraConexao(conexao):

  conexao.close()
  print('Conexão encerrada')
  _thread.exit()


def autenticaClientes(login, senha):

  usuario = util.getUsuario(login)
  if usuario:
    if util.comparaStrings(usuario['senha'], senha):
      print('\n---- Gerando token para o cliente ',usuario['nome'],' ----')
      return random.randint(0, 999999), usuario['id']
  
  return None,None

def atendeCliente(conexao, cliente):

  #recebendo mensagem de requisição de autenticação
  autenticacaoReq = AutenticacaoReq()
  msg = conexao.recv(autenticacaoReq.tamanho)
  autenticacaoReq.unpack(msg)

  # Realizando autenticação do usuário
  token, idUsuario = autenticaClientes(autenticacaoReq.login, autenticacaoReq.senha)
  
  # ---- Enviando resposta de autenticação ----
  # -- Autenticação negada --
  if not token:

    #enviando msgm para usuário informando acesso negado
    autenticacaoRes = AutenticacaoRes()
    msg = autenticacaoRes.pack('Acesso negado', -1)
    conexao.send(msg)

    #Encerrando conexão com usuário
    encerraConexao(conexao)

  # -- Autenticação aceita --
  #Enviando token e mensagem de sucesso para usuário
  print(f'Token gerado - {token}')
  autenticacaoRes = AutenticacaoRes()
  msg = autenticacaoRes.pack('Login efetuado com sucesso!',token)
  conexao.send(msg)

  #Recebendo solicitação da lista de pedidos do usuário
  print("\nRecebendo solicitação da lista de pedidos do usuário...")
  solListaPedidos = ListaPedidosReq()
  solListaPedidos.unpack(conexao.recv(solListaPedidos.tamanho))
  
  #não tem permissão para acessar lista de pedidos
  if solListaPedidos.token != token: 
    encerraConexao(conexao)
  
  #Acessando lista de pedidos cadastrados
  print("Solicitação atendida com sucesso!")
  pedidos = util.getPedidosUsuario(idUsuario)
  
  #Enviando quantidade de pedidos que o cliente tem
  possuiPedidos = PossuiPedidos()
  msg = possuiPedidos.pack(len(pedidos))
  conexao.send(msg)

  #Enviando lista de pedidos para usuário
  print("Enviando lista de pedidos do usuário...")
  for pedido in pedidos:
    pedidoRes = PedidoRes()
    flag = 0
    if pedido == pedidos[-1]:
      flag = 1
    conexao.send(pedidoRes.pack(pedido['id'], pedido['idItem'], pedido['quantidade'], pedido['valorUnitario'], flag))
  print("Lista de pedidos enviada com sucesso!")

  #Recebendo solicitação de estoque 
  print("\nRecebendo solicitação de envio de estoque...")
  solListaEstoque = EstoqueReq()
  solListaEstoque.unpack(conexao.recv(solListaEstoque.tamanho))
  
  #não tem permissão para acessar estoque
  if solListaEstoque.token != token: 
    encerraConexao(conexao)

  #Pegando estoque 
  print("Solicitação atendida com sucesso!")
  estoque = util.getEstoque()

  #Enviando lista de estoque para usuário
  print("Enviando estoque...")
  for e in estoque:
    estoqueRes = EstoqueRes()
    flag = 0
    if e == estoque[-1]: #se for a última linha
      flag = 1
    conexao.send(estoqueRes.pack(e['item'], e['descricao'], e['quantidade'], e['valorUnitario'], flag))
  print("Estoque enviado com sucesso!")

  # Recebendo se o cliente deseja realizar um pedido
  criacaoPedidoReq = CriacaoPedidoReq()
  criacaoPedidoReq.unpack(conexao.recv(criacaoPedidoReq.tamanho))
  deseja = 0

  while criacaoPedidoReq.flag == 1: 
    print("\nCliente irá criar um pedido...")
    deseja = 1
    listaItensPedido = []
    
    # Recebe pedidos do cliente
    print('\nImprimindo pedido recebido: ')
    print('\n############################')
    while True: # Percorre itens do pedido até o pedido acabar
      pedidoClienteRes = PedidoClienteRes()
      pedidoClienteRes.unpack(conexao.recv(pedidoClienteRes.tamanho))

      itemPedido = {
        'item': pedidoClienteRes.item,
        'qtdPedida': pedidoClienteRes.quantidade
      }

      listaItensPedido.append(itemPedido) # Pedido do cliente
      
      #Imprimindo pedido do cliente
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
      print('\n----- Pedido rejeitado -----')

      disponibilidadeRes = DisponibilidadeRes()
      msg = disponibilidadeRes.pack('Pedido rejeitado - Não há disponibilidade de estoque', -1)
      conexao.send(msg)

      #Encerra conexão
      encerraConexao(conexao)

    # Informa cliente que pedido tem disponibilidade
    disponibilidadeRes = DisponibilidadeRes()
    msg = disponibilidadeRes.pack('Pedido aceito - Há disponibilidade de estoque', token)
    conexao.send(msg)
    print('\nPedido tem disponibilidade em estoque')
    print('Pedido efetuado com sucesso!')
    print("Número do seu pedido: ",pedido['numero_pedido'])

    #Salvando pedido realizado no arquivo de pedidos
    util.atualizaPedidos(pedido,idUsuario)

    #Enviando estoque atualizado para cliente
    for e in estoqueAtualizado:
      estoqueRes = EstoqueRes()
      flag = 0
      if e == estoqueAtualizado[-1]: #se for a última linha
        flag = 1
      conexao.send(estoqueRes.pack(e['item'], e['descricao'], e['quantidade'], e['valorUnitario'], flag))
    
    criacaoPedidoReq.unpack(conexao.recv(criacaoPedidoReq.tamanho))
  else:  #Não quer criar novo pedido
    
    if deseja == 1:
      print("\nCliente não quis criar mais pedidos")
    else:
      print("\nCliente não quis criar pedido")
    conexao.close()
    print('Conexão encerrada')
    _thread.exit()

# Configuração do socket tcp
tcp = socket(AF_INET, SOCK_STREAM)
tcp.bind((HOST, PORT))
tcp.listen(10)

# Lendo a base de usuários cadastrados e armazenando em memória;
usuarios_cadastrados = []
usuarios_cadastrados = util.getUsuarios()

# Imprimindo usuários cadastrados:
print('\n----------------------------------------------------------')
print("Usuários cadastrados no sistema: \n")
for uc in usuarios_cadastrados:
    print('Id:',uc['id'],'  Nome:',uc['nome'],'  Login:', uc['login'],'  Senha:',uc['senha'])
print('----------------------------------------------------------')

# Aguardando por conexões
while True:
  con, cliente = tcp.accept()  #aceita conexão
  _thread.start_new_thread(atendeCliente, (con, cliente))   #começa uma nova thread

