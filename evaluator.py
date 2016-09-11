import re, sys, argparse, math
import parser as AST

def is_value(t): #this function is used to chaeck whether the stack should be checked for pattern matching
	x = t.type
	if x == "app" or x == "op1" or x == "op2":
		return False
	else:
		return True



def lookup (envi, name): # used in cek7 for matching variables to values
	if name not in envi.keys():
		return "invalid"
	else:	
		return envi[name]

def extend (envi, name, value): # used in cek 3 to add variable value mapping in the environment 
	dic = {name:value}
	envi.update(dic)
	return envi



def step(control,envi,stack,evaluation): # used to map various cek cases and return the appropriate status and cek

	if control.type == "app" and len(control.children)==2:
		envi = envi
		l = ["arg",control.children[1],envi]
		control = control.children[0]
		stack.append(l)
		evaluation += "  [cek1]\n"	
		return "fine", control, envi, stack,evaluation

	elif len(stack)!=0 and is_value(control) and stack[-1][0] == "arg" and control.type!="var" :
		l= ["fun", control,envi]
		stack_top = stack.pop()
		control = stack_top[1]
		envi = stack_top[2]
		stack.append(l)
		evaluation += "  [cek4]\n"
		return "fine", control, envi, stack,evaluation

	elif len(stack)!=0 and is_value(control) and stack[-1][0] == "fun" and control.type!="var" and stack[-1][1].type =="lam":
		stack_top = stack.pop()
		envi = extend(envi,stack_top[1].name,control)
		control = stack_top[1].children[0]
		evaluation += "  [cek3]\n"
		return "fine", control, envi, stack,evaluation

	elif is_value(control) and control.type=="var" and lookup(envi, control.name)!="invalid":
		control = lookup(envi, control.name)
		evaluation += "  [cek7]\n"
		return "fine", control, envi, stack,evaluation

	elif control.type=="op1":
		l = ["arg11",control]
		stack.append(l)
		control = control.children[0]
		evaluation += "  [cek2a]\n"
		return "fine", control, envi, stack,evaluation

	elif len(stack)!=0 and is_value(control) and stack[-1][0] == "arg11" and control.type=="num":
		stack_top = stack.pop()
		evaluation += "  [cek5a]\n"
		if stack_top[1].name=="iszero":
			if control.name == "0":
				control.name = "1"

				return "fine", control, envi, stack,evaluation
			else:
				control.name = "0"
				return "fine", control, envi, stack,evaluation

		elif stack_top[1].name=="add1":
			control.name = str(int(control.name)+1)
			return "fine", control, envi, stack,evaluation

		elif stack_top[1].name=="sub1":
			control.name = str(int(control.name)-1)
			return "fine", control, envi, stack,evaluation
		else:
			print("Don't know how to evaluate with this operator")
			return "stuck", control, envi, stack,evaluation

	elif control.type=="op2":
		l = ["arg12",control,control.children[1],envi]
		stack.append(l)
		control = control.children[0]
		evaluation += "  [cek2b]\n"
		return "fine", control, envi, stack,evaluation

	elif len(stack)!=0 and is_value(control) and stack[-1][0] == "arg12":
		stack_top = stack.pop()
		l = ["arg22",stack_top[1],control,envi]
		control = stack_top[2]
		stack.append(l)
		evaluation += "  [cek6b]\n"
		return "fine", control, envi, stack,evaluation

	elif len(stack)!=0 and is_value(control) and stack[-1][0] == "arg22" and control.type=="num" and stack[-1][2].type=="num":
		stack_top = stack.pop()
		evaluation += "  [cek5b]\n"
		if stack_top[1].name=="+":
			control.name = str(int(stack_top[2].name) + int(control.name))

		elif stack_top[1].name=="-":
			control.name = str(int(stack_top[2].name) - int(control.name))

		elif stack_top[1].name=="*":
			control.name = str(int(stack_top[2].name) * int(control.name))

		elif stack_top[1].name=="^":
			control.name = int(stack_top[2].name) ** int(control.name)
			control.name= str(math.floor(control.name))

		return "fine", control, envi, stack,evaluation

	elif control.type =="num" and   len(stack) == 0:
		return "fine", control, envi, stack,evaluation
		
	elif control.type =="lam" and   len(stack) == 0:
		return "fine", control, envi, stack,evaluation

	else:
		return "stuck", control, envi, stack,evaluation


		



def evaluate (tree): # the main function which takes the tree as input and gives us the final status
	control = tree
	envi = {}
	stack = []
	evaluation = "Sequence of rules:\n"
	while True:
		status, control, envi, stack,evaluation = step(control,envi,stack,evaluation)
		if status == "stuck":
			evaluation += "Answer:\n  "
			evaluation += "Stuck"
			break

		elif control.type =="num" and   len(stack) == 0:
			evaluation += "Answer:\n  "
			evaluation += control.name
			break

		elif control.type =="lam" and   len(stack) == 0:
			evaluation += "Answer:\n  "
			evaluation += "function"
			break
			
	return evaluation


	

