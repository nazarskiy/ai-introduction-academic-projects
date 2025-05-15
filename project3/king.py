from checker import CChecker

class CKing(CChecker):
    def __repr__(self):
        return "Q" if self.m_white else "K"

    def clone(self):
        return CKing(self.m_white)