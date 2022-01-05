from socket import *
import json
import struct

# Exemplo de cliente
cliente = {
  'id': 1,
  'nome': 'Matheus',
  'login': 'matheus',
  'senha': '1234'
}

# Dados da conexão
HOST = 'localhost'
PORT = 3333

login = input('Informe o login: ') # 20 String 
senha = input('Digite sua senha: ') # 10 String

tcp = socket(AF_INET, SOCK_STREAM)
tcp.connect((HOST, PORT))
codMensagem = 1
mensagemSerializada = struct.pack('!I20s10s', codMensagem, login.encode(), senha.encode())
print(mensagemSerializada)

tcp.send(mensagemSerializada)

input()