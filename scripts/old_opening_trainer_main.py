#############################################################################
############################# MODULES #######################################
#############################################################################
import pygame
import random
import time

import pygame

pygame.init()

from scripts.objects import *
from param import *
from func import *

init_position = Position(position)
curr_position = copyposition(init_position)

creerfenetre(res_screen)
actualiserfenetre(curr_position)

legal_moves = all_legal_moves(curr_position)
print(f"Number of legal moves are {len(legal_moves)}")
human_legal_moves = []
for move in legal_moves:
    human_legal_moves.append((coord_to_filerow(move[0]),coord_to_filerow(move[1])))


gamemode = "opening"
"""
if gamemode == "opening":
    training_finished = False
    color_tested = 'w'
    player_view = color_tested
    all_training_lines = get_all_lines_from_opening_folder('Openings_trainer\Openings',f'{color_tested}')
    print(all_training_lines)
    all_training_lines_redo = []
    all_lines_length = len(all_training_lines)
    index_line_questionned = 0
    init_index = 1 #1 is begining
    end_index = None #None for reherse the whole lot
    if end_index != None:
        all_training_lines = all_training_lines[init_index-1:end_index]
    else:
        all_training_lines = all_training_lines[init_index-1:]
    random.shuffle(all_training_lines)
    asked_line = all_training_lines[index_line_questionned]
    asked_line_list = asked_line.split()
    print(f"Asking line {index_line_questionned+init_index}/{all_lines_length}")
    correct_move = hum2comp_movename(curr_position,asked_line_list[0])
    if color_tested == 'w':
        semi_move_number = 0
    else:
        curr_position = make_move(curr_position,correct_move)
        legal_moves = all_legal_moves(curr_position)
        semi_move_number = 1
        actualiserfenetre(curr_position,texte1=text1,texte2=text2)
        correct_move = hum2comp_movename(curr_position,asked_line_list[semi_move_number])
"""
training_finished = False
subfolder = 'p'
all_training_lines = get_all_lines_from_folder('./Openings_trainer/Openings',subfolder)
print(all_training_lines)
all_training_lines_redo = []
all_lines_length = len(all_training_lines)
index_line_questionned = 0
random.shuffle(all_training_lines)
asked_line = all_training_lines[index_line_questionned][1]
curr_position = Position(all_training_lines[index_line_questionned][0])
actualiserfenetre(curr_position)
asked_line_list = asked_line.split()
print(f"Asking line {index_line_questionned}/{all_lines_length}")
correct_move = hum2comp_movename(curr_position,asked_line_list[0])
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
                actualiserfenetre(curr_position,coord_piece = sq1,grabed_piece = grabed_piece,mousepos = (x,y))
        if gamemode == "opening":
            if event.type == pygame.MOUSEBUTTONDOWN:
                sq1 = mousepos2square(event.pos)
                grabed_piece = curr_position.board[7-sq1[1]][sq1[0]]
                mouse_pressed = True
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pressed = False
                actualiserfenetre(curr_position)
                sq2 = mousepos2square(event.pos)
                if (sq1,sq2) == correct_move:
                    curr_position = make_move(curr_position,(sq1,sq2))
                    actualiserfenetre(curr_position)
                    time.sleep(0.5)
                    semi_move_number += 1
                    if len(asked_line_list) == semi_move_number:
                        index_line_questionned += 1
                        time.sleep(2)
                        if index_line_questionned >= len(all_training_lines) and len(all_training_lines_redo) == 0:
                            print("Training finished without mistakes :)")
                            training_finished = True
                        elif index_line_questionned >= len(all_training_lines) and all_training_lines != all_training_lines_redo:
                            all_training_lines = all_training_lines_redo
                            index_line_questionned = 0
                        elif index_line_questionned >= len(all_training_lines):
                            print("Training finished")
                            training_finished = True
                        if not training_finished:
                            print(f"Asking line {index_line_questionned+1}/{len(all_training_lines)}")
                            asked_line = all_training_lines[index_line_questionned][1]
                            curr_position = Position(all_training_lines[index_line_questionned][0])
                            actualiserfenetre(curr_position)
                            asked_line_list = asked_line.split()
                            print(f"Asking line {index_line_questionned}/{all_lines_length}")
                            correct_move = hum2comp_movename(curr_position,asked_line_list[0])
                            semi_move_number = 0
                            legal_moves = all_legal_moves(curr_position)
                            correct_move = hum2comp_movename(curr_position,asked_line_list[semi_move_number])
                            """
                            if color_tested == 'b':
                                curr_position = make_move(curr_position,correct_move)
                                legal_moves = all_legal_moves(curr_position)
                                semi_move_number += 1
                                correct_move = hum2comp_movename(curr_position,asked_line_list[semi_move_number])
                            actualiserfenetre(curr_position)
                            """
                    else:
                        correct_move = hum2comp_movename(curr_position,asked_line_list[semi_move_number])
                        curr_position = make_move(curr_position,correct_move)
                        legal_moves = all_legal_moves(curr_position)
                        actualiserfenetre(curr_position)
                        semi_move_number += 1
                        correct_move = hum2comp_movename(curr_position,asked_line_list[semi_move_number])
                elif (sq1,sq2) in legal_moves:
                    print(f"Incorrect move {sq1} to {sq2}, correct move was {coord_to_filerow(correct_move[0])} to {coord_to_filerow(correct_move[1])}")
                    for i in range(3):
                        all_training_lines_redo.append(asked_line)
"""
        if gamemode == "opening" and color_tested == 'w':
            if event.type == pygame.MOUSEBUTTONDOWN:
                sq1 = mousepos2square(event.pos)
            if event.type == pygame.MOUSEBUTTONUP:
                actualiserfenetre(curr_position)
                sq2 = mousepos2square(event.pos)
                if (sq1,sq2) == correct_move:
                    curr_position = make_move(curr_position,(sq1,sq2))
                    actualiserfenetre(curr_position)
                    time.sleep(0.5)
                    semi_move_number += 1
                    if len(asked_line_list) == semi_move_number:
                        index_line_questionned += 1
                        time.sleep(2)
                        if index_line_questionned >= len(all_training_lines) and all_training_lines != all_training_lines_redo:
                            all_training_lines = all_training_lines_redo
                            index_line_questionned = 0
                        elif index_line_questionned >= len(all_training_lines):
                            print("Training finished")
                        print(f"Asking line {index_line_questionned+1}/{len(all_training_lines)}")
                        asked_line = all_training_lines[index_line_questionned]
                        asked_line_list = asked_line.split()
                        semi_move_number = 0
                        curr_position = copyposition(init_position)
                        legal_moves = all_legal_moves(curr_position)
                        correct_move = hum2comp_movename(curr_position,asked_line_list[semi_move_number])
                        actualiserfenetre(curr_position)
                    else:
                        correct_move = hum2comp_movename(curr_position,asked_line_list[semi_move_number])
                        curr_position = make_move(curr_position,correct_move)
                        legal_moves = all_legal_moves(curr_position)
                        actualiserfenetre(curr_position)
                        semi_move_number += 1
                        correct_move = hum2comp_movename(curr_position,asked_line_list[semi_move_number])
                elif (sq1,sq2) in legal_moves:
                    print("Incorrect move")
                    for i in range(3):
                        all_training_lines_redo.append(asked_line)
"""
