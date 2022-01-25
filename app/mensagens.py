"""
Disciplina de Redes de Computadores
Autor:  Matheus de Souza e Thaís de Souza
Matrícula: 20191bsi0301 e 20191bsi0263 
Trabalho: Loja de produtos esportivos - Trabalho 2
Semestre: 2021/2
Data de conclusão: 12/01/2022
"""

from os import remove
import struct
from util import removeNulls

#Definindo a classe Mensagem  (com os atributos fixos de todas as mensagens)
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

		self.login = removeNulls(login.decode())
		self.senha = removeNulls(senha.decode())


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

		self.mensagem = removeNulls(mensagem.decode())
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

class PossuiPedidos(Mensagem):
	qtdPedidos = None

	def __init__(self):
		super().__init__(4, 8, '!II')
	
	def pack(self, qtdPedidos):
		self.qtdPedidos = qtdPedidos
		
		return struct.pack(self.formato, self.codMensagem, self.qtdPedidos)
	
	def unpack(self, msg):
		codMensagem, qtdPedidos = struct.unpack(self.formato, msg)

		self.qtdPedidos = qtdPedidos


class PedidoRes(Mensagem):
	idPedido = None
	item = None
	quantidade = None
	valorUnitario = None
	flag = None

	def __init__(self):
		super().__init__(5, 40, '!II20sIfI')
	
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
		self.item = removeNulls(item.decode())
		self.quantidade = quantidade
		self.valorUnitario = valorUnitario
		self.flag = flag

class EstoqueReq(Mensagem):

	token = None

	def __init__(self):
		super().__init__(6, 8, '!II')
	
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
		super().__init__(7, 86, '!I20s50sIfI') 
	
	def pack(self, item, descricao, quantidade, valorUnitario, flag):
		
		self.item = item
		self.descricao = descricao
		self.quantidade = quantidade
		self.valorUnitario = valorUnitario
		self.flag = flag
		
		return struct.pack(self.formato, self.codMensagem, self.item.encode(), self.descricao.encode(), self.quantidade, self.valorUnitario, self.flag)
	
	def unpack(self, msg):
		codMensagem, item, descricao, quantidade, valorUnitario, flag = struct.unpack(self.formato, msg)

		self.item = removeNulls(item.decode())
		self.descricao = removeNulls(descricao.decode())
		self.quantidade = quantidade
		self.valorUnitario = valorUnitario
		self.flag = flag

class CriacaoPedidoReq(Mensagem):
	token = None

	def __init__(self):
		super().__init__(8, 8, '!II')
	
	def pack(self, token):
		self.token = token

		return struct.pack(self.formato, self.codMensagem, self.token)
	
	def unpack(self, msg):
		codMensagem, token = struct.unpack(self.formato, msg)
		
		self.token = token

class PedidoClienteRes(Mensagem):
	item = None
	quantidade = None
	valorUnitario = None
	flag = None

	def __init__(self):
		super().__init__(9, 36, '!I20sIfI')
	
	def pack(self, item, quantidade, valorUnitario, flag):
		self.item = item
		self.quantidade = quantidade
		self.valorUnitario = valorUnitario
		self.flag = flag
		
		return struct.pack(self.formato, self.codMensagem, self.item.encode(), self.quantidade, self.valorUnitario, self.flag)
	
	def unpack(self, msg):
		codMensagem, item, quantidade, valorUnitario, flag = struct.unpack(self.formato, msg)

		self.item = removeNulls(item.decode())
		self.quantidade = quantidade
		self.valorUnitario = valorUnitario
		self.flag = flag

class DisponibilidadeRes(Mensagem):

	token = None
	mensagem = None

	def __init__(self):
		super().__init__(10, 78, '!I70si')
	
	def pack(self, mensagem, token):
		self.mensagem = mensagem
		self.token = token
		
		return struct.pack(self.formato, self.codMensagem, self.mensagem.encode(), token)
	
	def unpack(self, msg):
		codMensagem, mensagem, token = struct.unpack(self.formato, msg)

		self.mensagem = removeNulls(mensagem.decode())
		self.token = token

class EncerrarConexaoReq(Mensagem):
	def __init__(self):
		super().__init__(11, 4, '!I')
	
	def pack(self):
		return struct.pack(self.formato, self.codMensagem)
	
	def unpack(self, msg):
		codMensagem, = struct.unpack(self.formato, msg)
