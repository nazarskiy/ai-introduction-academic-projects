from abc import abstractmethod

class CChecker:
    def __init__(self, is_white: bool):
        self.m_white = is_white
        self.m_black = not is_white

    @abstractmethod
    def __repr__(self):
        pass

    def simpe_directions(self):
        return [(1, -1), (1, 1)] if self.m_white else [(-1, -1), (-1, 1)]

    def capture_directions(self):
        return [(1, 1), (1, -1), (-1, 1), (-1, -1)]