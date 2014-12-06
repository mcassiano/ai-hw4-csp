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

		self.neighbors = {row+col: self.get_neighbors(row+col, 
			self.constraints) for row in self.ROW for col in self.COL}

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
				for x_k in self.neighbors[x_i]:
					pair = (x_k, x_i)
					queue.append(pair)

	def ac3_remove_inconsistent_values(self, (var1, var2)):
		removed = False
		for value_var1 in self.domain[var1]:
			found_value = False
			for value_var2 in self.domain[var2]:
				if value_var1 != value_var2:
					found_value = True

			if not found_value and not len(self.domain[var1]) == 1:
				self.domain[var1].remove(value_var1)
				removed = True

		return removed

	def print_(self):
		print "-----------------"
		for i in self.ROW:
			for j in self.COL:
				print self.domain[i + j],
			print ""


if __name__ == "__main__":

	s = Sudoku("003020600900305001001806400008102900700000008006708200002609500800203009005010300")
	s.solve_ac3()
	#print s.domain