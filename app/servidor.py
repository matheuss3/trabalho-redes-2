from socket import *
from mensagens import AutenticacaoReq
import util
import _thread
import struct

# Dados da conexão
HOST = 'localhost'
PORT = 3333
BYTES_BY_MSG = 1024
CODING = 'UTF-8'

# def autenticaClientes(login, senha):
#   usuario = util.getUsuario(login)

#   if usuario:
#     if usuario['senha'] == senha:


def atendeCliente(conexao, cliente):
  mensagemAutenticacao = AutenticacaoReq()
  mensagemAutenticacao.unpack(conexao.recv(34))

  # token = autenticaClientes(login.decode(), senha.decode())

  

  print('Login:', mensagemAutenticacao.login)
  print('Senha:', mensagemAutenticacao.senha)



tcp = socket(AF_INET, SOCK_STREAM)
tcp.bind((HOST, PORT))
tcp.listen(10)

while True:
  con, cliente = tcp.accept()
  _thread.start_new_thread(atendeCliente, (con, cliente))

