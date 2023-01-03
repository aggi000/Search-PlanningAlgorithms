import time
from grid import Grid
from plot_results import PlotResults

def ac3(grid, var):
    """
        This is a domain-specific implementation of AC3 for Sudoku. 

        It keeps a set of arcs to be processed (arcs) which is provided as input to the method. 
        Since this is a domain-specific implementation, we don't need to maintain a graph and a set 
        of arcs in memory. We can store in arcs the cells of the grid and, when processing a cell, 
        we ensure arc consistency of all variables related to this cell by removing the value of
        cell from all variables in its column, row, and unit. 

        For example, if the method is used as a preprocessing step, then arcs is initialized with 
        all cells that start with a number on the grid. This method ensures arc consistency by
        removing from the domain of all variables in the row, column and unit the values of 
        the cells given as input. The method adds to the set of arcs all variables that have
        their values assigned during the propagation of the contrains. 
    """
    if not type(var) == list:
        arcs = [var]
    else:
        arcs = var
    checked = set()
    while len(arcs):
        cell = arcs.pop()
        checked.add(cell)

        assigned_row, failure = grid.remove_domain_row(cell[0], cell[1])
        if failure: return failure

        assigned_column, failure = grid.remove_domain_column(cell[0], cell[1])
        if failure: return failure

        assigned_unit, failure = grid.remove_domain_unit(cell[0], cell[1])
        if failure: return failure

        arcs.extend(assigned_row)
        arcs.extend(assigned_column)
        arcs.extend(assigned_unit)    
    return False

def pre_process_ac3(grid):
    """
    This method enforces arc consistency for the initial grid of the puzzle.

    The method runs AC3 for the arcs involving the variables whose values are 
    already assigned in the initial grid. 
    """
    arcs_to_make_consistent = []

    for i in range(grid.get_width()):
        for j in range(grid.get_width()):
            if len(grid.get_cells()[i][j]) == 1:
                arcs_to_make_consistent.append((i, j))

    ac3(grid, arcs_to_make_consistent)

def select_variable_fa(grid):
    for i in range(grid.get_width()):
        for j in range(grid.get_width()):
            cells= grid.get_cells()[i][j]
            if len(cells)>1:
                return (i,j)

def select_variable_mrv(grid):
    minimum_d=10
    col=-1
    row=-1
    for i in range(grid.get_width()):
        for j in range(grid.get_width()):
            cells= grid.get_cells()[i][j]
            if len(cells)>1:
                if len(cells)<minimum_d:
                    minimum_d=len(cells)
                    col=j
                    row=i
    return (row,col)

def search(grid, var_selector):
    if grid.is_solved():#check if the grid is already solved
        return grid, True
    x = var_selector(grid)#assign to next variable
    for i in grid.get_cells()[x[0]][x[1]]:#try each possible value for the selected variable
        if grid.is_value_consistent(i, x[0], x[1]):
            grid_copy = grid.copy()
            grid_copy.get_cells()[x[0]][x[1]] = i
            if (ac3(grid_copy, x) == False):
                y, z = search(grid_copy, var_selector)#backtracking to solve rest of the grid
                if z:
                    return y, True#return solution
    return None, False

file = open('tutorial_problem.txt', 'r')
problems = file.readlines()
for p in problems:
    g = Grid()
    g.read_file(p)

    # test your backtracking implementation without inference here
    # this test instance is only meant to help you debug your backtracking code
    # once you have implemented forward checking, it is fine to find a solution to this instance with inference

file = open('top95.txt', 'r')
problems = file.readlines()

running_time_fa = []
running_time_mrv = []
for p in problems:
    g = Grid()
    g.read_file(p)
   
    g_copy_fa = g.copy()
    g_copy_mrv = g.copy()

    start_time_fa = time.time()
    pre_process_ac3(g_copy_fa)
    correct_grid_fa, check_fa = search(g_copy_fa, select_variable_fa)
    end_time_fa = time.time()
    running_time_fa.append(end_time_fa-start_time_fa)
    
    start_time_mrv = time.time()
    pre_process_ac3(g_copy_mrv)
    corrected_grid_mrv, check_mrv = search(g_copy_mrv, select_variable_mrv)
    end_time_mrv = time.time()
    running_time_mrv.append(end_time_mrv-start_time_mrv)
    
plotter = PlotResults()
plotter.plot_results(running_time_mrv, running_time_fa,
"Running Time Backtracking (MRV)",
"Running Time Backtracking (FA)", "running_time")
    # test your backtracking implementation with inference here for instance grid_copy