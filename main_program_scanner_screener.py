import re, sys, argparse
import parserAST as AST
import evaluator as evaluate

# Keywords
def p_lambda(parser, token): return "lam"
def p_app(parser, token): return "app"
def p_add1(parser, token): return "op1(add1)"
def p_sub1(parser, token): return "op1(sub1)"
def p_iszero(parser, token): return "op1(iszero)"

# Operators
def p_operator(parser, token): return "op2(%s)" % token

# Num
def p_num(parser, token): return "num(%s)" % int(token)

# ID
def p_identifier(parser, token): return "var(%s)" % token

# Parens
def p_lparen(parser, token): return "Lparen" 
def p_rparen(parser, token): return "Rparen" 

parser = re.Scanner([
    # Key words
    (r"lam", p_lambda),
    (r"app", p_app),
    (r"add1", p_add1),
    (r"sub1", p_sub1),
    (r"iszero", p_iszero),

    # Operators
    (r"=|\+|-|\*|\^", p_operator),
    
    # Parns
    (r"\(", p_lparen),
    (r"\)", p_rparen),

    # Num
    (r"\d+", p_num),

    # ID
    (r"[a-zA-Z_]\w*", p_identifier),

    (r"\s+", None),
    ])

# Keywords
def s_lambda(scanner, token): return "ID(lam)"
def s_app(scanner, token): return "ID(app)"
def s_add1(scanner, token): return "ID(add1)"
def s_sub1(scanner, token): return "ID(sub1)"
def s_iszero(scanner, token): return "ID(iszero)"

# Operators
def s_operator(scanner, token): return "OP(%s)" % token

# Num
def s_num(scanner, token): return "NUM(%s)" % int(token)

# ID
def s_identifier(scanner, token): return "ID(%s)" % token

# Parens
def s_lparen(scanner, token): return "Lparen" 
def s_rparen(scanner, token): return "Rparen" 

# WS
def s_whitespace(scanner, token): return "WS"

scanner = re.Scanner([
    # Key words
    (r"lam", s_lambda),
    (r"app", s_app),
    (r"add1", s_add1),
    (r"sub1", s_sub1),
    (r"iszero", s_iszero),

    # Operators
    (r"=|\+|-|\*|\^", s_operator),
    
    # Parns
    (r"\(", s_lparen),
    (r"\)", s_rparen),

    # Num
    (r"\d+", s_num),

    # ID
    (r"[a-zA-Z_]\w*", s_identifier),

    (r"\s+", s_whitespace),
    ])
    


if __name__ == '__main__':


	output_string = ""


	for line in sys.stdin:
		scanner_tokens = scanner.scan(line)[0]
		if scanner_tokens[-1] == "WS":
			scanner_tokens = scanner_tokens[:-1]

		parser_tokens = parser.scan(line)[0]
		
		syntax_tree,tree = AST.AST(parser_tokens)
		
		evaluate_string = evaluate.evaluate(tree)
		
		input_string = "Input string:\n  " + line
		scanner_tokens = "Scanner tokens:\n  " +  ', '.join(scanner_tokens) + "\n" 
		parser_tokens = "Parser tokens:\n  " + ', '.join(parser_tokens) + "\n"
		syntax_tree = "Syntax tree:\n  " + syntax_tree + "\n"
		output = input_string + scanner_tokens + parser_tokens + syntax_tree + evaluate_string + "\n\n"
		
		output_string += output


	output_string += "done"
	#f = open("output.txt", "w+")
	#f.write(output_string)

	print(output_string)

'''
# Test suit
input1 = "42"
print(scanner.scan(input1))

input2 = "(app 43 44)"
print(scanner.scan(input2))

input3 = "(lam hello (app hello hello))"
print(scanner.scan(input3))

input4 = "(lam x (app y (add1 (sub1 (iszero (+ 2 (- 3 (* hello (^ 33 44)))))))))"
print(scanner.scan(input4))

input5 = "(^ (-0 5) 2)"
print(scanner.scan(input5))

input6 = "(^ 4 0)"
print(scanner.scan(input6))

input7 = "blah"
print(scanner.scan(input7))

input8 = "(app (+ 2 3) 4)"
print(scanner.scan(input8))

input9 = "(iszero 2)"
print(scanner.scan(input9))

input10 = "(iszero 0)"
print(scanner.scan(input10))

input11 = "(app (lam x x) 3)"
print(scanner.scan(input11))

input12 = "(app (app (app (app (lam x (app x x)) (lam f (lam n (lam a (lam b (app (app n (lam m (app (app (app (app f f) m) a) (app a b)))) b)))))) (lam s (lam z (app s (lam s (lam z z)))))) (lam x (+ x 1))) 5)"
print(scanner.scan(input12))

input13 = "(lam z (app (lam x (app x x)) (lam x (app x x))))"
print(scanner.scan(input13))

'''



