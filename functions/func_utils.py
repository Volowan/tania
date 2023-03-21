"""
This file contains utilitary functions
"""
import os
import objects.objects as obj
from params.params import *

def dist(x,y):
    return((x**2+y**2)**0.5)

def mousepos2square(mousepos,player_view):
    return(((mousepos[0]//width_square,7-(mousepos[1]//width_square)) if player_view == 'w' else (7-(mousepos[0]//width_square),mousepos[1]//width_square)))

def middlesquare2pos(square,player_view):
    return(((square[0]+0.5)*width_square,((7-square[1])+0.5)*width_square) if player_view == 'w' else ((7-square[0]+0.5)*width_square,((square[1])+0.5)*width_square))

def coord_to_filerow(coord):
    return(chr(coord[0]+97)+str(coord[1]+1))

def file_to_coord(file):
    return(ord(file)-97)

def filerow_to_coord(filerow):
    coord = (file_to_coord(filerow[0]),int(filerow[1])-1)
    return(coord)

def possible_square(sq):
    if sq[0] in range(8) and sq[1]in range(8):
        return(True)
    else:
        return(False)

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

def get_all_lines_from_pgn(pgnpath,color):
    chapters = get_all_chapters_from_pgn(pgnpath)
    all_lines = []
    for chapter in chapters:
        all_lines += get_all_lines_from_chapter(chapter,color)
    return(all_lines)

def get_all_chapters_from_pgn(pgnpath):
    """
    Take as an input the path of the pgn file, and as an output give a list of lists [fen,line_from_fen]
    """
    print(f"Importing pgn from {pgnpath}")
    chapters = []
    with open(pgnpath,'r') as pgnfile:
        line_read_in_chapter = False
        fen_of_chapter = starting_fen
        for line in pgnfile.readlines():
            if not line[0] in ['[','\n']:
                line_read_in_chapter = True
                chapters.append([fen_of_chapter,line])
            elif line[:5] == "[FEN ":
                fen_of_chapter = line.split('"')[1]
            if line[0] == '\n' and line_read_in_chapter:
                line_read_in_chapter = False
                fen_of_chapter = starting_fen
    return(chapters)

def get_all_lines_from_chapter(chapter,color):
    """
    take as an input a list of lists [fen,line_from_fen] and exits a list of all lines
    """
    chapter[1] = eliminate_useless_in_long_line(chapter[1])
    long_line = chapter[1]
    all_lines = get_all_lines_from_clean_line(chapter[0],long_line,color)
    return(all_lines)
"""
def get_all_lines_from_clean_line(starting_fen,long_line,color):
    all_lines = []
    long_line_list = long_line.split()
    print(f"long line list = {long_line_list}")
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
                print(f"Add: {line_without_parenthesis}")
                all_lines.append([starting_fen,line_without_parenthesis,color])
                long_line_list = long_line_list[:last_opening_parenthesis]+ long_line_list[i+1:]
                break
        if last_opening_parenthesis == 0:
            print(f"Add: {' '.join(long_line_list)}")
            all_lines.append([starting_fen,' '.join(long_line_list),color])
            long_line_list = []
    return(all_lines)
"""
def get_all_lines_from_clean_line(starting_fen,long_line,color):
    all_lines = []
    current_line = []
    long_line_list = long_line.split()
    print(f"long line list = {long_line_list}")
    while long_line_list:
        last_opening_parenthesis = 0
        for index_move,move in enumerate(long_line_list):
            if move[0] == '(':
                last_opening_parenthesis = index_move
                del current_line[-1]
                current_line.append(move[1:])#to remove oppening parenthesis
            elif move[-1] == ')':
                current_line.append(move[:-1])#to remove closing parenthesis
                all_lines.append([starting_fen,' '.join(current_line),color])
                #print(' '.join(current_line))
                #print(long_line_list)
                long_line_list = long_line_list[:last_opening_parenthesis]+long_line_list[index_move+1:]
                current_line = []
                break
            else:
                current_line.append(move)
        if last_opening_parenthesis == 0:
            all_lines.append([starting_fen,' '.join(current_line),color])
            long_line_list = ''
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
                    print(f"Eliminate '{long_line[indexparopen:j+1]}', but one char after is {long_line[j+1]}")
                    long_line = long_line[:indexparopen]+long_line[j+1:]
                    break
    long_line_sub = long_line.split("(")#It is not mandatory to take ) into account for now
    for i in range(len(long_line_sub)):
        long_line_sub[i] = ' '.join([texte for texte in long_line_sub[i].split() if (texte[0].isalpha() or texte==')')])#Suppress all non moves numbers
    long_line = ' ('.join(long_line_sub)#)
    print(long_line)
    return(long_line)

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

def get_all_lines_from_folder(path_of_opening,color_tested):
    all_lines=[]
    if 'b' in color_tested:
        path = os.path.join(path_of_opening,'black_openings')
        files = os.listdir(path)
        all_lines_one_file = []
        index_line = 1
        for file in files:
            if os.path.isfile(os.path.join(path, file)):
                all_lines_one_file = get_all_lines_from_pgn(os.path.join(path, file),'b')
                print(f"Lines {index_line} to {index_line+len(all_lines_one_file)-1}")
                index_line += len(all_lines_one_file)
                all_lines = all_lines + all_lines_one_file
    if 'w' in color_tested:
        path = os.path.join(path_of_opening,'white_openings')
        files = os.listdir(path)
        all_lines_one_file = []
        index_line = 1
        for file in files:
            if os.path.isfile(os.path.join(path, file)):
                all_lines_one_file = get_all_lines_from_pgn(os.path.join(path, file),'w')
                print(f"Lines {index_line} to {index_line+len(all_lines_one_file)-1}")
                index_line += len(all_lines_one_file)
                all_lines = all_lines + all_lines_one_file
    elif color_tested == 'o':
        path = os.path.join(path_of_opening,'other_positions')
    return(all_lines)


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
        movetext = movetext[:-2]
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
            print(f"on line 249, movetext = {movetext}")
            confusion = movetext[1:]
            human_possible_piece_position = [coord_to_filerow(c) for c in possible_piece_position]
            for i in range(len(possible_piece_position)):
                if confusion in human_possible_piece_position[i]:
                    starting_coord = possible_piece_position[i]
            return((starting_coord,arriving_coord))