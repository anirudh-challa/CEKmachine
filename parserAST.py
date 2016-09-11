#Tree data structure. It consists of type of the node, name of the node() and children of the node
class Tree(object):
    def __init__(self):
        self.children = []
        self.type = None
        self.name = None

#get type of the node		
def getTypeName(str):
	index = str.find('(')
	if(index==-1):
		return str,None
	else:
		#print(str[index+1:len(str)-1])
		return str[0:index],str[index+1:len(str)-1]
		

#the values related to num (eg: num 42),op1 (eg: op1 iszero),op2 (eg : op2 +),lam (eg: lam x) etc are stored as name in the tree data structure. app doesn't have any name associated with it.		
def FormAST(input,i):
	if(i[0]>=len(input)):
		return None;
		
	if(input[i[0]]=='Lparen'):
		i[0]=i[0]+1
	
	if(input[i[0]]=='Rparen'):
		i[0]=i[0]+1
		return None;
		
	node = Tree()
	node.type,node.name = getTypeName(input[i[0]])
	i[0]=i[0]+1
	
	type=""
	if(node.type=='lam'):
		type,node.name=getTypeName(input[i[0]])
		i[0]=i[0]+1
	
	
	if(node.type == 'var' or node.type == 'num'):
		return node
	else:
		while(1):
			if(i[0]>=len(input)):
				return None
			if(input[i[0]]=='Lparen'):
				i[0]=i[0]+1
			if(input[i[0]]=='Rparen'):
				i[0]=i[0]+1
				return node
			else:
				child = FormAST(input,i)
				if(child==None):
					return None
				node.children.append(child)
			
	return node;
	
#return syntax_tree string by traversing the tree
def traverse(node,s):
	s[0]+=node.type
	if(node.name!=None):
		s[0]+='('+node.name
	if(node.name==None and len(node.children)!=0):
		s[0]+='('
	elif(len(node.children)!=0):
		s[0]+=', '

	for i in range(0,len(node.children)):
		traverse(node.children[i],s)
		if(i!=len(node.children)-1):
			s[0]+=', '
	s[0]+=")"
	return s[0]
	
	
#forms the AST and returns the syntax_tree string		
def AST(input):
	#print('......')
	tree = FormAST(input,[0])
	ans_string = traverse(tree,[""])
	return ans_string,tree