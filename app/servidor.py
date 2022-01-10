from socket import *
from mensagens import AutenticacaoReq, AutenticacaoRes
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
  
  return None


def atendeCliente(conexao, cliente):
  autenticacaoReq = AutenticacaoReq()
  autenticacaoReq.unpack(conexao.recv(autenticacaoReq.tamanho))

  token, idUsuario = autenticaClientes(autenticacaoReq.login, autenticacaoReq.senha)
  
  if not token:
    conexao.close()
    print('Conexão encerrada')
    _thread.exit()

  print(f'Token gerado para o usuário - {token}')
  autenticacaoRes = AutenticacaoRes()
  conexao.send(autenticacaoRes.pack(token))

# Configuração do socket tcp
tcp = socket(AF_INET, SOCK_STREAM)
tcp.bind((HOST, PORT))
tcp.listen(10)

while True:
  con, cliente = tcp.accept()
  _thread.start_new_thread(atendeCliente, (con, cliente))
