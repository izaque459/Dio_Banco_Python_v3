import textwrap

class Main:
	
	def execute():
		menu = """\n
		================ MENU ================
		[d]\tDepositar
		[s]\tSacar
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