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
