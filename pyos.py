import os
import curses
import pycfg
import time
from pyarch import load_binary_into_memory
from pyarch import cpu_t

class os_t:
	def __init__ (self, cpu, memory, terminal):
		self.cpu = cpu
		self.memory = memory
		self.terminal = terminal

		self.terminal.enable_curses()

		self.console_str = ""
		self.terminal.console_print("ESTE EH O CONSOLE, DIGITE OS COMANDO AQUI!\n")

	def printk(self, msg):
		self.terminal.kernel_print("kernel: " + msg + "\n")

	def panic (self, msg):
		self.terminal.end()
		self.terminal.dprint("kernel panic: " + msg)
		self.cpu.cpu_alive = False
		#cpu.cpu_alive = False

	#Interrupcao do teclado
	def interrupt_keyboard (self):
		key = self.terminal.get_key_buffer()

		#printa no terminal o que eh digitado
		if ((key >= ord('a')) and (key <= ord('z'))) or ((key >= ord('A')) and (key <= ord('Z'))) or ((key >= ord('0')) and (key <= ord('9'))) or (key == ord(' ')) or (key == ord('-')) or (key == ord('_')) or (key == ord('.')):
		
			self.console_str = self.console_str + chr(key)
			self.terminal.console_print("\r" + self.console_str)
		
		#exclui do terminal as letras
		elif (key == curses.KEY_BACKSPACE):
			self.console_str = self.console_str[:-1]
			self.terminal.console_print("\r" + self.console_str)

		#ler o enter do teclado para se executar alguma acao	
		elif (key == curses.KEY_ENTER) or (key == ord('\n')):
			self.tratar_instrucao()
			self.console_str = "" 
			self.terminal.console_print("\r")
	
	#trata as interupcoes do teclado
	def handle_interrupt (self, interrupt):
		if (interrupt == pycfg.INTERRUPT_KEYBOARD): #constante 
			self.interrupt_keyboard() 
			# self.printk(str(interrupt) + ":(Teclado) Interupcao")
		# elif(interrupt == pycfg.INTERRUPT_MEMORY_PROTECTION_FAULT):
		# 	self.printk(str(interrupt) + ":(Falta de Memoria) Interupcao nao implementado")
		# elif(interrupt == pycfg.INTERRUPT_TIMER):
		# 	self.printk(str(interrupt + ":(Tempo) Interupcao nao implementado"))
		# else:
		# 	self.printk("Interupcao nao implementado")
		return
	
	#Tratando a string que eh digitado no console
	def tratar_instrucao(self):
		#Remove os espacos em brancos da tecla espaco
		comando = self.console_str.strip()	#dividir a string em relacao aos espacos 
		
		if(len(comando) > 0):
			#Dividir o que foi digitado depois do espaco 1 - acao e 2 arquivo.asm
			palavra = comando.split()
			
			#Posicao 0 vem ser os comandos de sair ou executar
			if (palavra[0] == "sair"):
				self.syscall()#informase a interrupcao do teclado
				time.sleep(3)
				self.cpu.cpu_alive = False
		
			elif (palavra[0] == "execute"):
				self.executarProcesso(palavra[1:])	
				
			# Caso comando digitado nao exista	
			else:
				self.terminal.console_print("\rComando Nao Encontrado no Sistema\n")
	
		#Caso usuario nao digite nenhum valor
		else:
			self.terminal.console_print("\rDigite Algum Comando\n")

	#Metodo de executar comando digitado
	def executarProcesso(self, lista):
		if(lista[0].find(".") >= 0): #procura pelo ponto se n encontra retorna -1

			#posicao 0 eh o nome do arquivo / posicao 1 eh a extensao
			arquivo = lista[0].split('.') #dividir a string entre antes e depois do ponto(.)

			#verificar extesoes que podem ser executadas(apenas 'asm')
			if(arquivo[1] == "asm"):
				self.terminal.console_print("\rArquivo Carregado\n")
			else:
				self.terminal.console_print("\rExtesao nao Suportada\n")

	#Mostra na tela a direita mensagemd e fim do Programa
	def syscall(self):
		self.terminal.app_print("Interupcao de Teclado Iniciado. Fim\n")
		return

#Estrutura de um processo
class process_t:
	def __init__ (self):
		pc = int
		regs = [8]
		# memoria_t memoria -> descritores de memoria
		# estado = int