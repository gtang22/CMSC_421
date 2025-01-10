import collections, sys, os
from logic import *
from planning import *

############################################################
# Problem: Planning 

# Blocks world modification
def blocksWorldModPlan():
    # BEGIN_YOUR_CODE (make modifications to the initial and goal states)
    initial_state = 'On(A, B) & Clear(A) & OnTable(B) & OnTable(D) & Clear(C) & On(C,D)'
    goal_state = 'On(B, A) & On(C, B) & On(D,C)'
    # END_YOUR_CODE

    planning_problem = \
    PlanningProblem(initial=initial_state,
                    goals=goal_state,
                    actions=[Action('ToTable(x, y)',
                                    precond='On(x, y) & Clear(x)',
                                    effect='~On(x, y) & Clear(y) & OnTable(x)'),
                             Action('FromTable(y, x)',
                                    precond='OnTable(y) & Clear(y) & Clear(x)',
                                    effect='~OnTable(y) & ~Clear(x) & On(y, x)')])
    
    return linearize(GraphPlan(planning_problem).execute())


def logisticsPlan():
    # BEGIN_YOUR_CODE (use the previous problem as a guide and uncomment the starter code below if you want!)
    # Test case 1 Initial: 'At(R1, D1) & On(R1, C1) & At(C2, D1) & At(C3, D2) & ~Empty(R1)'
    # Test case 1 End: 'At(R1, D3) & At(C2, D1) & At(C3, D2) & On(R1, C1) & ~Empty(R1)'
    # Real End: 'At(R1, D3) & At(C1, D3) & At(C2, D3) & At(C3, D3) & ~Empty(R1)'
    # Problem: D3
    
    
    # Test case 2 Initial: 'At(R1, D1) & On(R1, C1) & At(C2, D1) & At(C3, D2) & ~Empty(R1)'
    # Test case 2 End: 'At(C1, D2)'
    # Test 2 result: [Move(D1, D2, R1), Unload(C1, D2, R1)]
    
    # Test case 3 Initial: 'At(R1, D1) & On(R1, C1) & At(C2, D1) & At(C3, D2) & ~Empty(R1)'
    # Test case 3 End: 'At(C1, D1) & At(R1, D2) & Empty(R1)'
    # Test 3 result: Move(D1, D2, R1), Unload(C1, D1, R1)]
    
    # Test case 4 Initial: 'At(R1, D1) & On(R1, C1) & At(C2, D1) & At(C3, D2) & ~Empty(R1)'
    # Test case 4 End: 'At(C1, D1) & At(R1, D2) & On(C3, R1) & ~Empty(R1) & At(C2, D1)' 
    # Test 4 result: [Unload(C1, D1, R1), Move(D1, D2, R1), Load(C3, D2, R1)]
    # Gets another answer that's not right sometimes (moves C2 for some reason)
    
    initial_state = 'At(R1, D1) & On(C1, R1) & At(C2, D1) & At(C3, D2) & ~Empty(R1)'
    goal_state = 'At(C1, D1) & At(R1, D2) & On(C3, R1) & ~Empty(R1) & At(C2, D1)'
    weights = {'Move' : 
                        {Expr('Move', Expr('D1'), Expr('D2'), Expr('R1')) : 3,
                         Expr('Move', Expr('D2'), Expr('D1'), Expr('R1')) : 3,
                         Expr('Move', Expr('D2'), Expr('D3'), Expr('R1')) : 5,
                         Expr('Move', Expr('D3'), Expr('D2'), Expr('R1')) : 5,
                         Expr('Move', Expr('D1'), Expr('D3'), Expr('R1')) : 10,
                         Expr('Move', Expr('D3'), Expr('D1'), Expr('R1')) : 10
                         },
               'Unload' : 1, 
               'Load' : 1}
    '''
    move1 = Expr('Move', Expr('D1'), Expr('D2'), Expr('R1'))
    print(type(move1))
    print(move1.op)
    print(move1.args)
    
    
    Notes for Extra credit:
    Weight for each container:
        C1: 5
        C2: 8
        C3: 3
    
    Max carrying capacity: 10 
    Robot can carry mutiple boxes at the same time
    Unloading/loading can only happen once per box
    '''
    planning_problem = \
    PlanningProblem(initial=initial_state,
                     goals=goal_state,
                     actions=[Action('Move(x, y, r)', #x is prev location, y is new location, z is R1
                                     precond='At(r, x)',
                                     effect='At(r, y)',
                                     domain='Robot(r) & Place(x) & Place(y)'),
                              Action('Load(x, y, z)', # x is the box, y is location, z is R1
                                     precond='Empty(z) & At(z, y) & At(x, y)',
                                     effect='~Empty(z) & On(x, z)',
                                     domain='Robot(z) & Container(x) & Place(y)'),
                              Action('Unload(x, y, z)', # x is the box, y is location, z is R1
                                     precond='On(x, z) & At(z, y) & ~Empty(z)',
                                     effect='At(x, y) & Empty(z) & At(z, y)',
                                     domain='Robot(z) & Container(x) & Place(y)')],
                     domain='Container(C1) & Container(C2) & Container(C3) & Robot(R1) & Place(D1) & Place(D2) & Place(D3)'
                    )
    

    '''
    graphtemp = planning_problem
    graphtemp.act(expr('Unload(C1, D1, R1)'))
    graphtemp.act(expr('Move(D1, D2, R1)'))
    graphtemp.act(expr('Load(C3, D2, R1)'))
    print(graphtemp.goal_test())
    '''
    #Works do why doesn't the code do that automatically? Screwing up for 1st part of part b
    # Doesn't pick up on certain preconditions that isn't being achieved. Never figure out pickup 
    # so it won't do it
    
    
    #graph = linearize(GraphPlan(planning_problem, weights).execute())
    graph = Linearize(planning_problem=planning_problem).execute()
    # END_YOUR_CODE
    # Get cost from linearized graph
    cost = 0
    for step in graph:
        operation = step.op
        #print(operation)
        if operation in weights.keys():
            tempCost = 0
            temp = weights.get(operation)
            if type(temp) == dict:
                if weights.get(operation).get(step) is not None:
                    tempCost = weights.get(operation).get(step)
            else:
                tempCost = temp
            print(f"Cost of {operation}: " + str(tempCost))
            cost = tempCost + cost
            
    return graph, cost





