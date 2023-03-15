import pygame
from func_chess import *

res = (800,800)
backgroundcolor = (50,50,50)


createcases()
placepieces()

"""
screen = pygame.display.set_mode(res)

launched = TrueKC

while launched:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            launched = False
"""

while True:
    showchessboardterminal()
    print(f"{'move for black :' if move%2==0 else 'move for white :'}")
    print(f"move in main is {move}")
    c1c2 = input()
    print(f"your move is {c1c2[0:2]} to {c1c2[2:4]}")
    mouvement(c1c2[0:2],c1c2[2:4])