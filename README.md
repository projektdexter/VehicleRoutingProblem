# VehicleRoutingProblem

The [vehicle routing problem](https://en.wikipedia.org/wiki/Vehicle_routing_problem) is a combination of bin packing problem and Travelling Salesperson Problem. VRP is also np-hard. In fact, VRP is more hard than a tsp because of added complexity arising due to multiple vehicles. The below code uses PuLP solver to find the exact solution of the VRP. Other dependencies include numpy and pandas.

The mathematical formulation is similar to the tsp except that there are added constraints on vehicle capacity:

## Sets and Decision variables

$\mathbb{N}$ is the set of all customer node subset $i$ and $j$

$k$ is set of vehicles

We will use 2 binary variables $x_{ijk}$ and $y_{ik}$ where:

$x_{ijk}$ will take the value 1 if truck $k$ travels from node $i$ to node $j$, 0 otherwise. $i\in\mathbb{N}$ and $j\in\mathbb{N}$

$y_{ik}$ will take the value 1 if node $i$ is assigned to truck $k$

Other variables are:

$u_{ik}$ will take the value of the order of node $i$ in the final route of truck $k$. $i\in\mathbb{N}^{}$

$t_{ik}$ represents the arrival time for truck $k$ at node $i$. 

$tt_{ij}$ represents the truck travel time between nodes $i$ and $j$. 

$M$ is a very large number


Objective: Minimize the total time to visit all nodes

$$ Obj=min\{\sum_{i=D}^{D'}t_{ik}\} $$

Constraint 1: All non-zero nodes have to be visited by a truck exactly once 

$$ \sum_{k}^{K}y_{ik}=1 $$

Constraint 2: Node 0 should have K departures

$$ \sum_{k}^{K}y_{ok}=K $$

Constraint 3: $y_{ik}$ is 1 only when $x_{ijk}$ is 1

$$ \sum_{i}^{}x_{ijk}=\sum_{i}^{}x_{jik}=\sum_{i}^{}y_{ik} $$ 

Constraint 4: Vehicle limit capacity

$$ \sum_{i}^{}y_{ik}<=C $$ 

Constraint 5: Avoiding sub-tours for truck

$$ u_{ik}-u_{jk}-1\leq M(1-x_{ijk}) $$

Input Parameters:

**_time_matrix_**: is a **_NxN_** cost matrix between the points that have to be visited by the nodes, example:

```
    0     1   2     3   4
0   0  21.0  15  21.0  10
1  21   0.0   5   0.5  11
2  15   5.0   0   5.0   5
3  21   0.5   5   0.0  10
4  10  11.0   5  10.0   0
```

For small instances with $\leq15$ nodes, the vrp_exact function will give the exact solution.

## Example 1:

<img src=https://user-images.githubusercontent.com/114884444/198330529-16e2fe72-fbd9-4b71-93a6-2dbaafee60e2.png width="400">

With the below distance matrix:
```
time_matrix=
0	1	2	3	4	5	6	7	8
0	14.015	14.411	14.749	21.253	19.333	9.37	10.186	15.054
14.003	0	5.317	30.438	9.109	16.033	6.13	5.209	5.062
14.022	5.251	0	30.411	6.656	14.415	8.705	4.708	1.047
14.755	30.741	30.746	0	37.979	21.296	26.096	26.521	31.389
21.384	8.819	5.854	37.818	0	21.869	14.803	25.428	6.925
18.62	16.179	15.038	21.287	21.128	0	23.369	10.812	15.68
9.89	5.853	8.274	26.325	14.396	23.082	0	13.935	8.031
9.987	5.599	4.458	26.377	10.709	10.938	7.619	0	5.1
15.122	6.061	1.372	31.512	7.284	15.516	8.907	5.354	0

vrp_exact(time_matrix)
```
## Output:
<img src=https://user-images.githubusercontent.com/114884444/198349841-7bd10ef9-bf80-48a0-9e1a-996881532dd3.png width=400>


