
import collections

# The problem Class
class CSP_Problem ():
    def __init__(self, vars, domain, constraints):
        self.vars = vars
        self.domain = domain
        self.constraints = constraints

    def updateVars (self, varName, value):
        self.vars[varName] = value

    def updateDomain(self, varName, domain):
        self.domain[varName] = domain

    def isConsistent(self, var, val, assignment):
    	self.vars[var] = val
    	if(self.constraints()):
    		assignment[var] = val
    		return True
    	self.vars.pop(var)
    	return False
    	
    def forward_check(self, var, val):
    	temp_lst = list()
    	for i in range(0,9):
		row = []
		col = []
		for j in range(0, 9):
			row.append(str(i)+str(j))
			col.append(str(j)+str(i))
                temp_lst.append(row)
                temp_lst.append(col)
        temp_lst.append(['00','01','02','10','11','12','20','21','22'])
        temp_lst.append(['03','04','05','13','14','15','23','24','25'])
        temp_lst.append(['06','07','08','16','17','18','26','27','28'])
        temp_lst.append(['30','31','32','40','41','42','50','51','52'])
        temp_lst.append(['33','34','35','43','44','45','53','54','55'])
        temp_lst.append(['36','37','38','46','47','48','56','57','58'])
        temp_lst.append(['60','61','62','70','71','72','80','81','82'])
        temp_lst.append(['63','64','65','73','74','75','83','84','85'])
        temp_lst.append(['66','67','68','76','77','78','86','87','88'])
	for chk in temp_lst:
		if var in chk:
			for p in chk:
				if p == var:
					continue
				elif val in self.domain[p]:
					self.domain[p].remove(val)
					if len(self.domain[p]) == 0:
						return False
	return True


def select_unassigned_variable(csp_problem):
	temp = [t for t in csp_problem.vars.keys() if csp_problem.vars[t] == '_']
	temp = list(temp)
	if len(temp)==0:
		return None
	x = temp[0]
	#print(x)
	for var in temp:
		if(len(csp_problem.domain[var]) < len(csp_problem.domain[x])):
			x = var
	return x

def backtrackingSearch(csp_problem):
    return recursive_backtracking({}, csp_problem)

def recursive_backtracking(assignment, csp_problem):
    if len(assignment) == len(csp_problem.vars):
        return assignment
    var = select_unassigned_variable(csp_problem)
    if var == None:
    	if len([k for k in csp_problem.vars.keys() if csp_problem.vars[k] == '_']) == 0:
    		return csp_problem.vars
    	return None
    for val in csp_problem.domain[var]:
        if csp_problem.isConsistent(var, val, assignment):
            #csp_problem.assign(var, val, assignment)
            csp_problem.forward_check(var, val)
            #Renderer.render(csp_problem.vars)
            #print(csp_problem.domain)
            result = recursive_backtracking(assignment, csp_problem)
            if result is not None:
                return result
        #csp_problem.unassign(var, assignment)
    return None

# Human Readable printer Class
class Renderer():
	def __init__(self):
		pass

	@staticmethod
	def render(assignment):
		for i in range(0,9):
			disp = " |"
			for j in range(0, 9):
				disp = "{}{}{}".format(disp, assignment[str(i)+str(j)]," |")
			print(disp)
			print("-"*28)

# Game Class
class Game():

	def __init__(self, filename):
		pad = self.loadGame(filename)
		Vars, domainMap = {}, {}
		for i in range(0, len(pad)):
			for j in range(0, len(pad[i])):
				Vars[str(i)+str(j)] = pad[i][j]
				if pad[i][j] != '_':
					domainMap[str(i)+str(j)] = [pad[i][j]]
				else:
					domainMap[str(i)+str(j)] = [str(k) for k in range(1,10)]
		print("Iinitial Sudoku board")
		Renderer.render(Vars)
		def Alldiff(lst_in):
			lst = [self.csp_problem.vars[lst_in[n]] for n in range(0, len(lst_in))]
			lst = list(filter(('_').__ne__, lst))
			if len([item for item, count in collections.Counter(lst).items() if count > 1]) == 0:
				return True
			else:
				return False
		
		def const_func():
			r = False
			c = False
			b = False
			for i in range(0,9):
				row = []
				col = []
				for j in range(0, 9):
					row.append(str(i)+str(j))
					col.append(str(j)+str(i))
				r = Alldiff(row)
				c = Alldiff(col)
			b1,b2,b3= ['00','01','02','10','11','12','20','21','22'],['03','04','05','13','14','15','23','24','25'],['06','07','08','16','17','18','26','27','28']
			b4,b5,b6 = ['30','31','32','40','41','42','50','51','52'],['33','34','35','43','44','45','53','54','55'],['36','37','38','46','47','48','56','57','58']
			b7,b8,b9 = ['60','61','62','70','71','72','80','81','82'],['63','64','65','73','74','75','83','84','85'],['66','67','68','76','77','78','86','87','88']
			b = Alldiff(b1) and Alldiff(b2) and Alldiff(b3) and Alldiff(b4) and Alldiff(b5)
			b = b and Alldiff(b6) and Alldiff(b7) and Alldiff(b8) and Alldiff(b9)
			return (r and c and b)
		self.csp_problem = CSP_Problem(Vars, domainMap, const_func)
		self.initialCleanUp()
	
	def initialCleanUp(self):
		ks = [k for k in self.csp_problem.vars.keys() if self.csp_problem.vars[k] != '_']
		ks = list(ks)
		#print(keys)
		for key in ks:
			if(not self.csp_problem.forward_check(key, self.csp_problem.vars[key])):
				print("{} {}".format(key, "Failed"))

	def loadGame(self, filename):
		try:
			file = open(filename, "r")
			raw_Data = file.read()
			file.close()
			raw_Data = raw_Data.replace("\n", "")
			#print(raw_Data)
			raw_Data = raw_Data.replace(",", "")
			raw_Data = raw_Data.replace(" ", "")
			#print(raw_Data)
			lst_raw_data = list(raw_Data)[1:-1]
			#print(lst_raw_data)
			pad = []
			i = 0;
			while  i < len(lst_raw_data):
				pad.append([lst_raw_data[t] for t in range(i, i+9)])
				i+=9
			return pad
		except Exception, e:
			print("Failed to load the initial Game.\n Check the file and try again.")
			raise e
	def play(self):
		assignment = backtrackingSearch(self.csp_problem);
		if(assignment == None):
			print("The program failed to solve the Sudoku")
		else:
			print("Final Sudoku board")
			Renderer.render(assignment);

if __name__ == '__main__':
	filename = "data.txt"
	myGame = Game(filename)
	myGame.play()
