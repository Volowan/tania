import functions.func_utils as f_utl
from params.params import *
import objects.objects as obj

def all_legal_moves(position):
    global possible_moves_pieces
    all_moves = []
    if position.fiftymoves >= 100:
        print("Draw by the 50 moves rule")
        position.result_for_white = 0.5
        return([])
    if position.threefoldlist.count(position.posfen) >= 3:
        print("Draw by 3-fold repetition")
        position.result_for_white = 0.5
        return([])
    if (position.whitepieces in ['KB','BK','KN','NK','K'] and position.blackpieces in ['kb','bk','kn','nk','k']) or (position.whitepieces in ['KNN','NKN','NNK'] and position.blackpieces == 'k') or (position.blackpieces in ['knn','nkn','nnk'] and position.whitepieces == 'K'):
        position.result_for_white = 0.5
        print("Draw by insufficient material")
        return([])
    if position.player == 'w':
        play_pieces,opp_pieces = f_utl.get_all_pieces(position)
    else:
        opp_pieces,play_pieces = f_utl.get_all_pieces(position)
    for piece_namepos in play_pieces:
        piece_name = piece_namepos[0].upper()
        piece_pos = piece_namepos[1]
        if piece_name != 'P':#Moves of non-pawn pieces
            for sign in [1,-1]:
                for vector in possible_moves_pieces[piece_name][0]:
                    for length in range(1,possible_moves_pieces[piece_name][1]+1):
                        newpos = (piece_pos[0] + sign*length*vector[0],piece_pos[1] + sign*length*vector[1])
                        if f_utl.possible_square(newpos):#still is on the board
                            arriving_letter = position.board[7-newpos[1]][newpos[0]]
                            if arriving_letter.isalpha():
                                if (arriving_letter.isupper() and position.player == 'w') or (arriving_letter.islower() and position.player == 'b'):
                                    break
                                else:
                                    all_moves.append((piece_pos,newpos))
                                    break
                            else:
                                all_moves.append((piece_pos,newpos))
                        else:
                            break
        if piece_name == 'P':#Pawn moves
            if position.board[7-piece_pos[1]+(-1 if position.player == 'w' else +1)][piece_pos[0]] == ' ':
                if piece_pos[1] != (6 if position.player == 'w' else 1):
                    all_moves.append(((piece_pos),(piece_pos[0],piece_pos[1]+(1 if position.player == 'w' else -1))))
                    if piece_pos[1]==(1 if position.player=='w' else 6) and position.board[7-piece_pos[1]+(-2 if position.player == 'w' else 2)][piece_pos[0]] == ' ':
                        all_moves.append(((piece_pos),(piece_pos[0],piece_pos[1]+(2 if position.player == 'w' else -2))))
                else:
                    all_moves.append(((piece_pos),(piece_pos[0],piece_pos[1]+(1 if position.player == 'w' else -1),'Q' if position.player == 'w' else 'q')))
                    all_moves.append(((piece_pos),(piece_pos[0],piece_pos[1]+(1 if position.player == 'w' else -1),'R' if position.player == 'w' else 'r')))
                    all_moves.append(((piece_pos),(piece_pos[0],piece_pos[1]+(1 if position.player == 'w' else -1),'B' if position.player == 'w' else 'b')))
                    all_moves.append(((piece_pos),(piece_pos[0],piece_pos[1]+(1 if position.player == 'w' else -1),'N' if position.player == 'w' else 'n')))
            for sign in [1,-1]:
                if (piece_pos[0]+sign) in range(8):
                    arriving_letter = position.board[7-piece_pos[1]+(-1 if position.player == 'w' else 1)][piece_pos[0]+sign]
                    if (arriving_letter.isalpha() and ((arriving_letter.islower() and position.player == 'w')or (arriving_letter.isupper() and position.player == 'b'))):
                        if piece_pos[1] != (6 if position.player == 'w' else 1):
                            all_moves.append(((piece_pos),(piece_pos[0]+sign,piece_pos[1]+(1 if position.player == 'w' else -1))))
                        else:
                            all_moves.append(((piece_pos),(piece_pos[0]+sign,piece_pos[1]+(1 if position.player == 'w' else -1),'Q' if position.player == 'w' else 'q')))
                            print(f"{((piece_pos),(piece_pos[0]+sign,piece_pos[1]+(1 if position.player == 'w' else -1)),'Q' if position.player == 'w' else 'q')}")
                            all_moves.append(((piece_pos),(piece_pos[0]+sign,piece_pos[1]+(1 if position.player == 'w' else -1),'R' if position.player == 'w' else 'r')))
                            all_moves.append(((piece_pos),(piece_pos[0]+sign,piece_pos[1]+(1 if position.player == 'w' else -1),'B' if position.player == 'w' else 'b')))
                            all_moves.append(((piece_pos),(piece_pos[0]+sign,piece_pos[1]+(1 if position.player == 'w' else -1),'N' if position.player == 'w' else 'n')))
                    elif (piece_pos[0]+sign,piece_pos[1]+(1 if position.player == 'w' else -1)) == position.enpassantcoord:
                        all_moves.append(((piece_pos),(piece_pos[0]+sign,piece_pos[1]+(1 if position.player == 'w' else -1))))
    #CASTLES
    if ('K' if position.player == 'w' else 'k') in position.castle:
        if castle_permitted(position,position.player,'K'):
            kingrow = 0 if position.player == 'w' else 7
            all_moves.append(((4,kingrow),(6,kingrow)))
    if ('Q' if position.player == 'w' else 'q') in position.castle:
        if castle_permitted(position,position.player,'Q'):
            kingrow = 0 if position.player == 'w' else 7
            all_moves.append(((4,kingrow),(2,kingrow)))
    #CHECKING IF CORRECT
    all_moves_after_check=[]
    for move in all_moves:
        init_pos = position
        testpos = make_move(init_pos,move)
        if not square_is_attacked(testpos,testpos.Ksq if init_pos.player == 'w' else testpos.ksq,init_pos.player):
            all_moves_after_check.append(move)
    if len(all_moves_after_check)==0:
        if square_is_attacked(position,position.Ksq if position.player == 'w' else position.ksq,position.player):
            position.result_for_white = 1 if position.player == 'b' else 0
            print(f"{'White' if position.player == 'w' else 'Black'} player got checkmated")
        else:
            position.result_for_white = 0.5
            print("Draw by stalemate")
    return(all_moves_after_check)


