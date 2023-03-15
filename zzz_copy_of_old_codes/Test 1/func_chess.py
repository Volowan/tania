import pygame
import random

pygame.init()

numb2file = {
    0:'a',
    1:'b',
    2:'c',
    3:'d',
    4:'e',
    5:'f',
    6:'g',
    7:'h'
}

symbol={
    'bK':'♔',
    'bQ':'♕',
    'bR':'♖',
    'bB':'♗',
    'bN':'♘',
    'bp':'♙',
    'wK':'♚',
    'wQ':'♛',
    'wR':'♜',
    'wB':'♝',
    'wN':'♞',
    'wp':'♟'
}

#Original placement of pieces
original_placement = {
    'wp':[['a','b','c','d','e','f','g','h'],[2]],
    'wR':[['a','h'],[1]],
    'wN':[['b','g'],[1]],
    'wB':[['c','f'],[1]],
    'wQ':[['d'],[1]],
    'wK':[['e'],[1]],
    'bp':[['a','b','c','d','e','f','g','h'],[7]],
    'bR':[['a','h'],[8]],
    'bN':[['b','g'],[8]],
    'bB':[['c','f'],[8]],
    'bQ':[['d'],[8]],
    'bK':[['e'],[8]]
}

test_placement = {
    'wp':[[],[]],
    'wR':[[],[]],
    'wN':[['a'],[1]],
    'wB':[['b'],[3]],
    'wQ':[[],[]],
    'wK':[['g'],[6]],
    'bp':[[],[]],
    'bR':[[],[]],
    'bN':[[],[]],
    'bB':[[],[]],
    'bQ':[[],[]],
    'bK':[['h'],[8]]
}

files = ['a','b','c','d','e','f','g','h']
rows = [1,2,3,4,5,6,7,8]


all_pieces_name = ['p','R','N','B','Q','K']



move = 1 #odd = white to play
piecesterminal = False
wantcalculations = False
seecalculations = False
lastturnofcalculations = 0

class Square:
    """
    square of chess named by its file a-h and its row 1-8
    """
    def __init__(self, numfile, numbrow, ppiece = "", firstkingkill = ""):
        self.numbfile = numfile
        self.file = numb2file[numfile]
        self.row = numbrow + 1
        self.piece = ppiece
        self.enpassant = False
        self.firstkingkilled = firstkingkill
        if (numfile+1 + numbrow+1)%2 == 0:
            self.shade = "dark"
        else:
            self.shade = "light"


class Piece:
    """
    Piece of chess
    """
    def __init__(self, team, kind, movedyett = False):
        self.color = team
        if team == 'b':
            self.colornumb = 0
        elif team == 'w':
            self.colornumb = 1
        self.type = kind
        self.movedyet = movedyett


allcases = []
allpieces = []

def createcases():
    global allcases
    for i in range(8):
        for j in range(8):
            allcases.append(Square(i,j))

def placepieces():
    global all_pieces_name, allpieces, allcases
    for i in all_pieces_name:
        for j in ["w","b"]:
            k = j+i
            place = place_of_pieces[k]
            for case in allcases:
                if case.file in place[0] and case.row in place[1]:
                    allpieces.append(Piece(k[0],k[1:]))
                    case.piece = allpieces[-1]

def codeofcaseterminal(case):
    global piecesterminal
    if case.piece:
        col = str(case.piece.color)
        kind = str(case.piece.type)
        code = col+kind
        if piecesterminal:
            return(f"{symbol[code]} ")
        else:
            return(code)
    else:
        return("  ")

def showchessboardterminal(allcases):
    global symbol
    print('-----------------------------------------')
    for i in range(8):
        print(f'| {codeofcaseterminal(allcases[7-i])} | {codeofcaseterminal(allcases[15-i])} | {codeofcaseterminal(allcases[23-i])} | {codeofcaseterminal(allcases[31-i])} | {codeofcaseterminal(allcases[39-i])} | {codeofcaseterminal(allcases[47-i])} | {codeofcaseterminal(allcases[55-i])} | {codeofcaseterminal(allcases[63-i])} |')
        print('-----------------------------------------')

