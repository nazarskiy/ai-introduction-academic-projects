import math

class CPos:
    def __init__(self, value, row, col, status):
        self.m_value =  value
        self.m_row = row
        self.m_col = col
        self.m_status = status
        self.m_d = -1
        self.m_p = None
        self.m_h = 0
        self.m_g = float("inf")

    def set_value(self, value):
        self.m_value = value
    def set_status(self, status):
        self.m_status = status
    def set_d(self, d):
        self.m_d = d
    def set_p(self, p):
        self.m_p = p
    def set_h(self, other):
        self.m_h = self.manh_distance(other)
    def set_g(self, g):
        self.m_g = g

    def get_status(self):
        return self.m_status
    def get_value(self):
        return self.m_value
    def get_d(self):
        return self.m_d
    def get_p(self):
        return self.m_p
    def get_h(self):
        return self.m_h
    def get_g(self):
        return self.m_g

    def __lt__(self, other):
        return self.m_h < other.m_h

    def eucl_distance(self, other):
        return math.sqrt((self.m_row - other.m_row) ** 2 + (self.m_col - other.m_col) ** 2)

    def manh_distance(self, other):
        return abs(self.m_row - other.m_row) + abs(self.m_col - other.m_col)

    def neighbours(self, m, n):
        possible_neighbours = [(self.m_row + 1, self.m_col), (self.m_row - 1, self.m_col),
                               (self.m_row, self.m_col - 1), (self.m_row, self.m_col + 1)]
        valid_neighbours = [(r, c) for r, c in possible_neighbours if 0 <= r < m and 0 <= c < n]
        return valid_neighbours
