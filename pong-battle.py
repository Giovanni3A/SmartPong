import random
import sys
import pygame
import datetime
import numpy as np

path1 = sys.argv[1]
path2 = sys.argv[2]

def move_player(player,v,min_lim,max_lim):
    y = player[1] + v
    y = max(y,min_lim)
    y = min(y,max_lim)
    return [player[0],y]

def move_ball(posx,posy,vx,vy):
    return (posx+vx,posy+vy)

def neural_move(input,layer1):
    output = layer1.dot(input)
    decision = np.where(np.array(output)==max(output))[0][0]
    return decision

def pong(layer1,layer2):

    pygame.init()

    win_width = 400
    win_height = 400

    p_width = 20
    p_height = 90

    ball_radius = 5
    ball_v_limit = 3

    limit_pv = 3
    limit_p2_up = 3
    limit_p2_down = 3
    window = pygame.display.set_mode((win_width,win_height))
    pygame.display.set_caption("Hi!")

    p1 = [p_width/2,win_height/2-p_height/2]
    p2 = [win_width-3*p_width/2,win_height/2-p_height/2]
    p1_v = 0
    p2_v = 0

    ball = [int(win_width/2),int(win_height/2)]

    ball_vx = random.sample([-1,1],1)[0] 
    ball_vy = random.sample([-1,0,1],1)[0]

    n_balls_touch = 0
    zero_v_plays = 0
    winner = 0
    run = True
    while run:

        input1 = np.array([1,p1[1],ball[0],ball[1],ball_vx,ball_vy,p2[1]])
        input2 = np.array([1,p2[1],win_width-ball[0],ball[1],-ball_vx,ball_vy,p1[1]])

        move1 = neural_move(input1,layer1)
        move2 = neural_move(input2,layer2)
        
        if move1 == 1:
            p1_v = -limit_pv
        elif move1 == 2:
            p1_v = limit_pv

        if move2 == 1:
            p2_v = -limit_pv
        elif move1 == 2:
            p2_v = limit_pv

        p1 = move_player(p1,p1_v,0,win_height-p_height)
        p2 = move_player(p2,p2_v,0,win_height-p_height)
        
        ball = move_ball(ball[0],ball[1],ball_vx,ball_vy)

        # Bola bate no player 1
        if ball[0] <= p1[0] + p_width:

            # Contar vezes que os players jogaram parados
            if p1_v == p2_v == 0:
                zero_v_plays += 1

            if p1[1] <= ball[1] <= p1[1]+p_height:
                ball_vx = -ball_vx
                # Mudar a velocidade vertical da bola
                if p1_v != 0:
                    iball_vy = ball_vy+abs(p1_v)/p1_v
                    if iball_vy >= 0:
                        ball_vy = int(min(iball_vy,ball_v_limit))
                    else:
                        ball_vy = int(max(iball_vy,-ball_v_limit))
            else:
                run = False
                winner = 2
        # Bola bate no player 2
        elif ball[0] >= p2[0]:
            if p2[1] <= ball[1] <= p2[1]+p_height:
                ball_vx = -ball_vx
                # Mudar a velocidade vertical da bola
                if p2_v != 0:
                    iball_vy = ball_vy+abs(p2_v)/p2_v
                    if iball_vy >= 0:
                        ball_vy = int(min(iball_vy,ball_v_limit))
                    else:
                        ball_vy = int(max(iball_vy,-ball_v_limit))
            else:
                run = False
                winner = 1
        
        # Bola bater nas paredes verticais
        if ball[1] >= win_height or ball[1] <= 0:
            ball_vy = -ball_vy

        window.fill((0,0,0))
        pygame.draw.circle(window,(255,0,0),ball,ball_radius)
        pygame.draw.rect(window,(200,64,32),(p1[0],p1[1],p_width,p_height))
        pygame.draw.rect(window,(21,62,86),(p2[0],p2[1],p_width,p_height))
        pygame.display.update()
        pygame.time.delay(1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return []

    pygame.quit()
    return winner

name1 = path1.split("\\")[1]
name2 = path2.split("\\")[1]

input_file1 = path1
with open(input_file1,"r") as file:
    reader1 = file.read().split('\n')
    generation1 = int(reader1[0])
    p1 = reader1[1:len(reader1)][0]
file.close()

input_file2 = path2
with open(input_file2,"r") as file:
    reader2 = file.read().split('\n')
    generation2 = int(reader2[0])
    p2 = reader2[1:len(reader2)][0]
file.close()

player1 = [float(f) for f in p1.split(',')[0:21]]
player2 = [float(f) for f in p2.split(',')[0:21]]

layer1 = np.ndarray(shape=(3,7))
layer2 = np.ndarray(shape=(3,7))

layer1[0,:] = player1[0:7]
layer1[1,:] = player1[7:14]
layer1[2,:] = player1[14:21]

layer2[0,:] = player2[0:7]
layer2[1,:] = player2[7:14]
layer2[2,:] = player2[14:21]

print("***********************************************************")
print("On the left side, player {}, with {} generations of age".format(name1,generation1))
print("***********************************************************")
print("On the right side, player {}, with {} generations of age".format(name2,generation2))
print("***********************************************************")

print("It's shoowwww time!")
print("***********************************************************")

r = pong(layer1,layer2)

print("And the champion is {}!!!".format([name1,name2][r-1]))