import time
import os
import random

from objects.objects import Position
from params.params import *

import functions.func_chess as f_chs
import functions.func_utils as f_utl
import functions.func_visual as f_vis

tested_color = 'w'
init_position = Position(starting_fen)
curr_position = f_utl.copyposition(init_position)


f_vis.creerfenetre(res_screen)

legal_moves = f_chs.all_legal_moves(curr_position)
"""
print(f"Number of legal moves are {len(legal_moves)}")
human_legal_moves = []
for move in legal_moves:
    human_legal_moves.append((f_utl.coord_to_filerow(move[0]),f_utl.coord_to_filerow(move[1])))
"""


training_finished = False
all_training_lines = f_utl.get_all_lines_from_folder(os.path.join('.',os.path.join('data','pgn')),tested_color)
print(all_training_lines)
all_training_lines_redo = []
all_lines_length = len(all_training_lines)
index_line_questionned = 0
random.shuffle(all_training_lines)
asked_line = all_training_lines[index_line_questionned][1]
curr_position = Position(all_training_lines[index_line_questionned][0])
f_vis.actualiserfenetre(curr_position)
asked_line_list = asked_line.split()
print(f"Asking line {index_line_questionned}/{all_lines_length}")
correct_move = f_utl.hum2comp_movename(curr_position,asked_line_list[0])
print(f"correct move is {correct_move}")
semi_move_number = 0



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
            if mouse_pressed and grabed_piece != ' ':
                x,y = pygame.mouse.get_pos()
                f_vis.actualiserfenetre(curr_position,coord_piece = sq1,grabed_piece = grabed_piece,mousepos = (x,y))
        if event.type == pygame.MOUSEBUTTONDOWN:
            sq1 = f_utl.mousepos2square(event.pos)
            grabed_piece = curr_position.board[7-sq1[1]][sq1[0]]
            mouse_pressed = True
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pressed = False
            f_vis.actualiserfenetre(curr_position)
            sq2 = f_utl.mousepos2square(event.pos)
            print(f"move done is {(sq1,sq2)}")
            if (sq1,sq2) == correct_move:
                curr_position = f_chs.make_move(curr_position,(sq1,sq2))
                f_vis.actualiserfenetre(curr_position)
                semi_move_number += 1
                if len(asked_line_list) == semi_move_number:
                    curr_position = f_utl.copyposition(init_position)
                    index_line_questionned += 1
                    semi_move_number = 0
                    asked_line_list = all_training_lines[index_line_questionned][1].split()
                    correct_move = f_utl.hum2comp_movename(curr_position,asked_line_list[0])
                    print(f"Correct move is {correct_move}")
                    time.sleep(2)
                    f_vis.actualiserfenetre(curr_position)
                else:
                    time.sleep(0.5)
                    correct_move = f_utl.hum2comp_movename(curr_position,asked_line_list[semi_move_number])
                    f_vis.make_move_animation(curr_position,correct_move[0],correct_move[1],curr_position.board[7-correct_move[0][1]][correct_move[0][0]])
                    curr_position = f_chs.make_move(curr_position,correct_move)
                    legal_moves = f_chs.all_legal_moves(curr_position)
                    f_vis.actualiserfenetre(curr_position)
                    semi_move_number += 1
                    correct_move = f_utl.hum2comp_movename(curr_position,asked_line_list[semi_move_number])