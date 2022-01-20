"""
Disciplina de Redes de Computadores
Autor:  Matheus de Souza e Thaís de Souza
Matrícula: 20191bsi0301 e 20191bsi0263 
Trabalho: Loja de produtos esportivos - Trabalho 2
Semestre: 2021/2
Data de conclusão: 12/01/2022
"""


import random

def getUsuarios():
  usuarios = []
  
  arqUsuarios = open('../dados/clientes.csv')

  linhasUsuarios = arqUsuarios.readlines()[1:]

  for linha in linhasUsuarios:
    idu, nome, login, senha = linha.strip().split(';')
    
    usuario = {
      'id': int(idu),
      'nome': nome,
      'login': login,
      'senha': senha
    }

    usuarios.append(usuario)
  
  return usuarios

def removeNulls(a):
  b = a.replace('\x00', '')
  return b

def comparaStrings(a, b):
  a = a.replace('\x00', '')
  b = b.replace('\x00', '')

  return a == b

def getUsuario(login):
  usuarios = getUsuarios()
  for usuario in usuarios:
    if comparaStrings(usuario['login'], login):
      return usuario
  
  return None

def getPedidos():
  pedidos = []
  
  arqUsuarios = open('../dados/pedidos.csv')
  linhasPedidos = arqUsuarios.readlines()[1:]

  for linha in linhasPedidos:
    idPedido, idCliente, idItem, quantidade, valorUnitario = linha.strip().split(';')
    
    pedido = {
      'id': int(idPedido),
      'idCliente': int(idCliente),
      'idItem': idItem,
      'quantidade': int(quantidade),
      'valorUnitario': float(valorUnitario)
    }
    pedidos.append(pedido)
  
  return pedidos

def getPedidosUsuario(idCliente):
  pedidos = getPedidos()

  pedidosUsuario = []

  for pedido in pedidos:
    if pedido['idCliente'] == idCliente:
      pedidosUsuario.append(pedido)
  
  return pedidosUsuario

def getEstoque():

  listaEstoque = []

  arqEstoque = open('../dados/estoque.csv')
  linhasEstoque = arqEstoque.readlines()[1:]

  for linha in linhasEstoque:

    ide,item,descricao,quantidade,valor_unitario = linha.strip().split(';')

    estoque = {
      'id': int(ide),
      'item': item,
      'descricao': descricao,
      'quantidade': int(quantidade),
      'valorUnitario': float(valor_unitario)
    }
    listaEstoque.append(estoque)
  
  return listaEstoque

def criaPedidoConsumidor(estoque): #item, qtd e valorUnit
  copyEstoque = estoque[:]

  itensPedido = []
  
  r = 5
  i = 0

  while r > 0 and i < 5:
    itemSelected = copyEstoque.pop(random.randint(0, len(copyEstoque) - 1))

    a = 0
    if itemSelected['quantidade'] >= r:
      a = random.randint(1, r)
    elif itemSelected['quantidade'] > 0:
      a = random.randint(1, itemSelected['quantidade'])
    r -= a
    i += 1

    if a > 0:
      itemPedido = { 'item': itemSelected['item'], 'qtdPedida': a, 'valorUnitario' : itemSelected['valorUnitario'] }
      itensPedido.append(itemPedido)
    
  return itensPedido

def atualizaEstoque(estoque):
  fileEstoque = open('../dados/estoque.csv', 'w')

  fileEstoque.write('id;item;descricao;quantidade;valor_unitario\n')

  for itemEstoque in estoque:
    idEstoque = itemEstoque['id']
    item = itemEstoque['item']
    descricao = itemEstoque['descricao']
    qtdEstoque = itemEstoque['quantidade']
    vlUnitario = itemEstoque['valorUnitario']

    fileEstoque.write(f'{idEstoque};{item};{descricao};{qtdEstoque};{vlUnitario}\n')


def procuraItemEstoque(item, estoque):
  for itemEstoque in estoque:
    if itemEstoque['item'] == item:
      return itemEstoque


def atendePedidoCliente(pedidoCliente):  

  estoque = getEstoque()
  pedido = { 'numero_pedido': random.randint(1, 1000000), 'vlTotal': 0, 'itens': [] }

  for itemPedido in pedidoCliente:
    itemEstoque = procuraItemEstoque(itemPedido['item'], estoque)
    itemEstoque['quantidade'] -= itemPedido['qtdPedida']

    if itemEstoque['quantidade'] < 0:
      return None, getEstoque()
    
    pedido['itens'].append({
      'item': itemPedido['item'],
      'quantidade': itemPedido['qtdPedida'],
      'valorUnitario': itemEstoque['valorUnitario']
    })

    pedido['vlTotal'] += itemEstoque['valorUnitario'] * itemPedido['qtdPedida']

  # Salvar pedido

  atualizaEstoque(estoque)
  return pedido, getEstoque()

def atualizaPedidos(pedido, idCliente): #atualiza o arquivo de pedidos

  filePedidos = open('../dados/pedidos.csv', 'a')
  for itemPedido in pedido['itens']:
    
    idPedido = pedido['numero_pedido']
    idItem = itemPedido['item']
    quantidade = itemPedido['quantidade']
    valor_unitario = itemPedido['valorUnitario']

    filePedidos.write(f'{idPedido};{idCliente};{idItem};{quantidade};{valor_unitario}\n')
