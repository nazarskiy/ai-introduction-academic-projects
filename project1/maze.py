from pos import CPos
import os

class CMaze:
    def __init__(self, path):
        self.m_Maze = []
        self.m_s = self.m_e = [-1, -1]
        with open(path, "r") as f:
            for r_index, line in enumerate(f):
                row = []
                for c_index, char in enumerate(line):
                    if char == 'X' or char == ' ':
                        row.append(CPos(char, r_index, c_index, "not_found"))
                    elif char == 's':
                        self.m_s = [int(word) for word in line.replace(", ", ' ').split() if word.isdigit()]
                        self.m_Maze[self.m_s[1]][self.m_s[0]].set_value('S')
                    elif char == 'e':
                        self.m_e = [int(word) for word in line.replace(", ", ' ').split() if word.isdigit()]
                        self.m_Maze[self.m_e[1]][self.m_e[0]].set_value('E')
                    else: break
                if row:
                    self.m_Maze.append(row)

        if self.m_s == self.m_e:
            self.m_Maze[self.m_s[1]][self.m_s[0]].set_value('Q')

        self.m_m = len(self.m_Maze)
        self.m_n = len(self.m_Maze[0])

    def uvpath(self, u, v):
        path = []
        while u != v:
            path.append(v)
            v = v.get_p()
        return path

    def stdoutput(self, path):
        os.system("cls" if os.name == "nt" else "clear")
        for row in self.m_Maze:
            for i in row:
                if i in path:
                    print('o', end = '')
                else:
                    print(i.get_value(), end = '')
            print()