def nomove(deltaf,deltar):
    if deltaf==0 and deltar==0:
        return(True)
    return(False)

def selfcheck():
    return(False)

def clearmvt(case1,case2,jump = False,caneat=True,havetoeat=False):
    if jump and clearlanding(case1,case2,caneat,havetoeat):
        return(True)
    elif clearpath(case1,case2) and clearlanding(case1,case2,caneat,havetoeat):
        return(True)
    else:
        return(False)

def clearpath(case1,case2):
    global allcases
    deltaf,deltar = cases2deltas(case1,case2)
    distance = max(abs(deltaf),abs(deltar))
    if deltaf == 0:
        stepf = 0
    else:
        stepf = deltaf/(abs(deltaf))
    if deltar == 0:
        stepr = 0
    else:
        stepr = deltar/(abs(deltar))
    for i in range(1,distance):
        for case in allcases:
            if case.numbfile == case1.numbfile+(i*stepf) and case.row == case1.row+(i*stepr):
                if case.piece:
                    return(False)
    return(True)

def clearlanding(case1,case2,caneat,havetoeat):
    global allcases
    if not case2.piece and havetoeat and not case2.enpassant:
        return(False)
    if (not case2.piece and (not havetoeat or case2.enpassant))  or (case2.piece.color != case1.piece.color and caneat):
        if havetoeat and case2.enpassant:
            for case in allcases:
                if case.file == case2.file and case.row == case1.row:
                    
                    case.piece = ""
        return(True)
    else:
        return(False)

def resetenpassant():
    global move, allcases
    for case in allcases:
        if case.enpassant and move == case.enpassant+1:
            case.enpassant = False

def legal_mvt_king(case1,case2):
    deltaf,deltar = cases2deltas(case1,case2)
    if nomove(deltaf,deltar):
        return(False)
    elif max(abs(deltaf),abs(deltar)) == 1 and not selfcheck() and clearmvt(case1,case2):
        return(True)
    else:
        return(False)

def legal_mvt_rook(case1,case2):
    deltaf,deltar = cases2deltas(case1,case2)
    if nomove(deltaf,deltar):
        return(False)
    elif min(abs(deltaf),abs(deltar)) == 0 and not selfcheck() and clearmvt(case1,case2):
        return(True)
    else:
        return(False)

def legal_mvt_bishop(case1,case2):
    deltaf,deltar = cases2deltas(case1,case2)
    if nomove(deltaf,deltar):
        return(False)
    elif abs(deltaf)==abs(deltar) and not selfcheck() and clearmvt(case1,case2):
        return(True)
    else:
        return(False)

def cases2deltas(case1,case2):
    df = case2.numbfile-case1.numbfile
    dr = case2.row-case1.row
    return(df,dr)

def legal_mvt_queen(case1,case2):
    if legal_mvt_bishop(case1,case2) or legal_mvt_rook(case1,case2):
        return(True)
    else:
        return(False)

def legal_mvt_knight(case1,case2):
    deltaf,deltar = cases2deltas(case1,case2)
    if nomove(deltaf,deltar):
        return(False)
    elif ((deltaf)**2+(deltar)**2) == 5 and not selfcheck() and clearmvt(case1,case2,jump = True):
        return(True)
    else:
        return(False)

def legal_mvt_pawn(case1,case2,move,simulation):
    global allcases
    deltaf,deltar = cases2deltas(case1,case2)
    if deltaf == 0 and ((deltar == -((-1)**case1.piece.colornumb)*2 and not case1.piece.movedyet) or deltar == -((-1)**case1.piece.colornumb)) and clearmvt(case1,case2,caneat=False):
        for case in allcases:
            if case.row == case1.row -((-1)**case1.piece.colornumb) and case.file == case1.file:
                if not simulation:
                    case.enpassant = move
        return(True)
    elif abs(deltaf) == 1 and deltar == -((-1)**case1.piece.colornumb) and clearmvt(case1,case2,havetoeat=True):
        return(True)
    else:
        return(False)

