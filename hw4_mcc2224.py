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
		print "Failed to solve using AC-3"

print "Solved %d sudokus using AC-3 inference" % num_ac3_solved

# 1.6 solve all sudokus by backtracking
for line in sudokuList.split("\n"):
	s = Sudoku(line)
	if s.solve_backtrack():
		s.print_sudoku()
	else:
		print "Failed to solve using backtrack"