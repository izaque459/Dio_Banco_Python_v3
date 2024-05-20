import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

class Conta:
    _saldo = None
    _numero = None
    _agencia = None
    _cliente = None
    _historico = None

    def __init__(self,cliente,numero):
        self._saldo = 0.0
        self._numero = 0
        self._agencia = numero
        self._cliente = cliente
        self._historico = Historico()
        
    @classmethod
    def nova_conta(cls,cliente,conta):
        return cls(numero,cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
  
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._hitorico
    
    def sacar(self,valor):
        saldo = self.saldo
        excedeu_saldo = valor >saldo
        
        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
        elif valor>0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso ===")
            return True
        else:
            print("\n O valor informado é invalido. @@@")
            return False
            
    def depositar(self,valor):
    
        if valor>0:
            self._saldo += valor
            print("\n=== Operação realizada com sucesso! ===")
        else:
            print("\n@@@ Operacao falhou! O valor ínformado é invalido. @@@")
            return False
        return True

    

class ContaCorrente(Conta):
    __limite = None
    __limite_saques = None

    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self._agencia}
            C/C:\t\t{self._numero}
            Titular:\t{self._cliente.nome}
        """
        
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
        
    @property
    def nome(self):
        return self.__nome
        
    def adicionar(self,conta):
        self._contas.append(conta)
        return None

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
        
        
    def __listar_contas(self):
        for conta in self.__contas:
            print("=" * 100)
            print(textwrap.dedent(str(conta)))

    def __filtrar_cliente(self,cpf):
        clientes_filtrados = [cliente for cliente in self.__clientes if cliente.cpf == cpf]
        return clientes_filtrados[0] if clientes_filtrados else None
    

    def __criar_contas(self,numero):
        cpf = input("Informe o CPF do cliente: ")
        cliente = self.__filtrar_cliente(cpf)
        
        if not cliente:
            print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
            return None
        
        conta = ContaCorrente(cliente,numero)
        self.__contas.append(conta)
        cliente.adicionar(conta)
        
        print("\n=== Conta criada cm sucesso! ===")
        
        
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
            
            if opcao == "nc":
                numero_conta = len(self.__contas)+1
                self.__criar_contas(numero_conta)
                
            elif opcao == "lc":
                self.__listar_contas()
                
            elif opcao == "nu":
                self.__criar_cliente()
                
            elif opcao == "q":
                print("Saindo do sistema.")
                break
                
            else:
                print("Operação inválida, por favor selecione a operação desejada.")

main = Main()

main.execute()
