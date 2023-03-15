#############################################################################
############################# MODULES #######################################
#############################################################################
import pygame
import random
import time

from scripts.objects import *
from param import *
from func import *

init_position = Position(position)
curr_position = copyposition(init_position)



pygame.init()

print(get_all_pieces(curr_position))

creerfenetre(res_screen)
actualiserfenetre(curr_position)

legal_moves = all_legal_moves(curr_position)
print(f"Number of legal moves are {len(legal_moves)}")
human_legal_moves = []
for move in legal_moves:
    human_legal_moves.append((coord_to_filerow(move[0]),coord_to_filerow(move[1])))



gamemode = "players"# "playerIA" "IAs"



if gamemode == "opening":
    color_tested = 'b'
    player_view = color_tested
    all_training_lines = get_all_lines_from_opening_folder('Test 3\Openings','b')
    all_training_lines_redo = []
    random.shuffle(all_training_lines)
    index_line_questionned = 0
    asked_line = all_training_lines[index_line_questionned]
    asked_line_list = asked_line.split()
    print(f"Asking line {index_line_questionned+1}/{len(all_training_lines)}")
    correct_move = hum2comp_movename(curr_position,asked_line_list[0])
    print(correct_move)
    if color_tested == 'w':
        semi_move_number = 0
    else:
        curr_position = make_move(curr_position,correct_move)
        legal_moves = all_legal_moves(curr_position)
        semi_move_number = 1
        actualiserfenetre(curr_position)
        correct_move = hum2comp_movename(curr_position,asked_line_list[semi_move_number])

"""
print(f"computer legal moves of len {len(legal_moves)} is {legal_moves}\n")
print(f"human legal moves of len {len(human_legal_moves)} is {human_legal_moves}")
"""
while launched:
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            launched = False
        if gamemode == "players":
            if event.type == pygame.MOUSEBUTTONDOWN:
                sq1 = mousepos2square(event.pos)
            if event.type == pygame.MOUSEBUTTONUP:
                sq2 = mousepos2square(event.pos)
                if (sq1,sq2) in legal_moves:
                    curr_position = make_move(curr_position,(sq1,sq2))
                    print(curr_position.fen)
                    actualiserfenetre(curr_position)
                    legal_moves = all_legal_moves(curr_position)
                    print(f"Number of legal moves are {len(legal_moves)}")
                    human_legal_moves = []
                    for move in legal_moves:
                        human_legal_moves.append((coord_to_filerow(move[0]),coord_to_filerow(move[1])))
                    print(f"human legal moves of len {len(human_legal_moves)} is {human_legal_moves}")
                elif(sq1,(sq2[0],sq2[1],'Q' if curr_position.player == 'w' else 'q')) in legal_moves:
                    gamemode = "promotion2p" if gamemode == "players" else "promotion1p"
        elif gamemode == "promotion2p" or gamemode == "promotion1p":
            if not promotion_showed:
                afficherpromotion(curr_position)
                promotion_showed = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                square = mousepos2square((event.pos[0],event.pos[1]-width_square//2))
                print(square)
                if (player_view == 'w' and square in [(2,4),(3,4),(4,4),(5,4)])  or (player_view == 'b' and square in [(5,3),(4,3),(3,3),(2,3)]):
                    if square in [(2,4),(5,3)]:
                        curr_position = make_move(curr_position,(sq1,(sq2[0],sq2[1],'Q' if curr_position.player == 'w' else 'q')))
                    elif square in [(3,4),(4,3)]:
                        curr_position = make_move(curr_position,(sq1,(sq2[0],sq2[1],'B' if curr_position.player == 'w' else 'b')))
                    elif square in [(4,4),(3,3)]:
                        curr_position = make_move(curr_position,(sq1,(sq2[0],sq2[1],'N' if curr_position.player == 'w' else 'n')))
                    else:
                        curr_position = make_move(curr_position,(sq1,(sq2[0],sq2[1],'R' if curr_position.player == 'w' else 'r')))
                    gamemode = "players" if gamemode == "promotion2p" else "playerIA"
                    actualiserfenetre(curr_position)
                    legal_moves = all_legal_moves(curr_position)
                    print(f"Number of legal moves are {len(legal_moves)}")
        elif gamemode == "random":
            #if event.type == pygame.MOUSEBUTTONDOWN:
            if len(legal_moves) > 0:
                move = random.choice(legal_moves)
                curr_position = make_move(curr_position,move)
                print(curr_position.fen)
                actualiserfenetre(curr_position)
                legal_moves = all_legal_moves(curr_position)
                print(f"Number of legal moves are {len(legal_moves)}")
        elif gamemode == "opening" and color_tested == 'w':
            if event.type == pygame.MOUSEBUTTONDOWN:
                sq1 = mousepos2square(event.pos)
            if event.type == pygame.MOUSEBUTTONUP:
                sq2 = mousepos2square(event.pos)
                if (sq1,sq2) == correct_move:
                    curr_position = make_move(curr_position,(sq1,sq2))
                    actualiserfenetre(curr_position)
                    time.sleep(0.5)
                    semi_move_number += 1
                    if len(asked_line_list) == semi_move_number:
                        index_line_questionned += 1
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
        elif gamemode == "opening" and color_tested == 'b':
            if event.type == pygame.MOUSEBUTTONDOWN:
                sq1 = mousepos2square(event.pos)
            if event.type == pygame.MOUSEBUTTONUP:
                sq2 = mousepos2square(event.pos)
                if (sq1,sq2) == correct_move:
                    curr_position = make_move(curr_position,(sq1,sq2))
                    actualiserfenetre(curr_position)
                    time.sleep(0.5)
                    semi_move_number += 1
                    if len(asked_line_list) == semi_move_number:
                        index_line_questionned += 1
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
                        curr_position = make_move(curr_position,correct_move)
                        legal_moves = all_legal_moves(curr_position)
                        semi_move_number += 1
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
                    print(f"Incorrect move, correct move was {coord_to_filerow(correct_move[0])} to {coord_to_filerow(correct_move[1])}")
                    for i in range(3):
                        all_training_lines_redo.append(asked_line)

