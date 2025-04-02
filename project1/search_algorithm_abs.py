from maze import CMaze
import time
from abc import abstractmethod

class CSearchAlg:
    def __init__(self, path):
        self.m_maze = CMaze(path)
        self.m_s = self.m_maze.m_Maze[self.m_maze.m_s[1]][self.m_maze.m_s[0]]
        self.m_e = self.m_maze.m_Maze[self.m_maze.m_e[1]][self.m_maze.m_e[0]]
        self.m_expanded = 0

    def stdoutinfo(self, d):
        print('-' * self.m_maze.m_m)
        print("S Start")
        print("E End")
        print("# Opened node")
        print("o Path")
        print("X Wall")
        print("space Fresh node")
        print('-' * self.m_maze.m_m)
        print(f"Nodes expanded: {self.m_expanded}")
        print(f"S-E-Path lenght: {d}")

    def viz(self, d, path):
        time.sleep(0.0001)
        self.m_maze.stdoutput(path)
        self.stdoutinfo(d)

    @abstractmethod
    def solve_maze(self):
        pass
