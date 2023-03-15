#############################################################################
############################# COMMENTS ######################################
#############################################################################
"""
The way that the code is written, I think that if a discover selfcheck append when you eat a pawn en passant, the program will consider that legal

Be careful I got a bug with castle, control if king and rook didn't move but rook has been eaten, is long castle allowed anyway ?
"""
#############################################################################
############################# MODULES #######################################
#############################################################################
import pygame
import random
import time

#############################################################################
############################ VARIABLES ######################################
#############################################################################
pygame.init()

mini = False

player_view = 'w'

arial_font = pygame.font.SysFont("arial", 15, True)

stockpositions = []

moves_notation = []

screen = pygame.display.set_mode((1,1))



if not mini:
    border_chessboard_pix = 800
    chosen_pieces_sprite = pygame.image.load('Test 2/Chess_Pieces_Sprite_Reduced.png')
else:
    border_chessboard_pix = 400
    chosen_pieces_sprite = pygame.image.load('Test 2/Chess_Pieces_Sprite_Mini.png')



width_square = border_chessboard_pix//8#px

menu_width_pix = 200#px

res_screen = (border_chessboard_pix+menu_width_pix, border_chessboard_pix)

colorlight = (130, 150, 130)

colordark = (100, 120, 100)

colorlighthighlight = (160, 170, 80)

colordarkhighlight = (140, 150, 65)

backgroundcolor = (200, 200, 200)

last_move = []

possible_moves_pieces = {#Vecteurs directeurs et distance max (val. absolue)
    'K':[[(0,1),(1,-1),(1,0),(1,1)],1],
    'Q':[[(0,1),(1,-1),(1,0),(1,1)],7],
    'R':[[(0,1),(1,0)],7],
    'B':[[(1,1),(1,-1)],7],
    'N':[[(-2,1),(-1,2),(1,2),(2,1)],1],
    'wp':[[(-1,1),(1,1)],1],
    'bp':[[(-1,-1),(1,-1)],1],
    'castle_short':[(2,0)],
    'castle_long':[(-2,0)]}

possible_moves_pawn = {
    'wmove':[(0,1)],
    'wfirstmove':[(0,2)],
    'weat':[(-1,1),(1,1)],
    'bmove':[(0,-1)],
    'bfirstmove':[(0,-2)],
    'beat':[(-1,-1),(1,-1)]}

computertohumanfiles = {0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h'}

actual_position = None

all_pieces_names = ['K','p','R','N','B','Q']

original_placement = {
    'wK':[(4,0)],
    'wp':[(0,1),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1)],
    'wR':[(0,0),(7,0)],
    'wN':[(1,0),(6,0)],
    'wB':[(2,0),(5,0)],
    'wQ':[(3,0)],
    'bK':[(4,7)],
    'bp':[(0,6),(1,6),(2,6),(3,6),(4,6),(5,6),(6,6),(7,6)],
    'bR':[(0,7),(7,7)],
    'bN':[(1,7),(6,7)],
    'bB':[(2,7),(5,7)],
    'bQ':[(3,7)]}

pawn_battle_placement = {
    'wK':[(4,0)],
    'wp':[(0,1),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1)],
    'wQ':[],
    'wR':[],
    'wB':[],
    'wN':[],
    'bK':[(4,7)],
    'bp':[(0,6),(1,6),(2,6),(3,6),(4,6),(5,6),(6,6),(7,6)],
    'bQ':[],
    'bR':[],
    'bB':[],
    'bN':[],}

symbol_terminal={
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
    'wp':'♟'}

mateNB_placement = {
    'wK':[(4,3)],
    'bK':[(7,7)],
    'wp':[],
    'bp':[],
    'wQ':[],
    'bQ':[],
    'wR':[],
    'bR':[],
    'wB':[],
    'bB':[(2,7)],
    'wN':[],
    'bN':[(1,5)]}

test_placement = {
    'wK':[(6,0)],
    'bK':[(3,6)],
    'wp':[(0,1),(1,1),(2,1),(3,3),(5,2),(6,1),(7,1)],
    'bp':[(0,6),(1,4),(2,5),(3,4),(6,5)],
    'wQ':[(6,2)],
    'bQ':[(5,5)],
    'wR':[(0,0),(4,2)],
    'bR':[(0,7),(5,6)],
    'wB':[(1,2)],
    'bB':[(2,7)],
    'wN':[(1,0)],
    'bN':[(1,5)]}

