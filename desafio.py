import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

class Conta:
    _saldo = None
    _numero = None
    _agencia = None
    _cliente = None
    _historico = None
    
    def __init__():
        self._saldo = 0.0
        self._numero = 0
        self._agencia = "000000"
        self._cliente = Cliente
        self._historico = Historico
        
    
class ContaCorrente(Conta):
    __limite = None
    __limite_saques = None
    
    def __init__():
        self.__limite = 0.0
        self.__limite_saques = 1
        
class ContaPoupança(Conta):
    __limite_saques = None
    

class Transacao(ABC):
    def registrar_transacao(conta:Conta):
        return None

class Deposito(Transacao):
    __valor = None
    
class Saque(Transacao): 
    __valor = None
    
class Transferencia(Transacao):
    __valor = None
    
class Historico:
    def adicionar_transacao(transacao:Transacao):
        return None

class Cliente:
    _endereco = None
    _contas = None
    
    def __init__():
        self._endereco = "000000"
        self._contas = []


class PessoaFisica(Cliente):
    __cpf = None
    __nome = None
    __data_nascimento = None
    
class PessoaJuridica(Cliente):
    __cnpj = None
    __nome = None
    __data_criacao = None

class Main:
	
	def execute():
		menu = """\n
		================ MENU ================
		[d]\tDepositar
		[s]\tSacar
		[t]\tTransferir
		[e]\tExtrato
		[nc]\tNova conta
		[lc]\tListar contas
		[nu]\tNovo usuário
		[q]\tSair
		=> """
		
		while True:
		    opcao = input(textwrap.dedent(menu))
		    if opcao == "q":
		        print("Saindo do sistema.")
		        break
		    else:
		        print("Operacao invalida, por favor selecione a operação desejada.")
main = Main

main.execute()