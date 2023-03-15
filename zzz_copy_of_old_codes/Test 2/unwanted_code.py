

class Square:
    """
    #Square of the game of chess
    """
    def __init__(self, numrow, numcolumn, ppiece = None):
        self.row = numrow
        self.column = numcolumn
        self.piece = ppiece

def create_all_cases():
    global all_cases
    for file in range(8):
        all_cases.append([])
        for row in range(8):
            all_cases[-1].append(Square(file,row))