player_color = 'w' #First player to play ('w' or 'b')

#############################################################################
############################# CLASSES #######################################
#############################################################################
class Piece:
    """
    Piece of chess
    """
    position_on_sprite = {'bK':(0,1),'bQ':(1,1),'bR':(4,1),'bB':(2,1),'bN':(3,1),'bp':(5,1),'wK':(0,0),'wQ':(1,0),'wR':(4,0),'wB':(2,0),'wN':(3,0),'wp':(5,0)}
    def __init__(self, team, kind, numfile, numrow, movedyett = False):
        self.color = team #'w' white, 'b' black
        self.type = kind #The letter of the piece
        self.file = numfile
        self.row = numrow
        self.movedyet = movedyett
        self.position_sprite = Piece.position_on_sprite[team+kind]

class Position:
    def __init__(self, whiteppieces, blackppieces, castle, semiturn, caseenpassant = None):
        self.whitepieces = whiteppieces
        self.blackpieces = blackppieces
        self.board = [[None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None]]
        self.castles = castle
        self.halfturn = int(semiturn)
        self.enpassant = caseenpassant
        for piece in (self.whitepieces + self.blackpieces):
            self.board[piece.file][piece.row] = piece

#############################################################################
######################### SMALL FUNCTIONS ###################################
#############################################################################
def mousepos2square(mousepos):
    global player_view
    return(((mousepos[0]//width_square,7-(mousepos[1]//width_square)) if player_view == 'w' else (7-(mousepos[0]//width_square),mousepos[1]//width_square)))

def copyposition(position):
    fakewhitepieces = []
    fakeblackpieces = []
    for piece in position.whitepieces:
        fakewhitepieces.append(Piece('w',piece.type,piece.file,piece.row,piece.movedyet))
    for piece in position.blackpieces:
        fakeblackpieces.append(Piece('b',piece.type,piece.file,piece.row,piece.movedyet))
    return(Position(fakewhitepieces,fakeblackpieces,position.castles,position.halfturn,position.enpassant),position[0:-1])

def getpiece(position, square):
    return(position.board[square[0]][square[1]])

def displacement(square1,square2):
    return((square2[0]-square1[0],square2[1]-square1[1]))

def removepiece(position,piece):
    try:
        position.whitepieces.remove(piece)
    except ValueError:
        position.blackpieces.remove(piece)

def computersquaretohumansquare(square):
    global computertohumanfiles
    return(computertohumanfiles[square[0]]+str(square[1]+1))

#############################################################################
######################### VISUAL FUNCTIONS ##################################
#############################################################################
def creerfenetre(res):
    global screen
    screen = pygame.display.set_mode(res)
    pygame.display.set_caption("Chess bot Néoukommm")
    screen.fill(backgroundcolor)
    pygame.display.flip()

def actualiserfenetre(position,except_piece=None,coord_piece = None):
    global width_square, colorlight, colorlighthighlight, colordark, colordarkhighlight, screen, player_view
    afficherdamier(width_square,colorlight,colordark)
    afficherhighlight(width_square, colorlighthighlight, colordarkhighlight)
    afficherpieces(position,width_square,player_view,except_piece,coord_piece)
    affichercoups()
    pygame.display.flip()

def affichercoups():
    global moves_notation, arial_font,screen
    for (index,move) in enumerate(moves_notation):
        text_move = arial_font.render(f"{move}", True, (0,0,0))
        number_move = arial_font.render(f"{index//2+1}", True, (0,0,0))
        if index%2 == 0:
            screen.blit(number_move, (border_chessboard_pix,5+20*(index//2)))
        screen.blit(text_move, (border_chessboard_pix+0.5*menu_width_pix*(index%2)+40,5+20*(index//2)))

def afficherpieces(position,width_square,side,except_piece,coord_piece):
    global chosen_pieces_sprite,screen
    for piece in (position.whitepieces + position.blackpieces):
        if except_piece == None or (piece.file,piece.row) != (except_piece.file,except_piece.row):
            (a,b) = piece.position_sprite
            (x,y) = (piece.file if side =='w' else 7-piece.file,piece.row if side == 'b' else 7-piece.row)
            screen.blit(chosen_pieces_sprite,(x*width_square,y*width_square),(a*width_square,b*width_square,width_square,width_square))
    if except_piece != None:
        (a,b) = except_piece.position_sprite
        (x,y) = coord_piece
        screen.blit(chosen_pieces_sprite,(x-(width_square//2),y-(width_square//2)),(a*width_square,b*width_square,width_square,width_square))

def afficherdamier(width_square,colorlight,colordark):
    global screen, backgroundcolor
    screen.fill(backgroundcolor)
    for file in range(8):
        for row in range(8):
            square = pygame.Rect(row*width_square,file*width_square,width_square,width_square)
            if (file+row)%2 == 0:
                pygame.draw.rect(screen,colorlight,square)
            else:
                pygame.draw.rect(screen,colordark,square)

def afficherhighlight(width_square,colorlighthighlight,colordarkhighlight):
    global screen, backgroundcolor, last_move, player_view
    for case in last_move:
        position = case if player_view == 'w' else [7-case[0],7-case[1]]
        square = pygame.Rect(position[0]*width_square,(7-position[1])*width_square,width_square,width_square)
        if (position[0]+7-position[1])%2 == 0:
            pygame.draw.rect(screen,colorlighthighlight,square)
        else:
            pygame.draw.rect(screen,colordarkhighlight,square)

def afficherpromotion(position,piece):
    global width_square,screen
    actualiserfenetre(position)
    grey_rect = pygame.Rect(2*width_square,3.5*width_square,width_square*4,width_square)
    pygame.draw.rect(screen,(200,200,200),grey_rect)
    pygame.display.flip()
    height_sprite = 0 if piece.color == 'w' else 1
    screen.blit(chosen_pieces_sprite,(2*width_square,3.5*width_square),(1*width_square,height_sprite*width_square,4*width_square,width_square))
    pygame.display.flip()

#############################################################################
########################## LEGAL FUNCTIONS ##################################
#############################################################################
def legalmove(position,square1,square2,fake = False):
    color = 'w' if position.halfturn%2 == 0 else 'b'
    fake_pos = movement_piece(copyposition(position),square1,square2,fake = True)
    king = fake_pos.whitepieces[0] if color == 'w' else fake_pos.blackpieces[0]
    if attackedsquare(fake_pos,(king.file,king.row),color):
        return(False)
    else:
        return(True)

def legal_move_piece(position, square1, square2,fake):
    global possible_moves_pieces
    piece1 = position.board[square1[0]][square1[1]]
    disp = displacement(square1,square2)
    maxlength = possible_moves_pieces[piece1.type][1]
    for signe in [1,-1]:
        for length in range(1,maxlength+1):
            signelength = signe*length
            for move in possible_moves_pieces[piece1.type][0]:
                if disp == (move[0]*signelength,move[1]*signelength):
                    result = True
                    for i in range(1,length):
                        if position.board[square1[0]+move[0]*signe*i][square1[1]+move[1]*signe*i]:
                            result = False
                    return(result)
    return(False)

def legal_move_pawn(position,square1,square2,fake):
    global possible_moves_pawn, gamemode
    piece1 = getpiece(position,square1)
    piece2 = getpiece(position,square2)
    disp = displacement(square1,square2)
    pawn_color = piece1.color
    if disp in possible_moves_pawn[pawn_color+'move'] and not piece2:
        if square2[1] == (7 if pawn_color == 'w' else 0) and not fake:
            gamemode = 'gamemode_promotion'
        piece1.movedyet = True
        return(True)
    elif disp in possible_moves_pawn[pawn_color+'firstmove'] and piece1.row == (1 if piece1.color=='w' else 6) and not piece2:
        intermediate_square = (square1[0],square1[1]+(1 if piece1.color == 'w' else -1))
        if not getpiece(position,intermediate_square):
            if not fake:
                position.enpassant = (intermediate_square,position.halfturn)
            piece1.movedyet = True
            return(True)
        else:
            return(False)
    elif disp in possible_moves_pawn[pawn_color+'eat']:
        if piece2 and piece2.color != piece1.color:
            if square2[1] == (7 if pawn_color == 'w' else 0) and not fake:
                gamemode = 'gamemode_promotion'
            piece1.movedyet = True
            return(True)
        elif position.enpassant and (position.enpassant[0] == square2 and position.halfturn == position.enpassant[1]+1):
            lateralsquare = (square2[0],square1[1])
            piecetakenenpassant = getpiece(position,lateralsquare)
            if not fake:
                removepiece(position,piecetakenenpassant)
                position.board[piecetakenenpassant.file][piecetakenenpassant.row] = None
            if square2[1] == (7 if pawn_color == 'w' else 0) and not fake:
                gamemode = 'gamemode_promotion'
            piece1.movedyet = True
            return(True)
        else:
            return(False)
    else:
        return(False)

def legal_move_castle(position, square1, square2, fake):
    global possible_moves_pieces
    piece_king = getpiece(position,square1)
    color_king = piece_king.color
    row_king = piece_king.row
    file_king = piece_king.file
    disp = displacement(square1,square2)########################ADD IF CHECK, CANNOT CASTLE
    if disp in possible_moves_pieces['castle_short'] and position.castles[color_king][0] == 1:
        if attackedsquare(position,(file_king,row_king),color_king):
            return(False)
        square_rook = (7,row_king)
        for file in range(file_king+1,square_rook[0]):
            if getpiece(position,(file,row_king)) or attackedsquare(position,(file,row_king),color_king):
                return(False)
        if not fake:
            piece_rook = getpiece(position,square_rook)
            position.board[square_rook[0]][square_rook[1]] = None
            position.board[file_king+1][row_king] = piece_rook
            piece_rook.file = file_king+1
            position.castles[color_king][0] = 2
            position.castles[color_king][1] = 0
        return(True)
    elif disp in possible_moves_pieces['castle_long'] and position.castles[color_king][1] == 1:
        if attackedsquare(position,(file_king,row_king),color_king):
            return(False)
        square_rook = (0,row_king)
        for file in range(square_rook[0]+1,file_king):
            if getpiece(position,(file,row_king)) or attackedsquare(position,(file,row_king),color_king):
                return(False)
        if not fake:
            piece_rook = getpiece(position,square_rook)
            position.board[square_rook[0]][square_rook[1]] = None
            position.board[file_king-1][row_king] = piece_rook
            piece_rook.file = file_king-1
            position.castles[color_king][0] = 0
            position.castles[color_king][1] = 2
        return(True)
    else:
        return(False)

#############################################################################
########################## OTHER FUNCTIONS ##################################
#############################################################################
"""
def place_pieces(placement, castle = {'w':[1,1],'b':[1,1]},semiturn = 0, enpassant = None):
    global all_pieces_names,actual_position,all_cases
    allpieces ={'w':[],'b':[]}
    for color in ['w','b']:
        for piece_name in all_pieces_names:
            name = color+piece_name
            for file in placement[name][0]:
                for row in placement[name][1]:
                    allpieces[color].append(Piece(color,piece_name,file,row))
    actual_position = Position(allpieces['w'],allpieces['b'],castle,semiturn,enpassant)
"""
def place_pieces(placement, castle = {'w':[1,1],'b':[1,1]},semiturn = 0, enpassant = None):
    global all_pieces_names,actual_position,all_cases
    allpieces ={'w':[],'b':[]}
    for color in ['w','b']:
        for piece_name in all_pieces_names:
            name = color+piece_name
            for square in placement[name]:
                allpieces[color].append(Piece(color,piece_name,square[0],square[1]))
    actual_position = Position(allpieces['w'],allpieces['b'],castle,semiturn,enpassant)

def promote(letter,playmode = 'manual'):
    global gamemode, promotion_showed, last_move, actual_position
    piece = actual_position.board[last_move[1][0]][last_move[1][1]]
    piece.type = letter
    piece.position_sprite = Piece.position_on_sprite[piece.color+piece.type]
    if playmode == 'manual':
        gamemode = 'gamemode_game'
    else:
        gamemode = 'gamemode_random'
    promotion_showed = False
    promotionnotation(letter)

def movement_piece(position,square1,square2,fake = False):
    global gamemode
    position = copyposition(position)
    piece = position.board[square1[0]][square1[1]]
    piece2 = position.board[square2[0]][square2[1]]
    disp = displacement(square1,square2)
    if not fake:
        nameofmove(position,square1,square2)
    if not piece:
        print(f"Problem with the move {square1}->{square2}")
        for ppiece in position.whitepieces + position.blackpieces:
            if (ppiece.file,ppiece.row) == square1:
                print(f"J'ai trouvé une {ppiece.type} en {computersquaretohumansquare(square1)}")
    elif piece.type in ['R','K'] and not fake:
        color_piece = piece.color
        if piece.type == 'K' and (position.castles[color_piece][0] == 1 or position.castles[color_piece][1] == 1):
            if disp in [(2,0),(-2,0)]:
                color = piece.color
                king_row = 0 if color == 'w' else 7
                if disp == (2,0):#short castle
                    rook = position.board[7][king_row]
                    position.board[5][king_row] = rook
                    position.board[7][king_row] = None
                    rook.file,rook.row = (5,king_row)
                else:#long castle
                    rook = position.board[0][king_row]
                    position.board[0][king_row] = rook
                    position.board[3][king_row] = None
                    rook.file,rook.row = (3,king_row)
            else:
                position.castles[color_piece] = [0,0]
        else:#a rook moves
            if piece.file == 0 and position.castles[color_piece][1] == 1:
                position.castles[color_piece][1] = 0
            elif piece.file == 7 and position.castles[color_piece][0] == 1:
                position.castles[color_piece][0] = 0
    elif piece.type == 'p':
        if disp in [(0,2),(0,-2)]:
            if disp == (0,2):
                position.enpassant = ((square1[0],square1[1]+1),position.halfturn)
            else:
                position.enpassant = ((square1[0],square1[1]-1),position.halfturn)
        if disp[0] != 0 and not piece2:
            pieceenpassant = position.board[square2[0]][square1[1]]
            removepiece(position,pieceenpassant)
        if square2[1] == (7 if piece.color == 'w' else 0) and not fake:
            gamemode = 'gamemode_promotion'
    if piece2:
        removepiece(position,piece2)
    position.board[square2[0]][square2[1]] = piece
    position.board[piece.file][piece.row] = None
    piece.file,piece.row = square2[0],square2[1]
    if not fake:
        position.halfturn += 1
        checknotation(position)
    return(position)

#############################################################################
####################### FUNCTIONS IN PROGRESS ###############################
#############################################################################
def all_poss_attacking_1_piece(position,square,type,color):
    global possible_moves_pieces
    possible_moves = []
    if type in ['K', 'Q', 'R', 'B', 'N']:
        typee = type
        for move in possible_moves_pieces[typee][0]:
            for signe in [-1,1]:
                for length in range(1, possible_moves_pieces[typee][1]+1):
                    movee = (move[0]*length*signe,move[1]*length*signe)
                    if square[0]+movee[0] in range(8) and square[1]+movee[1] in range(8):
                        if not position.board[square[0]+movee[0]][square[1]+movee[1]]:
                            possible_moves.append((square[0]+movee[0],square[1]+movee[1]))
                        elif position.board[square[0]+movee[0]][square[1]+movee[1]].color != color:
                            possible_moves.append((square[0]+movee[0],square[1]+movee[1]))
                            break
                        else:
                            break
                    else:
                        break
    else:#It is a pawn
        side = 1 if color == 'w' else -1
        if square[0]-1 in range(8) and square[1]+side in range(8):
            if (getpiece(position,(square[0]-1,square[1]+side)) and getpiece(position,(square[0]-1,square[1]+side)).color == ('b' if color == 'w' else 'w')) or (((square[0]-1,square[1]+side),position.halfturn-1) == position.enpassant):
                possible_moves.append((square[0]-1,square[1]+side))
        if square[0]+1 in range(8) and square[1]+side in range(8):
            if (getpiece(position,(square[0]+1,square[1]+side)) and getpiece(position,(square[0]+1,square[1]+side)).color == ('b' if color == 'w' else 'w')) or (((square[0]+1,square[1]+side),position.halfturn-1) == position.enpassant):
                possible_moves.append((square[0]+1,square[1]+side))
    return(possible_moves)

def all_poss_non_attacking_1_piece(position,square,type,color):
    if type == 'p':
        possible_moves = []
        side = 1 if color == 'w' else -1
        if not getpiece(position,(square[0],square[1]+side)):
            possible_moves.append((square[0],square[1]+side))
            if square[1] == (1 if color == 'w' else 6) and not getpiece(position,(square[0],square[1]+2*side)):
                possible_moves.append((square[0],square[1]+2*side))
        return(possible_moves)
    else:
        return([])

def all_poss_1_piece(position,square,type,color):
    return(all_poss_attacking_1_piece(position,square,type,color)+all_poss_non_attacking_1_piece(position,square,type,color))

def all_poss_castles(position,color):
    row_king = 0 if color == 'w' else 7
    all_poss_moves = []
    if position.castles[color][0] == 1:
        if not getpiece(position,(5,row_king)) and not getpiece(position,(6,row_king)):
            if not attackedsquare(position,(4,row_king),color) and not attackedsquare(position,(5,row_king),color) and not attackedsquare(position,(6,row_king),color):
                all_poss_moves.append([(4,row_king),(6,row_king)])
    if position.castles[color][1] == 1:
        if not getpiece(position,(3,row_king)) and not getpiece(position,(2,row_king)) and not getpiece(position,(1,row_king)):
            if not attackedsquare(position,(4,row_king),color) and not attackedsquare(position,(3,row_king),color) and not attackedsquare(position,(2,row_king),color):
                all_poss_moves.append([(4,row_king),(2,row_king)])
    return(all_poss_moves)

def explorepossiblemoves(position,color):
    all_poss_moves = []
    for piece in (position.whitepieces if color == 'w' else position.blackpieces):
        all_moves_one_piece = all_poss_1_piece(position,[piece.file,piece.row],piece.type,color)
        for move in all_moves_one_piece:
            all_poss_moves.append([(piece.file,piece.row),move])
    return(all_poss_moves+all_poss_castles(position,color))

def explorelegalmoves(position,color):
    all_legal_moves = []
    all_possible_moves = explorepossiblemoves(position,color)
    for move in all_possible_moves:
        if legalmove(position,move[0],move[1],fake = True):
            all_legal_moves.append((move[0],move[1]))
    return(all_legal_moves)

def attackedsquare(position,square,color):
    for letter in ['K', 'Q', 'R', 'B', 'N', 'p']:
        all_attacking_moves = all_poss_attacking_1_piece(position,square,letter,color)
        for square2 in all_attacking_moves:
            if getpiece(position,square2) and getpiece(position,square2).type == letter:
                #print(f"There's a {letter} on {computersquaretohumansquare(square2)}")
                return(True)
    return(False)

def selfcheck(position,square1,square2):
    position_tested = copyposition(position)
    movement_piece(position_tested,square1,square2)
    color_playing = 'w' if position_tested.halfturn%2 == 0 else 'b'
    king = position_tested.whitepieces[0] if color_playing == 'w' else position_tested.blackpieces[0]
    if attackedsquare(position_tested,[king.file,king.row],color_playing):
        return(True)
    else:
        return(False)

def nameofmove(position,square1,square2,fake = False):
    global computertohumanfiles, moves_notation
    piece_type = getpiece(position,square1).type
    if piece_type in ['K', 'Q', 'R', 'B', 'N']:
        color = 'b' if position.halfturn%2 == 0 else 'w'
        moves = all_poss_attacking_1_piece(position,square2,piece_type,color)
        possible_pieces = []
        for move in moves:
            if getpiece(position,(move[0],move[1])) and getpiece(position,(move[0],move[1])).type == piece_type:
                possible_pieces.append(getpiece(position,(move[0],move[1])))
        if len(possible_pieces) == 1:
            text_piece =  piece_type
        elif len(possible_pieces) == 0:
            if square2[0] == 6:
                if not fake:
                    moves_notation.append(f"O-O")
                return("O-O")
            elif square2[0] == 2:
                if not fake:
                    moves_notation.append(f"O-O-O")
                return("O-O-O")
            else:#Should normally never append
                if not fake:
                    moves_notation.append(f"!!{computersquaretohumansquare(square1)}->{computersquaretohumansquare(square2)}!!")
                return(f"!!{computersquaretohumansquare(square1)}->{computersquaretohumansquare(square2)}!!")
        else:#Two or more piece of same type can access the square2
            for piece in possible_pieces:
                print(f"{piece.type}")
            if not fake:
                moves_notation.append(f"{computersquaretohumansquare(square1)}->{computersquaretohumansquare(square2)}")
            return(f"{computersquaretohumansquare(square1)}->{computersquaretohumansquare(square2)}")
        takes_text = 'x' if getpiece(position,square2) else ''
        square2text = computersquaretohumansquare(square2)
        if not fake:
            moves_notation.append(f"{text_piece}{takes_text}{square2text}")
        return(f"{text_piece}{takes_text}{square2text}")
    else:#Pawn movements
        file_square1 = square1[0]
        file_square2 = square2[0]
        if file_square1 == file_square2:
            if not fake:
                moves_notation.append(computersquaretohumansquare(square2))
            return(computersquaretohumansquare(square2))
        else:
            if not fake:
                moves_notation.append(f"{computertohumanfiles[file_square1]}x{computersquaretohumansquare(square2)}")
            return(f"{computertohumanfiles[file_square1]}x{computersquaretohumansquare(square2)}")

def checknotation(position):
    global moves_notation
    texte = moves_notation[-1]
    del moves_notation[-1]
    color_must_play = 'w' if position.halfturn%2 == 0 else 'b'
    if color_must_play == 'w':
        king = position.whitepieces[0]
    else:
        king = position.blackpieces[0]
    if not canplayerplay(position, color_must_play):
        if attackedsquare(position,(king.file,king.row),color_must_play):
            check = '#'
        else:
            check = '=0'
    elif attackedsquare(position,(king.file,king.row),color_must_play):
        check = '+'
    else:
        check = ''
    moves_notation.append(texte+check)

def promotionnotation(letter):
    global moves_notation
    moves_notation[-1] += f"={letter}"

def canplayerplay(position,color):
    if len(explorelegalmoves(position,color)):
        return(True)
    else:
        return(False)

def printexplorelegalmoves(position,color):
    liste = explorelegalmoves(position,color)
    texte = ''
    for elem in liste:
        texte += f'{nameofmove(position,elem[0],elem[1],fake = True)}, '
    print(texte)

def givemetheboardterminal(position):
    global symbol_terminal,player_view
    print('-----------------------------------------')
    for row in (range(8) if player_view == 'b' else range(7,-1,-1)):
        row_texte = '|'
        for file in range(8):
            piece = position.board[(file if player_view == 'w' else 7-file)][row]
            if piece:
                row_texte += f" {symbol_terminal[piece.color+piece.type]}  |"
            else:
                row_texte += "    |"
        print(row_texte)
        print('-----------------------------------------')



#############################################################################
############################# PROGRAM #######################################
#############################################################################
#place_pieces(original_placement)
#place_pieces(test_placement,castle = {'w':[0,0],'b':[0,0]})
#place_pieces(mateNB_placement,castle = {'w':[0,0],'b':[0,0]})
place_pieces(pawn_battle_placement,castle = {'w':[0,0],'b':[0,0]})

creerfenetre(res_screen)
actualiserfenetre(actual_position)

launched = True
#gamemode = 'gamemode_game'
gamemode = 'gamemode_random'
promotion_showed = False 
game_finished = False
color_computer = 'w' #in ['w' ,'b','both']
playerclicked = False
mate_to_stop_computer = False
mouse_pressed = False

legal_moves = explorelegalmoves(actual_position,'w' if actual_position.halfturn%2 == 0 else 'b')
print(f"Number of legal moves are {len(legal_moves)}")
printexplorelegalmoves(actual_position,'w' if actual_position.halfturn%2 == 0 else 'b')

########################
banana_delay = 20 # ms
banana_event = pygame.USEREVENT + 1
pygame.time.set_timer(banana_event, banana_delay)
########################



while launched:
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            launched = False
        if event.type == banana_event:
            if mouse_pressed and piece:
                x,y = pygame.mouse.get_pos()
                actualiserfenetre(actual_position,piece,(x,y))
        if gamemode == 'gamemode_game':
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pressed = True
                square1 = mousepos2square(event.pos)
                if square1[0] in range(8) and square1[1] in range(8):
                    piece = actual_position.board[square1[0]][square1[1]]
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pressed = False
                actualiserfenetre(actual_position)
                square2 = mousepos2square(event.pos)
                if (square1,square2) in legal_moves:
                    actual_position = movement_piece(actual_position,square1,square2)
                    givemetheboardterminal(actual_position)
                    legal_moves = explorelegalmoves(actual_position,'w' if actual_position.halfturn%2 == 0 else 'b')
                    print(f"Number of legal moves are {len(legal_moves)}")
                    printexplorelegalmoves(actual_position,'w' if actual_position.halfturn%2 == 0 else 'b')
                    last_move = [square1,square2]
                    print(f"En passant is {actual_position.enpassant}")
                    actualiserfenetre(actual_position)
                else:
                    print(f"Illegal move {square1}->{square2}")
        elif gamemode == 'gamemode_promotion':
            if not promotion_showed:
                afficherpromotion(actual_position,piece)
                promotion_showed = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                square = mousepos2square((event.pos[0],event.pos[1]-width_square//2))
                print(square)
                if (player_view == 'w' and square in [(2,4),(3,4),(4,4),(5,4)])  or (player_view == 'b' and square in [(5,3),(4,3),(3,3),(2,3)]):
                    if square in [(2,4),(5,3)]:
                        promote('Q')
                    elif square in [(3,4),(4,3)]:
                        promote('R')
                    elif square in [(4,4),(3,3)]:
                        promote('N')
                    else:
                        promote('B')
                    checknotation(actual_position)
                    legal_moves = explorelegalmoves(actual_position,'w' if actual_position.halfturn%2 == 0 else 'b')
                    print(f"Number of legal moves are {len(legal_moves)}")
                    printexplorelegalmoves(actual_position,'w' if actual_position.halfturn%2 == 0 else 'b')
                    actualiserfenetre(actual_position)
        if gamemode == 'gamemode_random':
            if  not mate_to_stop_computer and (actual_position.halfturn%2==0 and (color_computer in ['w','both'])) or (actual_position.halfturn%2==1 and color_computer in ['b','both']):
                actualiserfenetre(actual_position)
                print(f"halfturn is {actual_position.halfturn} and color_computer is {color_computer}")
                legal_moves = explorelegalmoves(actual_position,'w' if actual_position.halfturn%2 == 0 else 'b')
                if len(legal_moves) > 0:
                    chosen_move = random.choice(legal_moves)
                    actual_position = movement_piece(actual_position,chosen_move[0],chosen_move[1])
                    played_piece = actual_position.board[chosen_move[1][0]][chosen_move[1][1]]
                    if played_piece.type == 'p' and ((chosen_move[1][1] == 7 and color_computer in ['w','both']) or (chosen_move[1][1] == 0 and color_computer in ['w','both'])):
                        promote(random.choice(['Q','R','B','N']),playmode = 'random')
                    legal_moves = explorelegalmoves(actual_position,'w' if actual_position.halfturn%2 == 0 else 'b')
                    print(f"Number of legal moves are {len(legal_moves)}")
                    printexplorelegalmoves(actual_position,'w' if actual_position.halfturn%2 == 0 else 'b')
                    last_move = [chosen_move[0],chosen_move[1]]
                    legal_moves = explorelegalmoves(actual_position,'w' if actual_position.halfturn%2 == 0 else 'b')
                    actualiserfenetre(actual_position)
                    if color_computer != 'both':
                        print('Player to play')
                else:
                    mate_to_stop_computer = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pressed = True
                playerclicked = True
                square1 = mousepos2square(event.pos)
                if square1[0] in range(8) and square1[1] in range(8):
                    piece = actual_position.board[square1[0]][square1[1]]
            if event.type == pygame.MOUSEBUTTONUP and playerclicked:
                mouse_pressed = False
                playerclicked = False
                actualiserfenetre(actual_position)
                square2 = mousepos2square(event.pos)
                if (square1,square2) in legal_moves:
                    actual_position = movement_piece(actual_position,square1,square2)
                    legal_moves = explorelegalmoves(actual_position,'w' if actual_position.halfturn%2 == 0 else 'b')
                    print(f"Number of legal moves are {len(legal_moves)}")
                    printexplorelegalmoves(actual_position,'w' if actual_position.halfturn%2 == 0 else 'b')
                    last_move = [square1,square2]
                    print(f"En passant is {actual_position.enpassant}")
                    actualiserfenetre(actual_position)
                    print('Computer to play')
                    
                else:
                    print(f"Illegal move {square1}->{square2}")