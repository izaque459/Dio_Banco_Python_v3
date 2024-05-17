import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

class Conta:
    _saldo = None
    _numero = None
    _agencia = None
    _cliente = None
    _historico = None

    def __init__(self):
        self._saldo = 0.0
        self._numero = 0
        self._agencia = "000000"
        self._cliente = Cliente
        self._historico = Historico

class ContaCorrente(Conta):
    __limite = None
    __limite_saques = None

    def __init__(self):
        self.__limite = 0.0
        self.__limite_saques = 1

class ContaPoupança(Conta):
    __limite_saques = None
    __rendimento = None

class Transacao(ABC):
    def registrar_transacao(self, conta: Conta):
        return None

class Deposito(Transacao):
    __valor = None

class Saque(Transacao):
    __valor = None

class Transferencia(Transacao):
    __valor = None

class Historico:
    def adicionar_transacao(self, transacao: Transacao):
        return None

class Cliente:
    _endereco = None
    _contas = None

    def __init__(self,endereco):
        self._endereco = "000000"
        self._contas = []

class PessoaFisica(Cliente):
    __cpf = None
    __nome = None
    __data_nascimento = None
    
    def __init__(self,nome,cpf,data_nascimento,endereco):
        super().__init__(endereco)
        self.__cpf = cpf
        self.__nome = nome
        self.__nascimento = data_nascimento
        
    @property
    def cpf(self):
        return self.__cpf

class PessoaJuridica(Cliente):
    __cnpj = None
    __nome = None
    __data_criacao = None

class Main:
    __clientes = None
    __contas = None

    def __init__(self):
        self.__clientes = []
        self.__contas = []

    def __filtrar_cliente(self,cpf):
        clientes_filtrados = [cliente for cliente in self.__clientes if cliente.cpf == cpf]
        return clientes_filtrados[0] if clientes_filtrados else None
        
    def __criar_cliente(self):
        menu_criar_cliente = """Escolha o cliente a seguir: \n[f]\tCliente Fisico\n[j]\tCliente Juridico\n"""
        opcao_criar_cliente = input(textwrap.dedent(menu_criar_cliente))
        if opcao_criar_cliente == "f":
            print("Criar cliente fisico")
            cpf = input("Informe o CPF (somente número): ")
            cliente = self.__filtrar_cliente(cpf)
            
            if cliente:
                print("\n@@@ Já existe usuário com esse CPF! @@@")
                return
            
            nome = input("Informe o nome completo: ")
            data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
            endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
           
            cliente = PessoaFisica(nome,cpf,data_nascimento,endereco)
            
            self.__clientes.append(cliente)
            
            print("=== Cliente criado com sucesso! ===")
            
        elif opcao_criar_cliente == "j":
            print("Criar cliente juridico")
        else:
            print("Escolha invalida para cliente")

    def execute(self):
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
            if opcao == "nu":
                self.__criar_cliente()
            elif opcao == "q":
                print("Saindo do sistema.")
                break
            else:
                print("Operação inválida, por favor selecione a operação desejada.")

main = Main()

main.execute()
