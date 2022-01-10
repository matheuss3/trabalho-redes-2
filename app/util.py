def getUsuarios():
  usuarios = []
  
  arqUsuarios = open('../dados/clientes.csv')

  linhasUsuarios = arqUsuarios.readlines()[1:]

  for linha in linhasUsuarios:
    idu, nome, login, senha = linha.strip().split(';')
    
    usuario = {
      'id': idu,
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