def legal(case1,case2,move,simulation = False):
    colorplaying = 'w' if move%2 == 1 else 'b'
    if case1.piece and case1.piece.color == colorplaying:
        if case1.piece.type =="K" and legal_mvt_king(case1,case2):
            return(True)
        elif case1.piece.type =="Q" and legal_mvt_queen(case1,case2):
            return(True)
        elif case1.piece.type =="R" and legal_mvt_rook(case1,case2):
            return(True)
        elif case1.piece.type =="B" and legal_mvt_bishop(case1,case2):
            return(True)
        elif case1.piece.type =="N" and legal_mvt_knight(case1,case2):
            return(True)
        elif case1.piece.type =="p" and legal_mvt_pawn(case1,case2,move,simulation):
            return(True)
        else:
            return(False)
    else:
        return(False)

def check(board, move):
    for case in board:
        if case.piece and case.piece.colornumb == move%2:
            case2 = case
            break
    for case in board:
        if legal(case,case2,move+1,simulation=True):
            return(True)
    return(False)

def promotion(case2):
    choice = ""
    while not choice in ["Q","R","B","N"]:
        print("In which piece to you want to upgrade ? (Q,R,B,N):")
        choice = input("")
    stockpawn = case2.piece
    case2.piece = Piece(stockpawn.color,choice)


def mouvement(case1name,case2name, move):
    global allcases
    for case in allcases:
            if case.file == case1name[0] and case.row == int(case1name[1]):
                case1 = case
            if case.file == case2name[0] and case.row == int(case2name[1]):
                case2 = case
    if legal(case1,case2,move):
        resetenpassant()
        if not case1.piece.movedyet:
            case1.piece.movedyet = True
        if case2.piece and case2.piece.type == "K" and not allcases[0].firstkingkilled:
            allcases[0].firstkingkilled = case2.piece.color
        case2.piece = case1.piece
        case1.piece = ""
        if case2.piece and case2.piece.type == "p" and ((case2.row == 8 and case2.piece.color == "w") or (case2.row == 1 and case2.piece.color == "b")):
            promotion(case2)
        increasemove()
    else:
        print("Illegal move !")

def castlemovement(c1c2, move):
    global allcases
    rowofkingtable = ["","","","","","","",""]
    if move%2==1:
        rowofking=1
    else:
        rowofking=8
    for case in allcases:
        if case.row == rowofking:
            rowofkingtable[case.numbfile] = case
    if c1c2 == "O-O":#PLUS TARD, IL FAUDRA S'ASSURER QUE L'ENNEMI NE CONTROLE PAS LES CASES
        if not rowofkingtable[5].piece and not rowofkingtable[6].piece and not rowofkingtable[4].piece.movedyet and not rowofkingtable[7].piece.movedyet:
            rowofkingtable[6].piece = rowofkingtable[4].piece
            rowofkingtable[5].piece = rowofkingtable[7].piece
            rowofkingtable[4].piece = ""
            rowofkingtable[7].piece = ""
            resetenpassant()
            rowofkingtable[6].piece.movedyet = True
            rowofkingtable[5].piece.movedyet = True
            increasemove()
    elif c1c2 == "O-O-O":#PLUS TARD, IL FAUDRA S'ASSURER QUE L'ENNEMI NE CONTROLE PAS LES CASES
        if not rowofkingtable[1].piece and not rowofkingtable[2].piece and not rowofkingtable[3].piece and not rowofkingtable[4].piece.movedyet and not rowofkingtable[0].piece.movedyet:
            rowofkingtable[2].piece = rowofkingtable[4].piece
            rowofkingtable[3].piece = rowofkingtable[0].piece
            rowofkingtable[4].piece = ""
            rowofkingtable[0].piece = ""
            resetenpassant()
            rowofkingtable[2].piece.movedyet = True
            rowofkingtable[3].piece.movedyet = True
            increasemove()

def piecesorletters():
    global piecesterminal
    print("Wanna play with pieces ? (y/n)")
    yesno = input("")
    if yesno == "y":
        piecesterminal = True

def wannaseecalculations():
    global seecalculations,wantcalculations
    print(f"Wanna see the calculations ? (Not recommanded if your deepness is higher than 2, actual deepness: {wantcalculations}) (y/n)")
    yesno = input("")
    if yesno == "y":
        seecalculations = True


