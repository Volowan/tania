from func import *

class Position:
    def __init__(self, FEN,threefoldliste=[]):
        self.fen = FEN
        all_infos = FEN.split()
        self.posfen = all_infos[0]
        self.player = all_infos[1]
        self.castle = all_infos[2]
        self.enpassant = all_infos[3]
        self.enpassantcoord = '-' if self.enpassant == '-' else (file_to_coord(self.enpassant[0]),int(self.enpassant[1])-1)
        self.fiftymoves = int(all_infos[4])
        self.movenum = int(all_infos[5])
        ####################################
        self.threefoldlist = [c for c in threefoldliste]
        self.threefoldlist.append(self.posfen)
        self.result_for_white = None
        posfensplit = self.posfen.split("/")
        self.board = []
        self.whitepieces = ''
        self.blackpieces = ''
        sq = [0,7]
        for line in posfensplit:
            self.board.append('')
            for char in line:
                try:
                    self.board[-1] += int(char)*' '
                    sq[0] += int(char)
                except:
                    self.board[-1] += char
                    if char.isupper():
                        self.whitepieces += char
                        if char == 'K':
                            self.Ksq = tuple(sq)
                    else:
                        self.blackpieces += char
                        if char == 'k':
                            self.ksq = tuple(sq)
                    sq[0] += 1
            sq[0] = 0
            sq[1] -=1
