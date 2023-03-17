import time
import os
import random

from objects.objects import Position
from params.params import *

import functions.func_chess as f_chs
import functions.func_utils as f_utl
import functions.func_visual as f_vis

tested_color = 'wb'#'w','b' or 'wb'
player_view = tested_color[0]
init_position = Position(starting_fen)
#curr_position = f_utl.copyposition(init_position)


f_vis.creerfenetre(res_screen)


"""
print(f"Number of legal moves are {len(legal_moves)}")
human_legal_moves = []
for move in legal_moves:
human_legal_moves.append((f_utl.coord_to_filerow(move[0]),f_utl.coord_to_filerow(move[1])))
"""
last_move = None

training_finished = False
all_training_lines = f_utl.get_all_lines_from_folder(os.path.join('.',os.path.join('data','pgn')),tested_color)
print(all_training_lines)
all_training_lines_redo = []
all_lines_length = len(all_training_lines)
index_line_questionned = 0
random.shuffle(all_training_lines)
asked_line = all_training_lines[index_line_questionned][1]
curr_position = Position(all_training_lines[index_line_questionned][0])
legal_moves = f_chs.all_legal_moves(curr_position)
player_view = all_training_lines[index_line_questionned][2]
f_vis.actualiserfenetre(curr_position,player_view,last_move=last_move)
asked_line_list = asked_line.split()
print(f"Asking line {index_line_questionned}/{all_lines_length}")
correct_move = f_utl.hum2comp_movename(curr_position,asked_line_list[0])
#print(f"correct move is {correct_move}")
semi_move_number = 0

if curr_position.player != all_training_lines[index_line_questionned][2]:
    correct_move = f_utl.hum2comp_movename(curr_position,asked_line_list[semi_move_number])
    last_move = correct_move
    f_vis.make_move_animation(curr_position,player_view,correct_move[0],correct_move[1],curr_position.board[7-correct_move[0][1]][correct_move[0][0]])
    curr_position = f_chs.make_move(curr_position,correct_move)
    legal_moves = f_chs.all_legal_moves(curr_position)
    f_vis.actualiserfenetre(curr_position,player_view,last_move=last_move)
    semi_move_number += 1
    correct_move = f_utl.hum2comp_movename(curr_position,asked_line_list[semi_move_number])


########################
banana_delay = 10 # ms
banana_event = pygame.USEREVENT + 1
pygame.time.set_timer(banana_event, banana_delay)
########################


while launched:
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            launched = False
        if event.type == banana_event:
            if mouse_pressed and grabed_piece != ' ':
                x,y = pygame.mouse.get_pos()
                f_vis.actualiserfenetre(curr_position,player_view,coord_piece = sq1,grabed_piece = grabed_piece,mousepos = (x,y),last_move=last_move)
        if event.type == pygame.MOUSEBUTTONDOWN:
            sq1 = f_utl.mousepos2square(event.pos,player_view)
            if f_utl.possible_square(sq1):
                grabed_piece = curr_position.board[7-sq1[1]][sq1[0]]
                mouse_pressed = True
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pressed = False
            f_vis.actualiserfenetre(curr_position,player_view,last_move=last_move)
            sq2 = f_utl.mousepos2square(event.pos,player_view)
            #print(f"move done is {(sq1,sq2)}")
            if (sq1,sq2) == correct_move:
                last_move = (sq1,sq2)
                curr_position = f_chs.make_move(curr_position,(sq1,sq2))
                f_vis.actualiserfenetre(curr_position,player_view,last_move=last_move)
                semi_move_number += 1
                if len(asked_line_list) == semi_move_number:
                    time.sleep(2)
                    last_move = None
                    index_line_questionned += 1
                    #print(f"len of all_training_lines {len(all_training_lines)} and index {index_line_questionned}")
                    #print(f"training list == training redo : {all_training_lines== all_training_lines_redo }")
                    if len(all_training_lines) == index_line_questionned and (len(all_training_lines_redo)==0 or all_training_lines == all_training_lines_redo):
                        print("Training finished")
                        launched = False
                        time.sleep(5)
                        continue
                    elif len(all_training_lines) == index_line_questionned and all_training_lines != all_training_lines_redo:
                        index_line_questionned = 0
                        all_training_lines = all_training_lines_redo
                    semi_move_number = 0
                    asked_line_list = all_training_lines[index_line_questionned][1].split()
                    player_view = all_training_lines[index_line_questionned][2]
                    curr_position = f_utl.copyposition(Position(all_training_lines[index_line_questionned][0]))
                    f_vis.actualiserfenetre(curr_position,all_training_lines[index_line_questionned][2])
                    correct_move = f_utl.hum2comp_movename(curr_position,asked_line_list[0])
                    if curr_position.player != all_training_lines[index_line_questionned][2]:
                        time.sleep(0.5)
                        correct_move = f_utl.hum2comp_movename(curr_position,asked_line_list[semi_move_number])
                        last_move = correct_move
                        f_vis.make_move_animation(curr_position,player_view,correct_move[0],correct_move[1],curr_position.board[7-correct_move[0][1]][correct_move[0][0]])
                        curr_position = f_chs.make_move(curr_position,correct_move)
                        legal_moves = f_chs.all_legal_moves(curr_position)
                        f_vis.actualiserfenetre(curr_position,player_view,last_move=last_move)
                        semi_move_number += 1
                        correct_move = f_utl.hum2comp_movename(curr_position,asked_line_list[semi_move_number])
                    #print(f"Correct move is {correct_move}")
                    f_vis.actualiserfenetre(curr_position,player_view,last_move=last_move)
                else:
                    time.sleep(0.5)
                    correct_move = f_utl.hum2comp_movename(curr_position,asked_line_list[semi_move_number])
                    last_move = correct_move
                    f_vis.make_move_animation(curr_position,player_view,correct_move[0],correct_move[1],curr_position.board[7-correct_move[0][1]][correct_move[0][0]])
                    curr_position = f_chs.make_move(curr_position,correct_move)
                    legal_moves = f_chs.all_legal_moves(curr_position)
                    f_vis.actualiserfenetre(curr_position,player_view,last_move=last_move)
                    semi_move_number += 1
                    correct_move = f_utl.hum2comp_movename(curr_position,asked_line_list[semi_move_number])
            elif (sq1,sq2) in legal_moves:
                print("Line added to revision")
                if all_training_lines[index_line_questionned] not in all_training_lines_redo:
                    for i in range(number_of_repetitons):
                        all_training_lines_redo.append(all_training_lines[index_line_questionned])
            else:
                if  f_utl.possible_square(sq1) and f_utl.possible_square(sq2):
                    print(f"Illegal moves {f_utl.coord_to_filerow(sq1)} to {f_utl.coord_to_filerow(sq2)}")
                else:
                    print("Outside of board")