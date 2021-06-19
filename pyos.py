import os
import curses
import pycfg
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

	def interrupt_keyboard (self):
		key = self.terminal.get_key_buffer()

		if ((key >= ord('a')) and (key <= ord('z'))) or ((key >= ord('A')) and (key <= ord('Z'))) or ((key >= ord('0')) and (key <= ord('9'))) or (key == ord(' ')) or (key == ord('-')) or (key == ord('_')) or (key == ord('.')):
		
			self.console_str = self.console_str + chr(key)
			self.terminal.console_print("\r" + self.console_str)
			
		elif key == curses.KEY_BACKSPACE:
			self.console_str = self.console_str[:-1]
			self.terminal.console_print("\r" + self.console_str)
			
		elif (key == curses.KEY_ENTER) or (key == ord('\n')):
			self.comando_terminal()
			self.sair_terminal(self.console_str)
			self.console_str = ""
			self.terminal.console_print("\r")
			
			
	def handle_interrupt (self, interrupt):
		if interrupt == pycfg.INTERRUPT_KEYBOARD:
			self.interrupt_keyboard()
			
	def sair_terminal(self, console):
		if console == "sair":
			self.cpu.cpu_alive = False

	def syscall (self):
		#self.terminal.app_print(msg)
		return

	def comando_terminal(self):
		ler = self.console_str.split(" ")

		if(self.console_str == "msg"):
			if(ler[0] == "msg"):
				self.sair_terminal(self.console_str)
			
			return