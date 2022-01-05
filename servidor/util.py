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
