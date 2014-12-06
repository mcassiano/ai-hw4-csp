#!/usr/bin/env python
#coding:utf-8
from sudoku import Sudoku

# Reading of sudoku list from file
try:
    f = open("sudokus.txt", "r")
    sudokuList = f.read()
except:
	print "Error in reading the sudoku file."
	exit()

# 1.5 count number of sudokus solved by AC-3
num_ac3_solved = 0
for line in sudokuList.split("\n"):
	s = Sudoku(line)
	if s.solve_ac3():
		num_ac3_solved += 1
		s.print_sudoku()
	else:
		print "Failed to solve"

print "Solved %d sudokus" % num_ac3_solved

exit()

# 1.6 solve all sudokus by backtracking
for line in sudokuList.split("\n"):
	# Parse sudokuList to individual sudoku in dict, e.g. sudoku["A2"] = 1
	sudoku = {ROW[i] + COL[j]: int(line[9*i+j]) for i in range(9) for j in range(9)}

	# write your backtracking algorithms here

	printSudoku(sudoku)