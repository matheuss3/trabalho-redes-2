import struct

class Mensagem:
	def __init__(self, codMensagem, tamanho, formato):
		self.codMensagem = codMensagem
		self.tamanho = tamanho
		self.formato = formato

class AutenticacaoReq(Mensagem):
	login = None
	senha = None

	def __init__(self):
		super().__init__(1, 34, '!I20s10s')
	
	def pack(self, login, senha):
		self.login = login
		self.senha = senha

		return struct.pack(self.formato, self.codMensagem, login.encode(), senha.encode())
	
	def unpack(self, msg):
		codMensagem, login, senha = struct.unpack(self.formato, msg)

		self.login = login.decode()
		self.senha = senha.decode()




		
		


	


	

	

