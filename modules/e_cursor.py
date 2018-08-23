import sys
from e_object import e_object


class Cursor(e_object):

	def __init__(self):
		super().__init__()

	def hide(self):
		sys.stdout.write("\033[?25l")
		sys.stdout.flush()

	def show(self):
		sys.stdout.write("\033[?25h")
		sys.stdout.flush()

	
		
