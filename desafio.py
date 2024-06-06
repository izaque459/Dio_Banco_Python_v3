import textwrap
from abc import ABC, abstractclassmethod, abstractproperty,abstractmethod
from datetime import datetime


class Conta:
    _saldo = None
    _numero = None
    _agencia = None
    _cliente = None
    _historico = None

    def __init__(self, cliente, numero):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, conta):
        return cls(numero, cliente)

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
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso ===")
            return True
        else:
            print("\n O valor informado é invalido. @@@")
            return False

    def depositar(self, valor):

        if valor > 0:
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
            [
                transacao
                for transacao in self.historico.transacoes
                if transacao["tipo"] == Saque.__name__
            ]
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
    __RENDIMENTO = None
    
    def __init__(self, cliente, numero):
        super().__init__(cliente, numero)
        self.__RENDIMENTO = 0.1

    def __str__(self):
        return f"""\
            Agência:\t{self._agencia}
            Conta Poupança:\t{self._numero}
            Titular:\t{self._cliente.nome}
        """
        
    def __aplicar_rendimento(self):
        self._saldo += self._saldo*self.__RENDIMENTO
        
    def depositar(self,valor):
        if valor > 0:
            self._saldo += valor
            self.__aplicar_rendimento()
            print("\n=== Operação realizada com sucesso! ===")
        else:
            print("\n@@@ Operacao falhou! O valor ínformado é invalido. @@@")
            return False
        return True
        

class Transacao(ABC):

    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registra(self, conta):
        pass


