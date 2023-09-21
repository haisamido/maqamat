#!/usr/bin/env python3

import numpy as np

intervals    = 7
scale_length = 3

x=np.arange(intervals)

# for i, cent in enumerate(x):
#     print(i)

m=7
scale_length=3

A=np.zeros(((m+1)*2, m+1), dtype=int)

row = 0
col = 0

while row <= m:
    print(row,col)
    
    while col <= m:    
        A[row][col] = 1
        A[row][0]   = 1
        sum_of_row  = A.sum(axis=1)
        
        if sum_of_row[row] == scale_length:
            print("  SUM: ", row, col, sum_of_row[row])
            row     = row + 1

        col = col+1

    col=0
     
print(A)

    
# col=0..m
#   row=0
    #   cell(0,0)=1
    #   cell(0,1)=1
    #   cell(0,2)=1
    # if sum(cell(1,0..2))=scale_length=3
    #    row=row+1
#   row=1
    #   cell(1,0)=1
    #   cell(1,1)=1
    #   cell(1,3)=1
    # if sum(cell(2,1..2,4))=scale_length=3
    #    row=row+1
#   row=3
    #   cell(3,1)=1
    #   cell(3,2)=1
    #   cell(3,5)=1
    # if sum(cell(3,1..2,5))=scale_length=3
    #    row=row+1
#   row=4
    #   cell(4,1)=1
    #   cell(4,2)=1
    #   cell(4,6)=1
    # if sum(cell(4,1..2,6))=scale_length
    #    row=row+1
#   row=5
    #   cell(5,1)=1
    #   cell(5,2)=1
    #   cell(5,7)=1   
    # if sum(cell(5,1..2,7))=scale_length
    #    row=row+1
#   row=6
    #   cell(6,1)=1
    #   cell(6,2)=1
    #   cell(6,8)=1   



# 0,1,2,3,4,5,6,7
#
# if 3
#          6x6
    # 1, 1,1,0,0,0,0,0
    # 1, 1,0,1,0,0,0,0
    # 1, 1,0,0,1,0,0,0
    # 1, 1,0,0,0,1,0,0
    # 1, 1,0,0,0,0,1,0
    # 1, 1,0,0,0,0,0,1

#            5x5
    # 1, 0,1,1,0,0,0,0
    # 1, 0,1,0,1,0,0,0
    # 1, 0,1,0,0,1,0,0
    # 1, 0,1,0,0,0,1,0
    # 1, 0,1,0,0,0,0,1

#              4x4
    # 1, 0,0,1,1,0,0,0
    # 1, 0,0,1,0,1,0,0
    # 1, 0,0,1,0,0,1,0
    # 1, 0,0,1,0,0,0,1

#                3x3
    # 1, 0,0,0,1,1,0,0
    # 1, 0,0,0,1,0,1,0
    # 1, 0,0,0,1,0,0,1

#                  2x2
    # 1, 0,0,0,0,1,1,0
    # 1, 0,0,0,0,0,1,1

# if 4
    #      6x5
    # 1, 1,1,1,0,0,0,0
    # 1, 1,0,1,1,0,0,0
    # 1, 1,0,0,1,1,0,0
    # 1, 1,0,0,0,1,1,0
    # 1, 1,0,0,0,0,1,1    
    #
    # 1, 0,1,1,1,0,0,0
    # 1, 0,1,0,1,1,0,0
    # 1, 0,1,0,0,1,1,0
    # 1, 0,1,0,0,0,1,1

    # 1, 0,0,1,1,1,0,0
    # 1, 0,0,1,0,1,1,0
    # 1, 0,0,1,0,0,1,1
    
    # 1, 0,0,0,1,1,1,0
    # 1, 0,0,0,1,0,1,1