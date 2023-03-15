from param import *
import objects as obj
import os
import positions as pos


def creerfenetre(res):
    global screen
    screen = pygame.display.set_mode(res)
    pygame.display.set_caption("Chess bot Néoukommm")
    screen.fill(backgroundcolor)
    pygame.display.flip()

def actualiserfenetre(position,grabed_piece=None,coord_piece = None,mousepos = None,texte1='',texte2=''):
    global width_square, colorlight, colorlighthighlight, colordark, colordarkhighlight, screen, player_view
    afficherdamier(width_square,colorlight,colordark)
    #afficherhighlight(width_square, colorlighthighlight, colordarkhighlight,player_view)
    afficherpieces(position,width_square,player_view,coord_piece,grabed_piece,mousepos)
    affichertexte(texte1,texte2)
    pygame.display.flip()

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

def afficherhighlight(width_square,colorlighthighlight,colordarkhighlight,side):
    global screen, backgroundcolor, last_move
    for case in last_move:
        position = case if side == 'w' else [7-case[0],7-case[1]]
        square = pygame.Rect(position[0]*width_square,(7-position[1])*width_square,width_square,width_square)
        if (position[0]+7-position[1])%2 == 0:
            pygame.draw.rect(screen,colorlighthighlight,square)
        else:
            pygame.draw.rect(screen,colordarkhighlight,square)

