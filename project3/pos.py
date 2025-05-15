from checker import CChecker

class CPos:
    def __init__(self, r: int, c: int, is_blank: bool, checker: CChecker = None):
        self.m_r = r
        self.m_c = c
        self.m_blank = is_blank
        self.m_checker = checker

    def __repr__(self):
        if self.m_blank: return " ."
        return " " + repr(self.m_checker)