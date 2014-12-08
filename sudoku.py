import copy

class Sudoku:


	ROW = "ABCDEFGHI"
	COL = "123456789"

	def __init__(self, puzzle):
		self.board = {}
		for i in range(9):
			for j in range(9):
				self.board[self.ROW[i] + self.COL[j]] = int(puzzle[9*i+j])

		self.boxes = {
			'box1': [row+col for row in "ABC" for col in "123"],
			'box2': [row+col for row in "ABC" for col in "456"],
			'box3': [row+col for row in "ABC" for col in "789"],
			'box4': [row+col for row in "DEF" for col in "123"],
			'box5': [row+col for row in "DEF" for col in "456"],
			'box6': [row+col for row in "DEF" for col in "789"],
			'box7': [row+col for row in "GHI" for col in "123"],
			'box8': [row+col for row in "GHI" for col in "456"],
			'box9': [row+col for row in "GHI" for col in "789"]
		}

		self.domain = {}

		for row in self.ROW:
			for col in self.COL:
				if self.board[row+col] == 0:
					self.domain[row+col] = range(1,10)
				else:
					self.domain[row+col] = [self.board[row+col]]

		self.constraints = list(set(self.get_row_constraints() +
		 self.get_col_constraints() + self.get_box_constraints()))


	def get_box_values(self, box):
		return [self.board[cell] for cell in self.boxes['box%d' % box]]

	def get_box_for_variable(self, variable):
		for box in self.boxes.items():
			if variable in box[1]:
				return box[0]

	def get_row(self, row):
		return [row+col for col in self.COL]

	def get_row_values(self, row):
		return [self.board[variable] for variable in self.get_row(row)]

	def get_col(self, col):
		return [row+col for row in self.ROW]

	def get_col_values(self, col):
		return [self.board[variable] for variable in self.get_col(col)]

	def get_row_constraints(self):
		constraints = []
		for row_n in self.ROW:
			row = self.get_row(row_n)

			for row_mm in row:
				for row_nn in row:
					if not row_mm == row_nn and\
					 not (row_mm, row_nn) in constraints:
						constraint = (row_mm, row_nn)
						constraints.append(constraint)

		return constraints

	def get_col_constraints(self):
		constraints = []
		for col_n in self.COL:
			col = self.get_col(col_n)

			for col_mm in col:
				for col_nn in col:
					if not col_mm == col_nn and\
					 not (col_mm, col_nn) in constraints:
					 constraint = (col_mm, col_nn)
					 constraints.append(constraint)

		return constraints

	def get_box_constraints(self):
		constraints = []
		for box in self.boxes.items():
			the_box = box[1]

			for vars_mm in the_box:
				for vars_nn in the_box:
					if not vars_nn == vars_mm and\
					 not (vars_mm, vars_nn) in constraints:
						constraint = (vars_mm, vars_nn)
						constraints.append(constraint)

		return constraints

	def get_neighbors(self, cell, constraints):
		neighbors = filter(
			lambda c: c[0] == cell or c[1] == cell, constraints)

		return map(lambda c: c[0] if c[0] == cell else c[1], 
			constraints)

	def solve_ac3(self):

		queue = list(self.constraints)

		while queue:
			pair = queue.pop(0)
			x_i, x_j = pair

			if self.ac3_remove_inconsistent_values(pair):
				for (a, b) in self.constraints:
					if b == x_i and not a == x_j:
						pair = (a, b)
						queue.append(pair)

			if not self.domain[x_i]:
				return False

		for key in self.domain:
			if not len(self.domain[key]) == 1:
				return False

		return True

	def ac3_remove_inconsistent_values(self, (var1, var2)):
		
		if len(self.domain[var2]) == 1 and self.domain[var2][0] in self.domain[var1]:
			self.domain[var1].remove(self.domain[var2][0])
			return True

		return False

	def solve_backtrack(self):
		domain_copy = copy.deepcopy(self.domain)
		solution = self.__solve_backtrack_recursive({}, domain_copy)
		if solution is not False:
			self.domain = solution
			return True

		return False


	def __solve_backtrack_recursive(self, assignment, current_domain):

		if self.assignment_complete(assignment):
			return assignment

		var = self.select_unassigned_variable(current_domain, assignment)

		for value in self.sort_using_lcv(var, current_domain[var], assignment):
			if self.is_value_consistent(var, value, assignment):

				assignment[var] = [value]

				# forward checking
				new_domain = copy.deepcopy(current_domain)
				for (a, b) in self.constraints:
					if a == var and len(new_domain[b]) > 1 and value in new_domain[b]:
						new_domain[b].remove(value)

				result = self.__solve_backtrack_recursive(assignment, new_domain)

				if result != False:
					return result

				del assignment[var]

		return False


	def sort_using_lcv(self, var, values, assignment):
		return sorted(values, 
			key = lambda val: self.number_of_conflicts(
				var, val, assignment))


	def is_value_consistent(self, *args):
		return self.number_of_conflicts(*args) == 0

	def number_of_conflicts(self, var, value, assignment):

		n_conflicts = 0

		for (a, b) in self.constraints:
			if a == var and b in assignment.keys():
				if assignment[b][0] == value:
					n_conflicts += 1

		return n_conflicts

	def select_unassigned_variable(self, domain, assignment):

		unassigned_vars = filter(lambda x: x not in assignment.keys(),
			domain.keys())

		var = min(unassigned_vars,  
			key = lambda x: len(domain[x]))

		return var

	def assignment_complete(self, assignment):
		return len(assignment) == len(self.domain)

	def print_sudoku(self):
		print "-----------------"
		for i in self.ROW:
			for j in self.COL:
				print self.domain[i + j][0],
			print ""
		