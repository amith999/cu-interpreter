'''

Author: Amith Gopal
Program: Interpreter for Mathematical expressions in Python

'''


token_map = dict()
variable_map = dict ()




class Token(object):
	def __init__(self, tok_type, tok_value):
		self.type = tok_type
		self.value = tok_value


class Interpreter(object):
	
	global variable_map
	def __init__(self, text):
		self.text = text
		#print self.text
		self.lex_list = []
		self.is_print = 0
		self.is_expr  = 0
		self.pos = 0
		self.operand_list = []
		self.operator_list = []
		## First assuming that all the lex tokens are space separated
		self.lex_list = self.text.split() # Lexer class
		
		 

	def handle_print_statements(self):
		#print "HANDLING PRINT STATEMENTS"
		#print variable_map
		expression_val = self.evaluate_expression()
		print expression_val


	def handle_assignment_statements (self, temp_pos):
		#print "HANDLING ASSIGNMENT OPERATIONS"
		expression_val = self.evaluate_expression()
		
		variable_map[self.lex_list[temp_pos]] = expression_val
		
	def evaluate(self):
		#print self.pos

		if self.lex_list[self.pos] == "print":
			self.is_print = 1
			self.pos = self.pos + 1
			self.handle_print_statements ()

		elif self.lex_list[self.pos].isalpha() and self.lex_list[self.pos+1] == '=':
			## this seems to be an assignment operation
			if self.lex_list[self.pos] not in variable_map:
				variable_map[self.lex_list[self.pos]] = None

			temp_pos = self.pos
			
			self.pos = self.pos + 2
			self.handle_assignment_statements (temp_pos)
			

	def clear_lists (self):
		self.operator_list = []
		self.operand_list  = []

	def evaluate_expression(self):

		'''
		 	Differentiate between the print statements 
			and the assignment statements
			
		'''

		
		num_ops = len(self.lex_list)

		'''
			
			Checking the current position of the operands and operators
			with the total length of the operators and operands

		'''
		
		while self.pos < num_ops:
			

			if self.lex_list[self.pos].isalpha():
				if self.lex_list[self.pos] not in variable_map:
					print "This means that there are some variables which arent initialised before."
					return
				else:
					var = self.lex_list[self.pos]
					self.lex_list[self.pos] = str(variable_map[var])


			# for the first operator and no operand
			if self.lex_list[self.pos].isdigit():
				if 	(len(self.operator_list) == 0):
					self.operand_list.append(int(self.lex_list[self.pos]))
					#print self.operand_list
				elif ((self.operator_list[-1] == '+')):
					self.operand_list.append(int(self.lex_list[self.pos]))
				# on encountering the multiplication operator pop the first 2 elements from the operand list and the * or / operator
				elif (self.operator_list[-1] == '*'):
					self.operand_list.append (int(self.lex_list[self.pos]) * self.operand_list.pop())
					self.operator_list.pop()
				elif (self.operator_list[-1] == '/'):
					#print self.lex_list[self.pos] + "POPPED ELEMENT " + str(self.operand_list[-1])
					self.operand_list.append (self.operand_list.pop() / int(self.lex_list[self.pos]))
					self.operator_list.pop()
			
			# if it is an operator just push it in the operator list
			elif self.lex_list[self.pos] == '+' \
					or self.lex_list[self.pos] == '-' \
					or self.lex_list[self.pos] == '*' \
					or self.lex_list[self.pos] == '/':
				self.operator_list.append(self.lex_list[self.pos])


			self.pos = self.pos + 1



		#print "OPERATOR LIST " + str(self.operator_list) + "\n"
		#print "OPERAND LIST " + str(self.operand_list) + "\n"

		'''
				Till now all the multiplication and division operations are done. Now we need to descend through the stack and complete
				the addition and the subtraction operations.

		'''

		res = 0
		oper_ctr = len(self.operator_list)
		while oper_ctr:
			
			optr = self.operator_list.pop()
			if optr == '+':
				self.operand_list.append (self.operand_list.pop() + self.operand_list.pop())
			elif optr == '-':
				self.operand_list.append (-1 * (self.operand_list.pop() - self.operand_list.pop()))

			oper_ctr = oper_ctr - 1	

		'''
			The operations of addition, subtraction, multiplication and division
			are done.

			The result will be now in the first element of the operand stack
		'''
		res = self.operand_list.pop()

		self.clear_lists ()

		return res 
			
 

while True:
 	text = str(input())	
 	interpreter = Interpreter (text)
 	interpreter.evaluate()
