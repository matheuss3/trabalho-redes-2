from socket import *
import util
import _thread
import struct

# Dados da conexão
HOST = 'localhost'
PORT = 3333
BYTES_BY_MSG = 1024
CODING = 'UTF-8'

def atendeCliente(conexao, cliente):
  codMensagem, login, senha = struct.unpack('!I20s10s', conexao.recv(34))

  print(codMensagem)
  print('Login:', login.decode())
  print('Senha:', senha.decode())

usuarios = util.getUsuarios()

tcp = socket(AF_INET, SOCK_STREAM)
tcp.bind((HOST, PORT))
tcp.listen(10)

while True:
  con, cliente = tcp.accept()
  _thread.start_new_thread(atendeCliente, (con, cliente))

