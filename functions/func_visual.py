import pygame
import functions.func_utils as f_utl
from params.params import *
import time

def creerfenetre(res):
    global screen
    screen = pygame.display.set_mode(res)
    pygame.display.set_caption("TANIA chess beta")
    pygame.display.set_icon(pygame_icon)
    screen.fill(backgroundcolor)
    pygame.display.flip()

def actualiserfenetre(position,player_view,grabed_piece=None,coord_piece = None,mousepos = None,texte1='',texte2='',last_move=None):
    global width_square, colorlight, colorlighthighlight, colordark, colordarkhighlight, screen
    afficherdamier(width_square,colorlight,colordark)
    afficherhighlight(width_square, colorlighthighlight, colordarkhighlight,player_view,last_move)
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

def afficherhighlight(width_square,colorlighthighlight,colordarkhighlight,side,last_move):
    global screen, backgroundcolor
    if last_move==None:
        return
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

def make_move_animation(position,player_view,sq1,sq2,piece):
    start_x,start_y = f_utl.middlesquare2pos(sq1,player_view)
    end_x,end_y = f_utl.middlesquare2pos(sq2,player_view)
    visual_steps = int(f_utl.dist(sq2[0]-sq1[0],sq2[1]-sq1[1])*7)
    for i in range(visual_steps+1):
        actualiserfenetre(position,player_view,coord_piece = sq1 ,grabed_piece = piece, mousepos = ((1-i/visual_steps)*start_x+(i/visual_steps)*end_x,(1-i/visual_steps)*start_y+(i/visual_steps)*end_y))
        pygame.time.delay(5)