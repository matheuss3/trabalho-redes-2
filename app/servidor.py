"""
Disciplina de Redes de Computadores
Autor:  Matheus de Souza e Thaís de Souza
Matrícula: 20191bsi0301 e 20191bsi0263 
Trabalho: Loja de produtos esportivos - Trabalho 2
Semestre: 2021/2
Data de conclusão: 12/01/2022
"""

from socket import *
import _thread

import random

from mensagens import *
import util

# Dados da conexão
HOST = 'localhost'
PORT = 3333
MAX_BUFFER_SIZE = 1024
CODING = 'UTF-8'

def encerraConexao(conexao):
  conexao.close()
  print('Conexão encerrada')
  _thread.exit()

def autenticaClientes(login, senha):
  usuario = util.getUsuario(login)

  if usuario and util.comparaStrings(usuario['senha'], senha):
    print('\n---- Gerando token para o cliente ',usuario['nome'],' ----')
    return random.randint(0, 999999), usuario['id']
  
  return None, None

def recvMsg(conexao, cliente, dadosSessao):
  buffer = conexao.recv(MAX_BUFFER_SIZE)
  msg = None

  while True:
    codMsg = buffer[:4]
    codMsg, = struct.unpack('!I', codMsg)

    print('Codigo da mensagem: ' + str(codMsg))

    if codMsg == 1:  # Cliente querendo se autenticar
      autenticacaoReq = AutenticacaoReq()
      msg = buffer[:autenticacaoReq.tamanho]
      buffer = buffer[autenticacaoReq.tamanho:]
      autenticacaoReq.unpack(msg)

      tokenCliente, idCliente = autenticaClientes(autenticacaoReq.login, autenticacaoReq.senha)
      dadosSessao["token"] = tokenCliente
      dadosSessao["id"] = idCliente

      autenticacaoRes = AutenticacaoRes()
      if not tokenCliente:
        msgRes = autenticacaoRes.pack('Acesso negado', -1)
        conexao.send(msgRes)

        # Encerrando conexão com usuário
        encerraConexao(conexao)
      
      msgRes = autenticacaoRes.pack('Login efetuado com sucesso!', tokenCliente)
      conexao.send(msgRes)
    
    if codMsg == 3: # Cliente solicitando sua lista de pedidos
      print("\nRecebendo solicitação da lista de pedidos do usuário...")

      solListaPedidos = ListaPedidosReq()
      msg = buffer[:solListaPedidos.tamanho]
      buffer = buffer[solListaPedidos.tamanho:]
      solListaPedidos.unpack(msg)
      
      # Não possui permissão para acessar lista de pedidos
      if solListaPedidos.token != dadosSessao["token"]: 
        encerraConexao(conexao)
      
      # Passou pela verificação do token
      print("Solicitação atendida com sucesso!")

      # Acessando lista de pedidos cadastrados
      pedidos = util.getPedidosUsuario(dadosSessao["id"])

      # Enviando quantidade de pedidos que o cliente tem
      possuiPedidos = PossuiPedidos()
      msg = possuiPedidos.pack(len(pedidos))
      conexao.send(msg)

      # Enviando lista de pedidos para usuário
      print("Enviando lista de pedidos do usuário...")
      for pedido in pedidos:
        pedidoRes = PedidoRes()

        # Verifica se o item é o ultimo
        flag = 0
        if pedido == pedidos[-1]:
          flag = 1
        
        # Envio do item do pedido ao cliente
        conexao.send(pedidoRes.pack(pedido['id'], pedido['idItem'], 
          pedido['quantidade'], pedido['valorUnitario'], flag))
      
      print("Lista de pedidos enviada com sucesso!")
      
    if codMsg == 6: # Cliente querendo vizualizar o estoque
      print("\nRecebendo solicitação de envio de estoque...")
      
      solListaEstoque = EstoqueReq()
      msg = buffer[:solListaEstoque.tamanho]
      buffer = buffer[solListaEstoque.tamanho:]
      solListaEstoque.unpack(msg)

      # Não possui permissão para acessar lista de pedidos
      if solListaEstoque.token != dadosSessao["token"]: 
        encerraConexao(conexao)

      # Pegando estoque 
      print("Solicitação atendida com sucesso!")
      estoque = util.getEstoque()

      # Enviando lista de estoque para usuário
      print("Enviando estoque...")
      for e in estoque:
        estoqueRes = EstoqueRes()

        # Verifica se o item é o ultimo
        flag = 0
        if e == estoque[-1]: #se for a última linha
          flag = 1
        
        conexao.send(estoqueRes.pack(e['item'], e['descricao'], 
          e['quantidade'], e['valorUnitario'], flag))
      
      print("Estoque enviado com sucesso!")

    if codMsg == 8:
      print("\nCliente irá criar um pedido...")

      # Recebendo se o cliente deseja realizar um pedido
      criacaoPedidoReq = CriacaoPedidoReq()
      msg = buffer[:criacaoPedidoReq.tamanho]
      buffer = buffer[criacaoPedidoReq.tamanho:]

      # Lista dos itens passados pelo cliente
      listaItensPedido = []
      
      # Recebe pedidos do cliente
      print('\nImprimindo pedido recebido: ')
      print('\n############################')
      try:
        while True: # Percorre itens do pedido até o pedido acabar
          pedidoClienteRes = PedidoClienteRes()

          if len(buffer) == 0:
            msg = conexao.recv(pedidoClienteRes.tamanho)
          else:
            msg = buffer[:pedidoClienteRes.tamanho]
            buffer = buffer[pedidoClienteRes.tamanho:]
          
          pedidoClienteRes.unpack(msg)
          
          itemPedido = {
            'item': pedidoClienteRes.item,
            'qtdPedida': pedidoClienteRes.quantidade
          }

          listaItensPedido.append(itemPedido) # Pedido do cliente
          
          # Imprimindo pedido do cliente
          print(f'Item: {pedidoClienteRes.item}')
          print(f'Quantidade: {pedidoClienteRes.quantidade}')
          print(f'Valor Unitario: {pedidoClienteRes.valorUnitario}')
          print(f'Flag: {pedidoClienteRes.flag}')
          print('############################')

          # Ultimo item?
          if pedidoClienteRes.flag == 1:
            break
        
        #Verifica disponibilidade do pedido recebido
        pedido = util.atendePedidoCliente(listaItensPedido)
        disponibilidadeRes = DisponibilidadeRes()

        #Informa cliente que pedido não tem disponibilidade
        if not pedido: # Não tem disponibilidade de estoque
          print('\n----- Pedido rejeitado -----')

          msgRes = disponibilidadeRes.pack('Pedido rejeitado - Não há disponibilidade de estoque', -1)
          conexao.send(msgRes)

          # Encerra conexão
          encerraConexao(conexao)
        
        # Informa cliente que pedido tem disponibilidade
        msgRes = disponibilidadeRes.pack('Pedido aceito - Há disponibilidade de estoque', dadosSessao["token"])
        conexao.send(msgRes)

        print('\nPedido tem disponibilidade em estoque')
        print('Pedido efetuado com sucesso!')
        print("Número do seu pedido: ", pedido['numero_pedido'])

        # Salvando pedido realizado no arquivo de pedidos
        util.atualizaPedidos(pedido, dadosSessao["id"])
      except:
          print('-----------O cliente encerrou a conexão-----------')
          break
        
    if codMsg == 11: # Mensagem para encerrar conexão
      encerraConReq = EncerrarConexaoReq()
      msg = buffer[:encerraConReq.tamanho]
      buffer = buffer[encerraConReq.tamanho:]

      print("\nCliente deseja encerrar a conexão")
      encerraConexao(conexao)

    if len(buffer) == 0:
      print('Todo buffer foi lido!')
      break

  return msg

def conectado(con, cliente):
  print("Conectado ao cliente: ", cliente)
  dadosSessao = { "token": None, "id": None}
  while True:
    msg = recvMsg(con, cliente, dadosSessao)
    if not msg:
      break
  print("Cliente desconectado: ", cliente)
  _thread.exit()

def main():
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
    _thread.start_new_thread(conectado, (con, cliente))   #começa uma nova thread

if __name__ == '__main__':
  main()