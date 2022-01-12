import struct
import uuid

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


class AutenticacaoRes(Mensagem):
	token = None
	mensagem = None

	def __init__(self):
		super().__init__(2, 58, '!I50si')
	
	def pack(self, mensagem, token):
		self.mensagem = mensagem
		self.token = token
		
		return struct.pack(self.formato, self.codMensagem, self.mensagem.encode(), token)
	
	def unpack(self, msg):
		codMensagem, mensagem, token = struct.unpack(self.formato, msg)

		self.mensagem = mensagem.decode()
		self.token = token

class ListaPedidosReq(Mensagem):
	token = None

	def __init__(self):
		super().__init__(3, 8, '!II')
	
	def pack(self, token):
		self.token = token
		
		return struct.pack(self.formato, self.codMensagem, token)
	
	def unpack(self, msg):
		codMensagem, token = struct.unpack(self.formato, msg)

		self.token = token

class PedidoRes(Mensagem):
	idPedido = None
	item = None
	quantidade = None
	valorUnitario = None
	flag = None

	def __init__(self):
		super().__init__(4, 40, '!II20sIfI')
	
	def pack(self, idPedido, item, quantidade, valorUnitario, flag):
		self.idPedido = idPedido
		self.item = item
		self.quantidade = quantidade
		self.valorUnitario = valorUnitario
		self.flag = flag
		
		return struct.pack(self.formato, self.codMensagem, self.idPedido, self.item.encode(), self.quantidade, self.valorUnitario, self.flag)
	
	def unpack(self, msg):
		codMensagem, idPedido, item, quantidade, valorUnitario, flag = struct.unpack(self.formato, msg)

		self.idPedido = idPedido
		self.item = item.decode()
		self.quantidade = quantidade
		self.valorUnitario = valorUnitario
		self.flag = flag

class EstoqueReq(Mensagem):

	token = None

	def __init__(self):
		super().__init__(5, 8, '!II')
	
	def pack(self, token):
		self.token = token
		
		return struct.pack(self.formato, self.codMensagem, token)
	
	def unpack(self, msg):
		codMensagem, token = struct.unpack(self.formato, msg)

		self.token = token

class EstoqueRes(Mensagem):
	
	item = None
	descricao = None
	quantidade = None
	valorUnitario = None

	def __init__(self):
		super().__init__(6, 86, '!I20s50sIfI') 
	
	def pack(self, item, descricao, quantidade, valorUnitario, flag):
		
		self.item = item
		self.descricao = descricao
		self.quantidade = quantidade
		self.valorUnitario = valorUnitario
		self.flag = flag
		
		return struct.pack(self.formato, self.codMensagem, self.item.encode(), self.descricao.encode(), self.quantidade, self.valorUnitario, self.flag)
	
	def unpack(self, msg):
		codMensagem, item, descricao, quantidade, valorUnitario, flag = struct.unpack(self.formato, msg)

		self.item = item.decode()
		self.descricao = descricao.decode()
		self.quantidade = quantidade
		self.valorUnitario = valorUnitario
		self.flag = flag
