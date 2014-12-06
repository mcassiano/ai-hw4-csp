#!/usr/bin/env python
#coding:utf-8

# utility function to print each sudoku
def printSudoku(sudoku):
	print "-----------------"
	for i in ROW:
		for j in COL:
			print sudoku[i + j],
		print ""	



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
	# Parse sudokuList to individual sudoku in dict, e.g. sudoku["A2"] = 1
	sudoku = {ROW[i] + COL[j]: int(line[9*i+j]) for i in range(9) for j in range(9)}
	# write your AC3 algorithms here, update num_ac3_solved
	
	printSudoku(sudoku)

# 1.6 solve all sudokus by backtracking
for line in sudokuList.split("\n"):
	# Parse sudokuList to individual sudoku in dict, e.g. sudoku["A2"] = 1
	sudoku = {ROW[i] + COL[j]: int(line[9*i+j]) for i in range(9) for j in range(9)}

	# write your backtracking algorithms here

	printSudoku(sudoku)