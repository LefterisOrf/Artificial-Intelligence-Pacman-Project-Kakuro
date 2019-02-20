import time
from csp import *
from input_puzzles import *

class Kakuro(CSP):
	

	def __init__(self, grid):
        #grid values: -1 for a black cell, 0 for an empty cell or (row constraint,col constraint)
		values = [1,2,3,4,5,6,7,8,9]#range(1,10)# each variable can take the values from 1 to 9
		self.grid = grid
		self.variables = []
		self.right_constraint = dict()
		self.down_constraint = dict()
		self.neighbors = dict()
		current_row = 0
		for row in range(len(grid)):
			for col in range(len(grid[row])):
				cell = grid[row][col]
				if cell == '_': #variable cell
					self.variables.append((row,col))
				elif cell == '*': continue #empty black cell
				else: # constraint black cell
					if cell[0] != '': # omadopoiw tis metablites poy anhkoyn sto idio down_constraint me ena entry gia kathe metabliti
						for i in range(row+1,len(grid)):
							if grid[i][col] == '_':
								if (i,col) not in self.neighbors.keys():
									self.neighbors.setdefault((i,col),[])
								if (i,col) not in self.down_constraint.keys():
									self.down_constraint.setdefault((i,col),[])# arxikopoiw to down_constraint[(i,col)] me mia kenh lista
								for j in range(row+1,len(grid)):
									if grid[j][col] == '_':
										if j != i:
											self.down_constraint[(i,col)].append((j,col))
											self.neighbors[(i,col)].append((j,col))#oses metablites symmetexoyn mazi se periorismoys
									else: break
							else: break
					if cell[1] != '': # to idio me ta right_constraints
						for i in range(col+1,len(grid[row])):
							if grid[row][i] == '_':
								if (row,i) not in self.neighbors.keys():
									self.neighbors.setdefault((row,i),[])
								if (row,i) not in self.right_constraint.keys():
									self.right_constraint.setdefault((row,i),[])
								for j in range(col+1,len(grid[row])):
									if grid[row][j] == '_':
										if j != i:
											self.right_constraint[(row,i)].append((row,j))
											self.neighbors[(row,i)].append((row,j))
									else: break
							else: break
		self.domain = dict()
		for i in self.variables:
			self.domain[i] = values
		self.assignment = dict()
		self.function_calls = 0
		CSP.__init__(self ,self.variables, self.domain, self.neighbors, self.Function)
		#print("Done creating the kakuro var, with assignment:",CSP.infer_assignment(self))

	def Function(self, A, value_a, B, value_b):
		self.function_calls += 1
		if value_a == value_b: return False
		assignment = CSP.infer_assignment(self)
		domain_A = [ 1, 2, 3, 4, 5, 6, 7, 8, 9]
		domain_B = [ 1, 2, 3, 4, 5, 6, 7, 8, 9]
		Sum_row = 0
		Sum_col = 0
		c_col = False
		c_row = False
		if A[0] == B[0]: #common row
			c_row = True
		elif A[1] == B[1]: #common column
			c_col = True
		else:
			print("Oops")

		# Remove values from A 
		if A in self.down_constraint.keys():
			column_num = A[1]
			row_num = A[0]
			while (isinstance(self.grid[row_num][column_num], list) == False):#find the constraint node
				if (self.grid[row_num][column_num] =='*'):
					print("Error no constraint node not found")
					break
				row_num -= 1 #go up a step till the constraint node is found
			constraint_node = self.grid[row_num][column_num]
			Sum_constraint = constraint_node[0]
			Sum_col = Sum_constraint

			vars_in_constraint = 1 #1 because A is not on self.down_constraint[A]
			for var in self.down_constraint[A]:# for the remaining variables under the same constraint
				if var in assignment.keys(): # if they have an assigned value
					if assignment[var] in domain_A:
						domain_A.remove(assignment[var])# remove it from the A's possible values
					Sum_constraint -= assignment[var]
				else:
					vars_in_constraint += 1

			MaxValue = Sum_constraint - vars_in_constraint*(vars_in_constraint-1)/2 #Maximum value that a node can take under the constraint
			MinValue = Sum_constraint - ((20-vars_in_constraint)*(vars_in_constraint-1)/2)#Minimum value that a node can take
			domain_A = [x for x in domain_A if (x <= MaxValue) and (x >= MinValue)]

		if A in self.right_constraint.keys():
			column_num = A[1]
			row_num = A[0]
			while (isinstance(self.grid[row_num][column_num], list) == False):
				if (self.grid[row_num][column_num] =='*'):
					print("Error no constraint node found")
					break
				column_num -= 1 #go left a step till the constraint node is found
			constraint_node = self.grid[row_num][column_num]
			Sum_constraint = constraint_node[1]
			Sum_row = Sum_constraint
			vars_in_constraint = 1
			for var in self.right_constraint[A]:# for the remaining variables under the same constraint
				if var in assignment.keys():
					if assignment[var] in domain_A:
						domain_A.remove(assignment[var])
					Sum_constraint -= assignment[var]
				else:
					vars_in_constraint += 1

			MaxValue = Sum_constraint - vars_in_constraint*(vars_in_constraint-1)/2 #Maximum value that a node can take under the constraint
			MinValue = Sum_constraint - ((20-vars_in_constraint)*(vars_in_constraint-1)/2)#Minimum value that a node can take
			#print ("With Sum_constraint=",Sum_constraint," and vars_in_constraint=",vars_in_constraint,", MaxValue=",MaxValue)
			domain_A = [x for x in domain_A if (x <= MaxValue) and (x >= MinValue)]

		if (value_a not in domain_A):return False

		# Remove values from B  
		if B in self.down_constraint.keys():
			column_num = B[1]
			row_num = B[0]
			while (isinstance(self.grid[row_num][column_num], list) == False):
				if (self.grid[row_num][column_num] =='*'):
					print("Error no constraint node not found")
					break
				row_num -= 1 #go up a step till the constraint node is found
			constraint_node = self.grid[row_num][column_num]
			Sum_constraint = constraint_node[0]
			Sum_col = Sum_constraint
			vars_in_constraint = 1
			for var in self.down_constraint[B]:# for the remaining variables under the same constraint
				if var in assignment.keys():
					if assignment[var] in domain_B:
						domain_B.remove(assignment[var])
					Sum_constraint -= assignment[var]
				else:
					vars_in_constraint += 1
			MaxValue = Sum_constraint - vars_in_constraint*(vars_in_constraint-1)/2 #Maximum value that a node can take under the constraint
			MinValue = Sum_constraint - ((20-vars_in_constraint)*(vars_in_constraint-1)/2)#Minimum value that a node can take
			domain_B = [x for x in domain_B if (x <= MaxValue) and (x >= MinValue)]

		if B in self.right_constraint.keys():
			column_num = B[1]
			row_num = B[0]
			while (isinstance(self.grid[row_num][column_num], list) == False):
				if (self.grid[row_num][column_num] == '*'):
					print("Error no constraint node found")
					break
				column_num -= 1 #go left a step till the constraint node is found
			constraint_node = self.grid[row_num][column_num]
			Sum_constraint = constraint_node[1]
			Sum_row = Sum_constraint
			vars_in_constraint = 1
			for var in self.right_constraint[B]:# for the remaining variables under the same constraint
				if var in assignment.keys():
					if assignment[var] in domain_B:
						domain_B.remove(assignment[var])
					Sum_constraint -= assignment[var]
				else:
					vars_in_constraint += 1
			MaxValue = Sum_constraint - vars_in_constraint*(vars_in_constraint-1)/2 #Maximum value that a node can take under the constraint
			MinValue = Sum_constraint - ((20-vars_in_constraint)*(vars_in_constraint-1)/2)#Minimum value that a node can take
			domain_B = [x for x in domain_B if (x <= MaxValue) and (x >= MinValue)]
			if (value_b not in domain_B):
				return False
			temp_sum = 0
			if c_col == True:
				for var in self.down_constraint[A]:
					if var != B:
						if var in assignment.keys():
							temp_sum += assignment[var]
				if (temp_sum + value_a + value_b) > Sum_col: return False
			if c_row == True:
				for var in self.right_constraint[A]:
					if var != B:
						if var in assignment.keys():
							temp_sum += assignment[var]
				if (temp_sum + value_a + value_b) > Sum_row: return False
			return True

