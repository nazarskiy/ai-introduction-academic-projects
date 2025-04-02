from BFS import CBFS
from DFS import CDFS
from RandomSearch import CRandomSearch
from GreedySearch import CGreedySearch
from AStar import CAStar

def solve_the_maze(path, alg):
    if alg == 1:
        solver = CBFS(path)
    elif alg == 2:
        solver = CDFS(path)
    elif alg == 3:
        solver = CRandomSearch(path)
    elif alg == 4:
        solver = CGreedySearch(path)
    else:
        solver = CAStar(path)
    solver.solve_maze()