def logisticsPlanExtraCredit():
    # Don't touch (states are fixed)
    initial_state = 'At(R1, D1) & On(C1, R1) & At(C2, D1) & At(C3, D2)'
    goal_state = 'At(R1, D3) & At(C1, D3) & At(C2, D3) & At(C3, D3)'
    '''    
    Notes for Extra credit:
    Weight for each container:
        C1: 5
        C2: 8
        C3: 3
    
    Max carrying capacity: 10 (Meanign only C1 and C3 can be carried at the same time)
    Robot can carry mutiple boxes at the same time
    Unloading/loading can only happen once per box
    '''
    planning_problem = \
    PlanningProblem(initial=initial_state,
                     goals=goal_state,
                     actions=[Action('Move(x, y, r)', #x is prev location, y is new location, z is R1
                                     precond='At(r, x)',
                                     effect='At(r, y)',
                                     domain='Robot(r) & Place(x) & Place(y)'),
                              Action('Load(x, y, z)', # x is the box, y is location, z is R1
                                     precond='At(z, y) & At(x, y)',
                                     effect='On(x, z)',
                                     domain='Robot(z) & Container(x) & Place(y)'),
                              Action('Unload(x, y, z)', # x is the box, y is location, z is R1
                                     precond='On(x, z) & At(z, y)',
                                     effect='At(x, y)& At(z, y)',
                                     domain='Robot(z) & Container(x) & Place(y)')],
                     domain='Container(C1) & Container(C2) & Container(C3) & Robot(R1) & Place(D1) & Place(D2) & Place(D3)'
                    )
    '''
    graphtemp = planning_problem
    graphtemp.act(expr('Unload(C1, D1, R1)'))
    graphtemp.act(expr('Move(D1, D2, R1)'))
    graphtemp.act(expr('Load(C3, D2, R1)'))
    print(graphtemp.goal_test())
    '''
    #graph = linearize(GraphPlan(planning_problem, weights).execute())
    graph = Linearize(planning_problem=planning_problem).execute()
    return graph

#a = blocksWorldModPlan()
a, cost = logisticsPlan()
print("Total cost: " + str(cost))
print(a)


#logisticsPlan()