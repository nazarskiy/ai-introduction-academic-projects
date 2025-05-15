from checker import CChecker

class CComchecker(CChecker):
    def __repr__(self):
        return "⚪" if self.m_white else "⚫"

    def clone(self):
        return CComchecker(self.m_white)
