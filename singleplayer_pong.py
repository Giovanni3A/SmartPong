import pygame
import random
import datetime
import numpy as np

def move_player(player,v,min_lim,max_lim):
    y = player[1] + v
    y = max(y,min_lim)
    y = min(y,max_lim)
    return [player[0],y]

def v_pc_player(pc_center,ball,v_limits):
    if pc_center < ball[1]:
        return v_limits[1]
    elif pc_center > ball[1]:
        return -v_limits[0]
    else:
        return 0

def move_ball(posx,posy,vx,vy):
    return (posx+vx,posy+vy)

def pong():

    pygame.init()

    win_width = 400
    win_height = 400
    window = pygame.display.set_mode((win_width,win_height))
    pygame.display.set_caption("Hi!")

    p_width = 20
    p_height = 90

    p1 = [10,210]
    p2 = [win_width-30,210]
    ball = [250,250]
    ball_radius = 5

    ball_vx = -1 
    ball_vy = random.sample([-1,1],1)[0]
    ball_v_limit = 3

    limit_pv = 3
    limit_p2_up = 3
    limit_p2_down = 2

    initial_t = datetime.datetime.now()
    winner = True
    run = True
    while run:

        p1_v = 0
        p2_v = 0

        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w]:
            p1_v = -limit_pv
        if keys[pygame.K_s]:
            p1_v = limit_pv

        p1 = move_player(p1,p1_v,0,win_height-p_height)

        # p2 é o mais pika
        p2_v = v_pc_player(p2[1]+p_height/2,ball,(limit_p2_up,limit_p2_down))
        p2 = move_player(p2,p2_v,0,win_height-p_height)
        
        ball = move_ball(ball[0],ball[1],ball_vx,ball_vy)

        # Bola bate em algum player
        if ball[0] <= p1[0] + p_width:
            if p1[1] <= ball[1] <= p1[1]+p_height:
                ball_vx = -ball_vx
                if p1_v != 0:
                    ball_vy = int(min(ball_vy+abs(p1_v)/p1_v,ball_v_limit))
            else:
                run = False
                winner = False
        elif ball[0] >= p2[0]:
            if p2[1] <= ball[1] <= p2[1]+p_height:
                ball_vx = -ball_vx
                if p2_v != 0:
                    ball_vy = int(min(ball_vy+abs(p2_v)/p2_v,ball_v_limit))
            else:
                run = False

        # Bola bater nas paredes verticais
        if ball[1] >= win_height or ball[1] <= 0:
            ball_vy = -ball_vy

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        window.fill((0,0,0))
        pygame.draw.circle(window,(255,0,0),ball,ball_radius)
        pygame.draw.rect(window,(200,64,32),(p1[0],p1[1],p_width,p_height))
        pygame.draw.rect(window,(21,62,86),(p2[0],p2[1],p_width,p_height))
        pygame.display.update()

        pygame.time.delay(7)

    total_time = (datetime.datetime.now() - initial_t).seconds
    score = 2*total_time if winner else total_time

    pygame.quit()

    return score

print(pong())
