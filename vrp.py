import numpy as np 
from pulp import *
import pandas as pd

def vrp(items, vehicles,limit):
    time_matrix = pd.read_csv('time_matrix.csv')
    if (len(items))==2:
        return(1, 2*time_matrix.loc[0,1])
    if (len(items))==3:
        return(1, time_matrix.loc[0,1] + time_matrix.loc[0,2] + time_matrix.loc[0,1] + time_matrix.loc[2,0])

    result = []
    result_name = []
    M=10000
    result_df = pd.DataFrame()
    row,col = time_matrix.shape
    vehicles=vehicles

    problem = LpProblem('TravellingSalesmanProblem', LpMinimize)

    # Decision variable X & Y for truck route
    decisionVariableX = LpVariable.dicts('decisionVariable_X', ((i, j, k) for i in items for j in items for k in range(vehicles)), lowBound=0, upBound=1, cat='Integer')
    decisionVariableY = LpVariable.dicts('decisionVariable_y', ((i, k) for i in items for k in range(vehicles)), lowBound=0, upBound=1, cat='Integer')

    # subtours elimination
    decisionVariableU = LpVariable.dicts('decisionVariable_U', ((i, k) for i in items for k in range(vehicles)), lowBound=0, cat='Integer')

    # Decision variable T for truck arrival time
    decisionVariableT = LpVariable.dicts('decisionVariable_T', ((i,k) for i in items for k in range(vehicles)), lowBound=0, cat='Float')

    # Objective Function
    problem += lpSum(decisionVariableT[i, k] for i in items for k in range(vehicles))

    for k in range(vehicles):
        problem += lpSum(decisionVariableY[i, k] for i in items) <= limit
        for i in items:
            problem += (decisionVariableX[i,i, k] == 0) # elimination of (1 to 1) route
            if i==0:
                problem += (decisionVariableT[i, k] == 0) # at node 0 time=0

    for i in items:
        if (i != 0):
            problem += lpSum(decisionVariableY[i, k] for k in range(vehicles)) == 1
            for k in range(vehicles):
                problem += lpSum(decisionVariableX[i, j, k] for j in items)== decisionVariableY[i, k] 
                problem += lpSum(decisionVariableX[j, i, k] for j in items)== decisionVariableY[i, k] 
        if (i == 0):
            for k in range(vehicles):
                problem += lpSum(decisionVariableX[i, j, k] for j in items) <= 1 
                problem += lpSum(decisionVariableX[j, i, k] for j in items) <= 1 
        

    for i in items:
        for j in items:
            for k in range(vehicles):
                if i != j and (j != 0):
                    problem += decisionVariableT[j, k] >= decisionVariableT[i, k] + time_matrix.iloc[i][j] - M*(1-decisionVariableX[i,j, k]) # Calculating time of arrival at each node
                if i != j and (i != 0) and (j != 0):
                    problem += decisionVariableU[i, k]  <=  decisionVariableU[j, k] + M * (1 - decisionVariableX[i, j, k])-1 # sub-tour elimination for truck


    status = problem.solve(CPLEX_CMD()) 
    for var in problem.variables():
        if (problem.status == 1):
            if (var.value() !=0):
                result.append(var.value())
                result_name.append(var.name)
    result_df['Variable Name'] = result_name
    result_df['Variable Value'] = result
    return (problem.status, problem.objective.value())



if (__name__) == ('__main__'):
    items=[0,1,3,4,6,7,8,9]
    sts, obj = vrp(items,3,3)
