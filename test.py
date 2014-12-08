__author__ = 'Chao Chen'


cluster_std = [1, 2, 3, 4, 5, 6, 7, 8, 9]

try:
    output = open("output.txt", 'r')
    input = open("sudokus.txt", 'r')
    problem_index = 0
    count_correct_solution = 0
    while 1:
        line = input.readline()
        if not line:
            break
        problem_index += 1

        input_line = line.strip("\r\n")

        out_line = ""
        tmp = output.readline()
        if not tmp:
            break
        for i in xrange(9):
            tmp = output.readline()
            out_line += tmp[0]+tmp[2]+tmp[4]+tmp[6]+tmp[8]+tmp[10]+tmp[12]+tmp[14]+tmp[16]

        for j in xrange(81):
            if input_line[j] != "0" and input_line[j] != out_line[j]:
                print "Sudoku map not matched! Sudoku Number: ", problem_index
                exit()

        cluster_block = []
        cluster_row = []
        cluster_column = []
        is_correct = True

        for m in xrange(3):
            for n in xrange(3):
                for p in xrange(3):
                    for q in xrange(3):
                        cluster_block.append(int(out_line[m*27+n*3+p*9+q]))
                cluster_block.sort()
                if not cluster_block.__eq__(cluster_std):
                    is_correct = False
                cluster_block = []

        for m in xrange(9):
            for n in xrange(9):
                cluster_row.append(int(out_line[m*9+n]))
                cluster_column.append(int(out_line[n*9+m]))
            cluster_row.sort()
            cluster_column.sort()
            if not cluster_row.__eq__(cluster_std):
                is_correct = False
            if not cluster_column.__eq__(cluster_std):
                is_correct = False
            cluster_row = []
            cluster_column = []
        
        if is_correct:
            count_correct_solution += 1
    print "\nTotal problems:          ", problem_index
    print "Total correct solutions: ", count_correct_solution
    output.close()
    input.close()
except:
    print "Error in reading file."
    exit()