class Deposito(Transacao):
    __valor = None
    
    def __init__(self, valor):
        self.__valor = valor

    @property
    def valor(self):
        return self.__valor

    def registra(self, conta):
        sucesso_transacao = conta.depositar(self.__valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
        

class Saque(Transacao):
    __valor = None

    def __init__(self, valor):
        self.__valor = valor

    @property
    def valor(self):
        return self.__valor

    def registra(self, conta):
        sucesso_transacao = conta.sacar(self.__valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
        

class Transferencia(Transacao):
    __valor = None
    __conta_destino = None
    
    def __init__(self, valor, conta_destino):
        self.__valor = valor
        self._conta_destino = conta_destino

    @property
    def valor(self):
        return self.__valor

    def registra(self, conta):
        if conta.sacar(self.valor):
            self.__conta_destino.depositar(self.valor)
            conta.historico.adicionar_transacao(self)
            self.__conta_destino.historico.adicionar_transacao(self)

class Historico:
    __transacoes = None
  
    def __init__(self):
        self.__transacoes = []

    @property
    def transacoes(self):
        return self.__transacoes

    def adicionar_transacao(self, transacao):
        self.__transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

class Cliente:
    _endereco = None
    _contas = None

    def __init__(self, endereco):
        self._endereco = "000000"
        self._contas = []
        
    def adicionar(self, conta):
        self._contas.append(conta)

    def realizar_transacao(self, conta, transacao):
        transacao.registra(conta)
    
    def recuperar_contas(self):
        return self._contas


class PessoaFisica(Cliente):
    __cpf = None
    __nome = None
    __data_nascimento = None

    def __init__(self, nome, cpf, data_nascimento, endereco):
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



class PessoaJuridica(Cliente):
    __cnpj = None
    __nome = None
    __data_criacao = None
    
    def __init__(self, nome, cnpj, data_criacao, endereco):
        super().__init__(endereco)
        self.__nome = nome
        self.__cnpj = cnpj
        self.__data_criacao = data_criacao

    @property
    def cnpj(self):
        return self.__cnpj

    @property
    def nome(self):
        return self.__nome

class Main:
    __clientes = None
    __contas = None

    def __init__(self):
        self.__clientes = []
        self.__contas = []

    def __listar_contas(self):
        if self.__contas:
            for conta in self.__contas:
                print("=" * 100)
                print(textwrap.dedent(str(conta)))
        else:
            print("Não há contas criadas\n")

    def __filtrar_cpf_cliente(self, cpf):
        clientes_filtrados = [
            cliente for cliente in self.__clientes if isinstance(cliente, PessoaFisica) and cliente.cpf == cpf
        ]
        return clientes_filtrados[0] if clientes_filtrados else None


    def __filtrar_cnpj_cliente(self, cnpj):
        clientes_filtrados = [
            cliente for cliente in self.__clientes if isinstance(cliente, PessoaJuridica) and cliente.cnpj == cnpj
        ]
        return clientes_filtrados[0] if clientes_filtrados else None
        
    def __escolha_CPF_CNPJ(self):
        menu_escolha_CPF_CNPJ = """Para o CPF escolha 1 para CNPJ escolha 2: """
        opcao_escolha = input(textwrap.dedent(menu_escolha_CPF_CNPJ))
        
        while (opcao_escolha!= '1') and (opcao_escolha != '2'):
            print("Digite a opcao correta\n")
            opcao_escolha = input(textwrap.dedent(menu_escolha_CPF_CNPJ))
            
        if opcao_escolha == '1':
            cpf = input("Informe o CPF: ")
            cliente = self.__filtrar_cpf_cliente(cpf)
        else:
            cnpj= input("Informe o CNPJ: ")
            cliente = self.__filtrar_cnpj_cliente(cnpj)
            
        return cliente
    
    def __sacar(self):
        
        cliente = self.__escolha_CPF_CNPJ()

        if not cliente:
            print(
                "\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@"
            )
            return None

        contas = cliente.recuperar_contas()

        if not contas:
            print("\n@@@ O cliente não possui contas! @@@")
            return None

        escolhas = 0
        escolha = -1
        for conta in contas:
            print(f"\nPara conta\n{conta}\nEscolha {escolhas}")
            escolhas += 1

        while (int(escolha) < 0) or (int(escolha) > len(contas)):
            escolha = input("\nEscolha a conta: ")
      
        
        conta = contas[int(escolha)]

        valor = float(input("\nInforme o valor do saque: "))
        transacao = Saque(valor)
        cliente.realizar_transacao(conta, transacao)

    def __depositar(self):
        
        cliente = self.__escolha_CPF_CNPJ()

        if not cliente:
            print(
                "\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@"
            )
            return None

        contas = cliente.recuperar_contas()

        if not contas:
            print("\n@@@ O cliente não possui contas! @@@")
            return None

        escolhas = 0
        escolha = -1
        for conta in contas:
            print(f"\nPara conta\n{conta}\nEscolha {escolhas}")
            escolhas += 1

        while (int(escolha) < 0) or (int(escolha) > len(contas)):
            escolha = input("\nEscolha a conta: ")
      
        
        conta = contas[int(escolha)]

        valor = float(input("\nInforme o valor do depósito: "))
        transacao = Deposito(valor)
        cliente.realizar_transacao(conta, transacao)

        
    def __criar_conta_poupanca(self,numero):
    
        cliente = self.__escolha_CPF_CNPJ()
        
        if not cliente:
            print(
                "\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@"
            )
            return None
            
        conta = ContaPoupança(cliente, numero)
        
        self.__contas.append(conta)
        cliente.adicionar(conta)
       
        print("\n=== Conta poupança criada cm sucesso! ===")
        
    def __criar_conta_corrente(self,numero):
    
        cliente = self.__escolha_CPF_CNPJ()
            
        if not cliente:
            print(
                "\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@"
            )
            return None
        conta = ContaCorrente(cliente, numero)
        
        self.__contas.append(conta)
        cliente.adicionar(conta)
       
        print("\n=== Conta corrente criada cm sucesso! ===")

    def __criar_cliente(self):
        menu_criar_cliente = """Escolha o cliente a seguir: \n[f]\tCliente Fisico\n[j]\tCliente Juridico\n=> """
        opcao_criar_cliente = input(textwrap.dedent(menu_criar_cliente))
        if opcao_criar_cliente == "f":
            print("Criar cliente fisico")
            cpf = input("Informe o CPF (somente número): ")
            cliente = self.__filtrar_cpf_cliente(cpf)

            if cliente:
                print("\n@@@ Já existe usuário com esse CPF! @@@")
                return

            nome = input("Informe o nome completo: ")
            data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
            endereco = input(
                "Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): "
            )

            cliente = PessoaFisica(nome, cpf, data_nascimento, endereco)

            self.__clientes.append(cliente)

            print("=== Cliente criado com sucesso! ===")

        elif opcao_criar_cliente == "j":
            print("Criar cliente juridico")
            cnpj = input("Informe o CNPJ (somente número): ")
            cliente = self.__filtrar_cnpj_cliente(cnpj)

            if cliente:
                print("\n@@@ Já existe usuário com esse CNPJ! @@@")
                return

            nome = input("Informe o nome completo: ")
            data_criacao = input("Informe a data de nascimento (dd-mm-aaaa): ")
            endereco = input(
                "Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): "
            )

            cliente = PessoaJuridica(nome, cnpj, data_criacao, endereco)

            self.__clientes.append(cliente)

            print("=== Cliente criado com sucesso! ===")
        else:
            print("Escolha invalida para cliente")

    def execute(self):
        menu = """\n
        ================ MENU ================
        [d]\tDepositar
        [s]\tSacar
        [t]\tTransferir
        [e]\tExtrato
        [cc]\tConta Corrente
        [cp]\tConta Poupança
        [lc]\tListar contas
        [nu]\tNovo usuário
        [q]\tSair
        => """

        while True:
            opcao = input(textwrap.dedent(menu))
            
            if opcao == "s":
                self.__sacar()
            elif opcao == "d":
                self.__depositar()
            elif opcao == "cp":
                numero_conta = len(self.__contas) + 1
                self.__criar_conta_poupanca(numero_conta)
                
            elif opcao == "cc":
                numero_conta = len(self.__contas) + 1
                self.__criar_conta_corrente(numero_conta)
                
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
