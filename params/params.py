import pygame
import os

pygame.init()

launched = True
screen = pygame.display.set_mode((1,1))
miniboard = True
mouse_pressed = False

number_of_repetitons = 3 #In case of wrong answer

pygame_icon = pygame.image.load(os.path.join('data',os.path.join('images','volowan_logo_mini.png')))

starting_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

text1 = "Repertoire"

text2 = ""

arial_font = pygame.font.SysFont("arial", 30, True)

init_rook_castle_correspondance ={
    (0,0):'Q',
    (7,0):'K',
    (0,7):'q',
    (7,7):'k'}

promotion_showed = False

if not miniboard:
    border_chessboard_pix = 800
    chosen_pieces_sprite = pygame.image.load('data/images/Chess_Pieces_Sprite_Reduced.png')
else:
    border_chessboard_pix = 400
    chosen_pieces_sprite = pygame.image.load('data/images/Chess_Pieces_Sprite_Mini.png')

width_square = border_chessboard_pix//8#px

menu_width_pix = 200#px#200#px

res_screen = (border_chessboard_pix+menu_width_pix, border_chessboard_pix)

setcolor1 = [(130, 150, 130),(100, 120, 100),(160, 170, 80),(140, 150, 65),(200, 200, 200)]
setcolor2 = [(136,164,186),(105,134,152),(149,184,114),(132,165,94),(70,70,70)]

colorlight,colordark,colorlighthighlight,colordarkhighlight,backgroundcolor = setcolor2

possprite = {
    'K':(0,0),
    'Q':(1,0),
    'B':(2,0),
    'N':(3,0),
    'R':(4,0),
    'P':(5,0),
    'k':(0,1),
    'q':(1,1),
    'b':(2,1),
    'n':(3,1),
    'r':(4,1),
    'p':(5,1)}

possible_moves_pieces = {#Vecteurs directeurs et distance max (val. absolue)
    'K':[[(0,1),(1,-1),(1,0),(1,1)],1],
    'Q':[[(0,1),(1,-1),(1,0),(1,1)],7],
    'R':[[(0,1),(1,0)],7],
    'B':[[(1,1),(1,-1)],7],
    'N':[[(-2,1),(-1,2),(1,2),(2,1)],1]}

