# -*- coding: utf-8 -*-
"""
BIW modular alg demo

A PPPR test

input: BIW task list of project A, SOB of project A (25 cars), initial day of the week, resourse info.
output: Gantt chart 
"""

# In[0]: import packages
import numpy as np
import pandas as pd


# main function
def main(csv_input='projA_input.csv'):
    # In[1]: standarized input
    # tasklist = pd.read_csv(csv_input,sep=',',index_col='Veh_No')
    gantt_s = pd.read_csv('gantt_s.csv',sep=',')
    gantt_d = pd.read_csv('gantt_d.csv',sep=',')
    merge(gantt_s, gantt_d)
    return gantt_s.to_csv(sep=',', index=False)


def merge(left, right):
    for i, row in left.iterrows():
        for j, column in row.iteritems():
            print(j)
            if j != 'Veh_No':
                print(column)
                print(right.at[i, j])
                left.at[i, j] = str(column) + '$' + str(right.at[i, j])
