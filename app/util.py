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

def comparaStrings(a, b):
  a = a.replace('\x00', '')
  b = b.replace('\x00', '')

  return a == b

def getUsuario(login):
  usuarios = getUsuarios()
  for usuario in usuarios:
    if comparaStrings(usuario['login'], login):
      print(usuario)
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
  itensPedido = []

  for i in range(5):
    itemSelected = random.choice(estoque)

    itemExists = False
    for itemPedido in itensPedido:
      if itemPedido['item'] == itemSelected['item']:
        itemPedido['qtdPedida'] += 1
        itemExists = True
        break
    
    if not itemExists:
      itemPedido = { 'item': itemSelected['item'], 'qtdPedida': 1, 'valorUnitario' : itemSelected['valorUnitario'] }
      itensPedido.append(itemPedido)
    
  return itensPedido