def afficherpieces(position,width_square,side,coord_piece,grabed_piece,mousepos):
    global chosen_pieces_sprite,screen
    cursor = [0,0] if side == 'w' else [7*width_square,7*width_square]
    for line in position.board:
        for char in line:
            if char != ' ':
                pieceonsprite = [possprite[char][0]*width_square,possprite[char][1]*width_square,width_square,width_square]
                screen.blit(chosen_pieces_sprite,cursor,pieceonsprite)
            cursor[0] += width_square if side == 'w' else -width_square
        cursor[0] = 0 if side == 'w' else 7*width_square
        cursor[1] += width_square if side == 'w' else -width_square
        if coord_piece != None:
            file,row = (7-coord_piece[1],coord_piece[0]) if side == 'w' else (coord_piece[1],7-coord_piece[0])
            square = pygame.Rect(row*width_square,file*width_square,width_square,width_square)
            if (file+row)%2 == 0:
                pygame.draw.rect(screen,colorlight,square)
            else:
                pygame.draw.rect(screen,colordark,square)
        if mousepos != None:
            pieceonsprite = [possprite[grabed_piece][0]*width_square,possprite[grabed_piece][1]*width_square,width_square,width_square]
            screen.blit(chosen_pieces_sprite,(mousepos[0]-width_square//2,mousepos[1]-width_square//2),pieceonsprite)

def affichertexte(texte1,texte2):
        text_1 = arial_font.render(texte1, True, (0,0,0))
        text_2 = arial_font.render(texte2, True, (0,0,0))
        screen.blit(text_1, (border_chessboard_pix +10,10))
        screen.blit(text_2, (border_chessboard_pix+10,40))

def afficherpromotion(position):
    global width_square,screen
    actualiserfenetre(position)
    grey_rect = pygame.Rect(2*width_square,3.5*width_square,width_square*4,width_square)
    pygame.draw.rect(screen,(200,200,200),grey_rect)
    pygame.display.flip()
    height_sprite = 0 if position.player == 'w' else 1
    screen.blit(chosen_pieces_sprite,(2*width_square,3.5*width_square),(1*width_square,height_sprite*width_square,4*width_square,width_square))
    pygame.display.flip()

def mousepos2square(mousepos):
    global player_view
    return(((mousepos[0]//width_square,7-(mousepos[1]//width_square)) if player_view == 'w' else (7-(mousepos[0]//width_square),mousepos[1]//width_square)))

def hum2comp_movename(position,movetext):
    promotion = False
    while movetext[-1] in ['+','#','=','!','?']:
        movetext = movetext[:-1]
    if movetext == 'O-O':
        move = ((4,0),(6,0)) if position.player == 'w' else ((4,7),(6,7))
        return(move)
    elif movetext == 'O-O-O':
        move = ((4,0),(2,0)) if position.player == 'w' else ((4,7),(2,7))
        return(move)
    if movetext[-1] in ['Q','R','B','N']:
        promotion = True
        promotion_letter = movetext[-1]
        movetext = movetext[-2]
    if not promotion:
        arriving_coord = filerow_to_coord(movetext[-2:])
    if promotion:
        c = filerow_to_coord(movetext[-2:])
        arriving_coord = (c[0],c[1],promotion_letter)
    movetext = movetext[:-2]
    if movetext == '':
        starting_coord = (arriving_coord[0],arriving_coord[1]-(1 if position.player == 'w' else -1))
        if position.board[7-starting_coord[1]][starting_coord[0]].upper() == 'P':
            return(starting_coord,arriving_coord)
        else:
            return((starting_coord[0],starting_coord[1]-(1 if position.player == 'w' else -1)),arriving_coord)
    if movetext[-1] == 'x':
        movetext = movetext[:-1]
    if movetext[0].islower():
        startingfile = file_to_coord(movetext[0])
        starting_coord = (startingfile,arriving_coord[1]-(1 if position.player == 'w' else -1))
        return((starting_coord,arriving_coord))
    else:
        possible_piece_position = []
        piece = movetext[0]
        for sign in [-1,1]:
            for vector in possible_moves_pieces[piece][0]:
                for length in range(1,possible_moves_pieces[piece][1]+1):
                    newsquare = (arriving_coord[0]+sign*length*vector[0],arriving_coord[1]+sign*length*vector[1])
                    if possible_square(newsquare):
                        arriving_letter = position.board[7-newsquare[1]][newsquare[0]]
                        if arriving_letter.isalpha():
                            if arriving_letter.upper() == piece and ((arriving_letter.isupper() and position.player == 'w') or (arriving_letter.islower() and position.player == 'b')):
                                possible_piece_position.append(newsquare)
                                break
                            else:
                                break
                    else:
                        break
        if len(possible_piece_position) == 1:
            starting_coord = possible_piece_position[0]
            return((starting_coord,arriving_coord))
        else:
            confusion = movetext[1:]
            human_possible_piece_position = [coord_to_filerow(c) for c in possible_piece_position]
            for i in range(len(possible_piece_position)):
                if confusion in human_possible_piece_position[i]:
                    starting_coord = possible_piece_position[i]
            return((starting_coord,arriving_coord))



def coord_to_filerow(coord):
    return(chr(coord[0]+97)+str(coord[1]+1))

def file_to_coord(file):
    return(ord(file)-97)

def filerow_to_coord(filerow):
    coord = (file_to_coord(filerow[0]),int(filerow[1])-1)
    return(coord)


def board2fen(board,player,castle,enpassant,fiftymoves,movenum):
    fen = ""
    spacestreak = 0
    for line in board:
        for char in line:
            if char == ' ':
                spacestreak += 1
            else:
                if spacestreak:
                    fen += str(spacestreak)
                    spacestreak = 0
                fen += char
        if spacestreak:
            fen += str(spacestreak)
            spacestreak = 0
        fen += "/"
    fen = fen[0:-1]#to erase last "/"
    fen += f" {player} {castle} {enpassant} {fiftymoves} {movenum}"
    return(fen)

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
        play_pieces,opp_pieces = get_all_pieces(position)
    else:
        opp_pieces,play_pieces = get_all_pieces(position)
    for piece_namepos in play_pieces:
        piece_name = piece_namepos[0].upper()
        piece_pos = piece_namepos[1]
        if piece_name != 'P':#Moves of non-pawn pieces
            for sign in [1,-1]:
                for vector in possible_moves_pieces[piece_name][0]:
                    for length in range(1,possible_moves_pieces[piece_name][1]+1):
                        newpos = (piece_pos[0] + sign*length*vector[0],piece_pos[1] + sign*length*vector[1])
                        if possible_square(newpos):#still is on the board
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

def possible_square(sq):
    if sq[0]>=0 and sq[0]<=7 and sq[1]>= 0 and sq[1]<=7:
        return(True)
    else:
        return(False)

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
    position = copyposition(positionn)
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
            newenpassant = coord_to_filerow((sq1[0],(sq1[1]+sq2[1])//2))
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
    newfen = board2fen(board,'b' if position.player == 'w' else 'w',newcastle if newcastle else '-',newenpassant,str(newfiftymoves),str(int(position.movenum) + (1 if position.player == 'b' else 0)))
    newpos = obj.Position(newfen,[c for c in position.threefoldlist] if newfiftymoves else [])
    return(newpos)

def copyposition(position):
    return(obj.Position(position.fen,position.threefoldlist[0:-1]))

def get_all_pieces(position):
    #Return two 2-tuples list composed by the name of the piece and its position
    all_w_pieces = []
    all_b_pieces = []
    pos = [-1,7]
    for i in range(len(position.posfen)):
        char = position.posfen[i]
        if char.isalpha():
            pos = [pos[0]+1,pos[1]]
            if char.islower():
                all_b_pieces.append((char,tuple(pos)))
            else:
                all_w_pieces.append((char,tuple(pos)))
        elif char == "/":
            pos = [-1,pos[1]-1]
        else:
            pos = [pos[0]+int(char),pos[1]]
    return(all_w_pieces,all_b_pieces)

def square_is_attacked(position,square,color_attacked):
    for letter in ['K','Q','R','B','N']:
        for sign in [-1,1]:
            for vector in possible_moves_pieces[letter][0]:
                for length in range(1,possible_moves_pieces[letter][1]+1):
                    newsquare = (square[0]+sign*length*vector[0],square[1]+sign*length*vector[1])
                    if possible_square(newsquare):
                        arriving_letter = position.board[7-newsquare[1]][newsquare[0]]
                        if arriving_letter.isalpha():
                            if arriving_letter == (letter.lower() if color_attacked == 'w' else letter):
                                return(True)
                            else:
                                break
                    else:
                        break
    newpos = (square[0]-1,square[1]+(1 if color_attacked == 'w' else -1))
    if possible_square(newpos) and (position.board[7-newpos[1]][newpos[0]] == ('p' if color_attacked == 'w' else 'P')):
        return(True)
    newpos = (square[0]+1,square[1]+(1 if color_attacked == 'w' else -1))
    if possible_square(newpos) and (position.board[7-newpos[1]][newpos[0]] == ('p' if color_attacked == 'w' else 'P')):
        return(True)
    return(False)


def get_all_lines_from_pgn(pgnpath):
    chapters = get_all_chapters_from_pgn(pgnpath)
    all_lines = []
    for chapter in chapters:
        all_lines += get_all_lines_from_chapter(chapter)
    return(all_lines)

def get_all_chapters_from_pgn(pgnpath):
    """
    Take as an input the path of the pgn file, and as an output give a list of lists [fen,line_from_fen]
    """
    print(f"Importing pgn from {pgnpath}")
    chapters = []
    with open(pgnpath,'r') as pgnfile:
        line_read_in_chapter = False
        fen_of_chapter = pos.starting#starting fen
        for line in pgnfile.readlines():
            if not line[0] in ['[','\n']:
                line_read_in_chapter = True
                chapters.append([fen_of_chapter,line])
            elif line[:5] == "[FEN ":
                fen_of_chapter = line.split('"')[1]
            if line[0] == '\n' and line_read_in_chapter:
                line_read_in_chapter = False
                fen_of_chapter = pos.starting
    return(chapters)

def get_all_lines_from_chapter(chapter):
    """
    take as an input a list of lists [fen,line_from_fen] and exits a list of all lines
    """
    chapter[1] = eliminate_useless_in_long_line(chapter[1])
    long_line = chapter[1]
    all_lines = get_all_lines_from_clean_line(chapter[0],long_line)
    return(all_lines)

def get_all_lines_from_clean_line(starting_fen,long_line):
    all_lines = []
    long_line_list = long_line.split()
    while long_line_list:
        last_opening_parenthesis = 0
        for i in range(len(long_line_list)):
            if long_line_list[i][0] == '(':
                last_opening_parenthesis = i
            elif long_line_list[i][-1] == ')':
                long_line_list[i] = long_line_list[i][:-1]#remove closing parenthesis
                line_found_list = long_line_list[:i+1]
                del line_found_list[last_opening_parenthesis-1]
                line_found = ' '.join(line_found_list)
                line_without_parenthesis = ''.join(line_found.split('('))#)
                all_lines.append([starting_fen,line_without_parenthesis])
                long_line_list = long_line_list[:last_opening_parenthesis]+ long_line_list[i+1:]
                break
        if last_opening_parenthesis == 0:
            all_lines.append([starting_fen,' '.join(long_line_list)])
            long_line_list = []
    return(all_lines)

def eliminate_useless_in_long_line(long_line):
    """
    eliminates human comments, as well as '.' and numbers of moves
    """
    for i in range(long_line.count('{')):
            for j in range(len(long_line)):
                if long_line[j] == '{':
                    indexparopen = j
                elif long_line[j] == '}':
                    long_line = long_line[:indexparopen]+long_line[j+1:]
                    break
    long_line_sub = long_line.split("(")#It is not mandatorya to take ) into account for now
    for i in range(len(long_line_sub)):
        long_line_sub[i] = ' '.join([texte for texte in long_line_sub[i].split() if texte[0].isalpha()])#Suppress all non moves numbers
    long_line = ' ('.join(long_line_sub)#)
    return(long_line)

"""

def get_all_lines_from_pgn(pgnpath):
    print(f"Importing pgn from {pgnpath}")
    with open(pgnpath) as f:
        fullpgn = f.readlines()
    pgn = []
    for line in fullpgn:
        if line != '\n' and line[0] != '[':
            pgn.append(line)
    all_lines = []
    for long_line in pgn:
        for i in range(long_line.count('{')):
            for j in range(len(long_line)):
                if long_line[j] == '{':
                    indexparopen = j
                elif long_line[j] == '}':
                    long_line = long_line[:indexparopen]+long_line[j+1:]
                    break
        while long_line != '':
            last_oppening_parenthesis = 0
            last_closing_parenthesis = 0
            prems = True
            for i,char in enumerate(long_line):
                if char == '*' and prems:
                    all_lines.append(clean_line(long_line[:-3]))
                    long_line = ''
                if char == '(':
                    last_oppening_parenthesis = i
                if char == ')' and prems:
                    prems = False
                    last_closing_parenthesis = i
                    raw_line = long_line[:i]
                    all_lines.append(clean_line(raw_line))
                    if last_closing_parenthesis != len(long_line)-1:
                        long_line = long_line[0:last_oppening_parenthesis]+long_line[last_closing_parenthesis+1:]
                    else:
                        long_line = long_line[0:last_oppening_parenthesis]
                    last_oppening_parenthesis = 0
                    last_closing_parenthesis = 0
    return(all_lines)

"""

def clean_line(rawline):
    rawline = rawline.replace('.','')
    clean_list = rawline.split()
    indexes_of_par = []
    for i,elem in enumerate(clean_list):
        if elem[0]== '(':
            indexes_of_par.insert(0,i-1)
            indexes_of_par.insert(0,i)
    for index in indexes_of_par:
        del clean_list[index]
    cleaner_list = []
    for elem in clean_list:
        if not elem.isdigit():
            cleaner_list.append(elem)
    clean_line = ' '.join(cleaner_list)
    return(clean_line)

def get_all_lines_from_folder(path_of_opening,subfolder='p'):
    if subfolder == 'b':
        path = path_of_opening+'\Black'
    if subfolder == 'w':
        path = path_of_opening+'\White'
    if subfolder == 'p':
        path = path_of_opening+'\Problems'
    files = os.listdir(path)
    all_lines = []
    all_lines_one_file = []
    index_line = 1
    for file in files:
        if os.path.isfile(os.path.join(path, file)):
            all_lines_one_file = get_all_lines_from_pgn(os.path.join(path, file))
            §print(f"Lines {index_line} to {index_line+len(all_lines_one_file)-1}")
            index_line += len(all_lines_one_file)
            all_lines = all_lines + all_lines_one_file
    return(all_lines)
