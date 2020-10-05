## Reference on how to design the checker piece class
# https://github.com/techwithtim/Python-Checkers-AI/blob/master/checkers/piece.py

class individual_checker:

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.isKing = False

    def make_king(self):
        self.king = True