#Value of a first killed king is 200 to dissuade a trade of king
valueOfPieces ={
    'p':1,
    'N':3,
    'B':3,
    'R':5,
    'Q':9,
    'K':100
}

def countmaterial(board):
    score = 0
    if board[0].firstkingkilled:
        if board[0].firstkingkilled == "w":
            score += 200
        else:
            score -= 200
    for case in board:
        if case.piece:
            score += -(-1)**case.piece.colornumb*valueOfPieces[case.piece.type]
    return(score)

def increasemove():
    global move
    move += 1
    print(f"move number is {move}")

def doyouwantcalculation():
    global wantcalculations
    print("Do you want calculations (0 = no, other = deepness)?")
    number = input()
    wantcalculations = int(number)



def calculate(deepness,position,move):
    if deepness == 0:
        return(("none",countmaterial(position)))
    else:
        tableau = []
        tableauchiffres = []
        tableaubest = []
        for indice1,case1 in enumerate(position):#IL MANQUE LES CASTLES ET LES PROMOTIONS
            for indice2,case2 in enumerate(position):
                if legal(case1,case2,move,simulation = True):
                    positionp = []
                    for caseact in position:
                        casep = Square(caseact.numbfile,caseact.row-1)
                        if caseact.piece:
                            pieceact = caseact.piece
                            piecep = Piece(pieceact.color,pieceact.type,movedyett = pieceact.movedyet)
                            casep.piece = piecep
                        positionp.append(casep)
                    case1p = positionp[indice1]
                    case2p = positionp[indice2]
                    case2p.piece = case1.piece
                    case1p.piece = ""
                    if seecalculations:
                        print(f"Calculation of {case1.file}{case1.row}{case2.file}{case2.row} ^_^")
                        showchessboardterminal(positionp)
                    tableau.append(((f"{case1.file}{case1.row}{case2.file}{case2.row}"),calculate(deepness-1,positionp,move+1)[1]))
        if tableau:
            for elem in tableau:
                tableauchiffres.append(elem[1])
            if move % 2 == 1:#white to play
                bestchiffre = max(tableauchiffres)
            else:
                bestchiffre = min(tableauchiffres)
            for elem in tableau:
                if elem[1] == bestchiffre:
                    tableaubest.append(elem)
            return(random.choice(tableaubest))
        else:#LOL MEC IL FAUT CODER QQCH ICI
            print("Lol, Je sais pas quoi f mon bro")
            return(("Lol","Je sais pas quoi f mon bro"))

"""
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
-----------------------------------LE PROGRAMME YO---------------------------------------------
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
"""
place_of_pieces = test_placement
#place_of_pieces = original_placement

#######CREATOR MODE#########
creatormode = False
if creatormode:
    piecesterminal = False
    wantcalculations = 3
    seecalculations = False
############################

createcases()
placepieces()

if not creatormode:
    piecesorletters()
    doyouwantcalculation()
    if wantcalculations:
        wannaseecalculations()

ordicouleur = 0# 0 for black, 1 for white

while True:
    showchessboardterminal(allcases)
    """#player vs player
    if move%2 == ordicouleur:
        if move != lastturnofcalculations:
            advice = calculate(wantcalculations,allcases,move)
            lastturnofcalculations = move
            print(f"My advice is {advice}")
        else:
            print(f"My advice is still {advice}")
    """
    print(f"Score : {countmaterial(allcases)}")
    print(f"{'move for black :' if move%2==0 else 'move for white :'}")
    #Computer vs human
    if move%2 == ordicouleur:
        advice = calculate(wantcalculations,allcases,move)
        print(f"{advice}")
        c1c2 = advice[0]
    else:
        c1c2 = input()
    try:
        if c1c2[0] in files and int(c1c2[1]) in rows and c1c2[2] in files and int(c1c2[3]) in rows:
            print(f"your move is {c1c2[0:2]} to {c1c2[2:4]}")
            mouvement(c1c2[0:2],c1c2[2:4],move)
        elif c1c2 in ["O-O","O-O-O"]:
            castlemovement(c1c2,move)
    except:
        pass
