import sys
from e_object import e_object
from e_cursor import Cursor

class Console(e_object):
	
	cursor=Cursor()
	m_user_input=None

	def __init__(self):
		super().__init__()
	


	@staticmethod
	def get_int_input(message):
		user_input=int(input(message))
		return user_input
	@staticmethod
	def get_str_input(message):
		user_input=input(message)
		return user_input
	@staticmethod
	def get_float_input(message):
		user_input=float(input(message))
		return user_input
	
	@staticmethod
	def get_choice_input(message,choice=[]):

		Console.m_user_input=input(message)
		
		if Console.m_user_input=="":

			Console.m_user_input="Enter"
		
		if Console.m_user_input not in choice:
	
			Console.get_choice_input(message,choice)
		else:

			return Console.m_user_input
		

	@staticmethod
	def get_input_data():
		return Console.m_user_input
		