def castle_permitted(position,color,side):
    kingrow = 0 if color == 'w' else 7
    if side == 'K':
        for column in [4,5]:#arriving square has not to be checked as it will be anyway later
            if square_is_attacked(position,(column,kingrow),color):
                return(False)
        for column in [5,6]:
            if position.board[7-kingrow][column] != ' ':
                return(False)
        return(True)
    elif side == 'Q':
        for column in [4,3]:#same here
            if square_is_attacked(position,(column,kingrow),color):
                return(False)
        for column in [3,2,1]:
            if position.board[7-kingrow][column] != ' ':
                return(False)
        return(True)


def make_move(positionn,move):
    position = f_utl.copyposition(positionn)
    castlelist = [c for c in position.castle]
    enpassant_happened = False
    sq1,sq2 = move
    board = position.board
    piece = board[7-sq1[1]][sq1[0]]
    if piece.upper() == 'K':
        if position.player == 'w':
            castlelist = [c for c in castlelist if c.islower()]
        else:
            castlelist = [c for c in castlelist if c.isupper()]
        if sq2[0]-sq1[0] == 2:#King side castle
            if position.player == 'w':
                #print(f"x1 Modification of {position.board[7]} in {position.board[7][:5]+'R  '}")
                position.board[7] = position.board[7][:5]+'R  '
            else:
                #print(f"x2 Modification of {position.board[0]} in {position.board[0][:5]+'r  '}")
                position.board[0] = position.board[0][:5]+'r  '
        elif sq1[0]-sq2[0] == 2:#Queen side castle
            if position.player == 'w':
                #print(f"x3 Modification of {position.board[7]} in {'   R'+position.board[7][5:]}")
                position.board[7] ='   R'+position.board[7][4:]
            else:
                #print(f"x4 Modification of {position.board[0]} in {'   r'+position.board[7][5:]}")
                position.board[0] ='   r'+position.board[0][4:]
    if sq2 in [(0,0),(0,7),(7,7),(7,0)]:
        try:
            castlelist.remove(init_rook_castle_correspondance[sq2])
        except:
            pass
    if piece.upper() == 'R':
        if sq1 in [(0,0),(0,7),(7,7),(7,0)]:
            try:
                castlelist.remove(init_rook_castle_correspondance[sq1])
            except:
                pass
    arrivingletter = board[7-sq2[1]][sq2[0]]
    newenpassant = '-'
    newfiftymoves = int(position.fiftymoves) + 1
    if piece.upper() == 'P':
        newfiftymoves = 0
        if abs(sq1[1]-sq2[1]) == 2:
            newenpassant = f_utl.coord_to_filerow((sq1[0],(sq1[1]+sq2[1])//2))
        elif sq2 == position.enpassantcoord:
            enpassant_happened = True
        elif sq2[1] in [0,7]:
            piece = sq2[2]
    elif arrivingletter.isalpha():
        newfiftymoves = 0
    board = position.board
    board[7-sq1[1]] = board[7-sq1[1]][0:sq1[0]]+' '+board[7-sq1[1]][sq1[0]+1:8]
    board[7-sq2[1]] = board[7-sq2[1]][0:sq2[0]]+piece+board[7-sq2[1]][sq2[0]+1:8]
    if enpassant_happened:
        eaten_piece_square = (sq2[0],sq1[1])
        board[7-eaten_piece_square[1]] = board[7-eaten_piece_square[1]][0:eaten_piece_square[0]]+' '+board[7-eaten_piece_square[1]][eaten_piece_square[0]+1:8]
    newcastle = ''.join(castlelist)
    newfen = f_utl.board2fen(board,'b' if position.player == 'w' else 'w',newcastle if newcastle else '-',newenpassant,str(newfiftymoves),str(int(position.movenum) + (1 if position.player == 'b' else 0)))
    newpos = obj.Position(newfen,[c for c in position.threefoldlist] if newfiftymoves else [])
    return(newpos)

def square_is_attacked(position,square,color_attacked):
    for letter in ['K','Q','R','B','N']:
        for sign in [-1,1]:
            for vector in possible_moves_pieces[letter][0]:
                for length in range(1,possible_moves_pieces[letter][1]+1):
                    newsquare = (square[0]+sign*length*vector[0],square[1]+sign*length*vector[1])
                    if f_utl.possible_square(newsquare):
                        arriving_letter = position.board[7-newsquare[1]][newsquare[0]]
                        if arriving_letter.isalpha():
                            if arriving_letter == (letter.lower() if color_attacked == 'w' else letter):
                                return(True)
                            else:
                                break
                    else:
                        break
    newpos = (square[0]-1,square[1]+(1 if color_attacked == 'w' else -1))
    if f_utl.possible_square(newpos) and (position.board[7-newpos[1]][newpos[0]] == ('p' if color_attacked == 'w' else 'P')):
        return(True)
    newpos = (square[0]+1,square[1]+(1 if color_attacked == 'w' else -1))
    if f_utl.possible_square(newpos) and (position.board[7-newpos[1]][newpos[0]] == ('p' if color_attacked == 'w' else 'P')):
        return(True)
    return(False)