def main():
	
	while (True):
		print ("Difficulty 0: puzzle0, puzzle1\nDifficulty 1: puzzle2\nDifficulty 2: puzzle3")
		selection = input("Please select a puzzle (0,1,2,3) or type \"exit\" to exit:")
		if selection == "0":
			puz = puzzle0
			print("Puzzle0 selected!")
		elif selection == "1":
			puz = puzzle1
			print("Puzzle1 selected!")
		elif selection == "2":
			puz = puzzle2
			print("Puzzle2 selected!")
		elif selection == "3":
			puz = puzzle3
			print("Puzzle3 selected!")
		elif selection == "4":
			puz = puzzle4
			print("Puzzle4 selected!")
		elif selection == "exit" or selection == "Exit" or selection == "EXIT":
			break
		else:
			print ("Wrong command given, puzzle2 is selected by default")
			puz = puzzle2

		myvar = Kakuro(puz)
		print ("Backtracking search")
		start_time = time.time()
		result = backtracking_search(myvar )
		print (result)
		print ("Finished backtracking_search in",time.time()-start_time," seconds")
		print ("Constraint function calls: ", myvar.function_calls)
		print ("Number of assignments: ",myvar.nassigns)
		print ("\n\n")

		myvar = Kakuro(puz)
		print ("Forward Checking")
		start_time = time.time()
		result = backtracking_search(myvar, inference = forward_checking )
		print (result)
		print ("Finished Forward Checking in",time.time()-start_time," seconds")
		print ("Constraint function calls: ", myvar.function_calls)
		print ("Number of assignments: ",myvar.nassigns)
		print ("\n\n")

		myvar = Kakuro(puz)
		print ("Forward Checking with MRV")
		start_time = time.time()
		result = backtracking_search(myvar, inference = forward_checking, select_unassigned_variable = mrv )
		print (result)
		print ("Finished Forward Checking-MRV in",time.time()-start_time," seconds")
		print ("Constraint function calls: ", myvar.function_calls)
		print ("Number of assignments: ",myvar.nassigns)
		print ("\n\n")

		myvar = Kakuro(puz)
		print ("Mac")
		start_time = time.time()
		result = backtracking_search(myvar, inference = mac )
		print (result)
		print ("Finished mac in",time.time()-start_time," seconds")
		print ("Constraint function calls: ", myvar.function_calls)
		print ("Number of assignments: ",myvar.nassigns)
		print ("\n\n")

		myvar = Kakuro(puz)
		print ("Min_con")
		start_time = time.time()
		result = min_conflicts(myvar)
		print (result)
		print ("Finished min_conflicts in",time.time()-start_time," seconds")
		print ("Constraint function calls: ", myvar.function_calls)
		print ("Number of assignments: ",myvar.nassigns)

		print ("\n\n\n")



if __name__ == "__main__":
	main()