import pygame
import sys
from program_logic import *
from database import get_best, cur, add_player

def draw_interface(score,delta=0):
    pygame.draw.rect(screen,WHITE,TITLE_REC)
    font=pygame.font.SysFont('stxingkai',70)
    font_score= pygame.font.SysFont('simsun',48)
    font_delta= pygame.font.SysFont('simsun',48)
    text_score= font_score.render("Score: ",True, COLOR_TEXT)
    text_score_value=font_score.render(f"{score}: ",True, COLOR_TEXT)
    screen.blit(text_score, (20,35))
    screen.blit(text_score_value,(175,35))
    if delta > 0:
        text_delta= font_delta.render(f"+{delta} ",True, COLOR_TEXT)
        screen.blit(text_delta,(175,65))
    for row in range(BLOCKS):
        for column in range(BLOCKS):
            value = mas[row][column]
            text= font.render(f'{value}', True, BLACK)
            w= column*SIZE_BLOCKS +(column+1)*MARGIN
            h= row*SIZE_BLOCKS +(row+1)*MARGIN + SIZE_BLOCKS
            pygame.draw.rect(screen,COLORS[value] ,(w,h,SIZE_BLOCKS,SIZE_BLOCKS))
            if value !=0:
                font_w, font_h = text.get_size()
                text_x=w + (SIZE_BLOCKS - font_w) / 2
                text_y=h + (SIZE_BLOCKS - font_h) / 2
                screen.blit(text,(text_x,text_y))
BLOCKS= 4
SIZE_BLOCKS=110
MARGIN=10
WIDTH= BLOCKS * SIZE_BLOCKS + MARGIN * 5
HEIGTH= WIDTH + SIZE_BLOCKS
TITLE_REC= pygame.Rect(0,0,WIDTH,SIZE_BLOCKS)
WHITE= (225, 255, 255)
GRAY=(130, 130, 130)
BLACK=(0,0,0)
COLORS={
0: (130,130,130),
2: (255,255,255),
4: (255,255,128),
8: (225,255,0),
16:(225,235,225),
32:(255,235,128),
64:(255,235,0),
128:(255,225,125),
256:(130,130,130),
512:(255,255,255),
1024:(255,255,128),
2048:(225,255,0)  }
COLOR_TEXT=(255, 127, 0)
USERNAME= None
score=None
delta= None
pygame.init()
screen= pygame.display.set_mode((WIDTH,HEIGTH))
pygame.display.set_caption("2048_or_game_na_colenke")
GAMERS_DB = get_best()
mas=None
text=None

def init_const():
    global score, mas, delta
    delta=0
    score = 0
    mas=  [
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0]
    ]    
    empty1= get_empty_list(mas)
    empty2= get_empty_list(mas)
    random.shuffle(empty1)
    random.shuffle(empty2)
    random_num1= empty1.pop()
    random_num2= empty2.pop()
    x1, y1= get_index_for_number(random_num1)
    x2, y2= get_index_for_number(random_num2)
    mas= insert_2_or_4(mas,x1,y1)
    mas= insert_2_or_4(mas,x2,y2)

init_const()

def draw_top_gamers():
    font_top= pygame.font.SysFont('simsun',30)
    font_gamer= pygame.font.SysFont('simsun',24)
    text_head= font_top.render("Best tries: ", True, COLOR_TEXT)
    screen.blit(text_head,(250,0))
    for index, gamer in enumerate(GAMERS_DB):
        name, score =gamer
        s=f"{index+1}.{name} - {score}"
        text_gamer= font_gamer.render(s, True, COLOR_TEXT)
        screen.blit(text_gamer,(250,25 + 25 * index))
        print(index,name,score)

def draw_intro():
    img2048= pygame.image.load('C:\\Users\\Akira\\Documents\\VScode\\2048\\2048.png')
    font=pygame.font.SysFont('stxingkai',70)
    text_welcome= font.render('Welcome!',True, WHITE)
    name = 'Введите имя'
    is_find_name=False
    while not is_find_name:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    if name == 'Введите имя':
                        name =event.unicode
                    else:
                        name+= event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_RETURN:
                    if len(name) > 2:
                        global USERNAME
                        USERNAME = name
                        is_find_name= True
                        break
        screen.fill(BLACK)
        text_name= font.render(name,True,WHITE)
        rect_name=text_name.get_rect()
        rect_name.center = screen.get_rect().center
        screen.blit(pygame.transform.scale(img2048,[200,200]),[10,10])
        screen.blit(text_welcome, (230,80))
        screen.blit(text_name, rect_name)
        pygame.display.update()
    screen.fill(BLACK)

def draw_game_over():
    global USERNAME, GAMERS_DB
    img2048= pygame.image.load('C:\\Users\\Akira\\Documents\\VScode\\2048\\2048.png')
    font=pygame.font.SysFont('stxingkai',70)
    text_game_over= font.render('Game over!',True, WHITE)
    text_score=font.render(f"Вы набрали {score}: ",True, WHITE)
    best_score=0
    if len(GAMERS_DB)>1:
        best_score= GAMERS_DB[0][1]
    if score > best_score:
        text="Рекорд побит"
    else:
        text=f'Рекорд {best_score}'
    add_player(USERNAME,score)
    text_record= font.render(text, True, WHITE)
    make_disicion= False
    GAMERS_DB=get_best()
    while not make_disicion:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    make_disicion= True
                    init_const()
                elif event.key == pygame.K_RETURN:
                    USERNAME = None
                    make_disicion= True
                    init_const()
        screen.fill(BLACK)
        screen.blit(text_game_over, (230,80))
        screen.blit(text_score, (30,250))
        screen.blit(text_record, (30,300))
        screen.blit(pygame.transform.scale(img2048,[200,200]),[10,10])
        pygame.display.update()
    screen.fill(BLACK)

def game_loop():
    global mas,score,delta
    draw_interface(score,delta)
    draw_top_gamers()
    pygame.display.update()
    is_mas_move= False
    while is_zero_in_mas(mas) or can_move(mas):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                delta=0
                if event.key == pygame.K_LEFT:
                    mas,delta,is_mas_move=move_left(mas)
                elif event.key == pygame.K_RIGHT:
                    mas,delta,is_mas_move=move_right(mas)
                elif event.key == pygame.K_UP:
                    mas,delta,is_mas_move=move_up(mas)
                elif event.key == pygame.K_DOWN:
                    mas,delta,is_mas_move=move_down(mas)
                score+=delta
                print(is_mas_move)
                if is_zero_in_mas(mas) and is_mas_move:
                    empty= get_empty_list(mas)
                    random.shuffle(empty)
                    random_num= empty.pop()
                    x, y= get_index_for_number(random_num)
                    mas= insert_2_or_4(mas,x,y)                
                    print(f'Мы выполнили элемент под номером {random_num}')
                    is_mas_move=False
                pretty_print(mas)
                draw_interface(score,delta)
                pygame.display.update()

while True:
    if USERNAME is None:
        draw_intro()
    game_loop()
    draw_game_over()