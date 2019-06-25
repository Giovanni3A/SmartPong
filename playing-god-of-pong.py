import random
import sys
import pygame
import datetime
import numpy as np

n = int(sys.argv[1])
n_fittests = int(sys.argv[2])
n_sons = int(sys.argv[1])
n_gen = int(sys.argv[3])

def init_n_players_1_layer(n):
    with open("population.dat","w") as file:

        # Write generation 1
        file.write("1")
        file.write("\n")
        
        for player in range(n):
            
            # layer 1
            for neuron_3 in range(3):
                for p in range(7):
                    r = round(2*random.random()-1,2)
                    file.write('{},'.format(r))
            if player < n-1: 
                file.write("\n")

    file.close()


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

def neural_move(input,layer1):
    output = layer1.dot(input)
    decision = np.where(np.array(output)==max(output))[0][0]
    return decision

def pong(layer1):

    pygame.init()

    win_width = 600
    win_height = 500
    window = pygame.display.set_mode((win_width,win_height))
    pygame.display.set_caption("Hi!")

    p_width = 20
    p_height = 90

    p1 = [10,210]
    p2 = [win_width-30,210]
    p1_v = 0
    p2_v = 0

    ball = [250,250]
    ball_radius = 5

    ball_vx = -1 
    #ball_vy = ball_init_dir
    ball_vy = random.sample([-1,0,1],1)[0]
    ball_v_limit = 3

    limit_pv = 3
    limit_p2_up = 3
    limit_p2_down = 2

    n_balls_touch = 0
    n_walks = 0
    zero_v_plays = 0
    winner = False
    run = True
    while run:

        input = np.array([1,p1[1],ball[0],ball[1],ball_vx,ball_vy,p2[1]])
        #player_vertical_position = p1[1]
        #ball_horizontal_posiiton = ball[0]
        #ball_vertical_position = ball[1]
        #ball_horizontal_velocity = ball_vx
        #ball_vartical_velocity = ball_vy
        #oponent_vertical_position = p2[1]

        move = neural_move(input,layer1)        

        #keys = pygame.key.get_pressed()
        
        #if keys[pygame.K_w]:
        #    p1_v = -limit_pv
        #if keys[pygame.K_s]:
        #    p1_v = limit_pv
        if move == 1:
            p1_v = -limit_pv
        elif move == 2:
            p1_v = limit_pv
        
        # Conta numero de passos do player 1
        n_walks += abs(p1_v)

        p1 = move_player(p1,p1_v,0,win_height-p_height)

        # p2 acompanha a bola se ela está na metade dele da tela
        if ball[0] >= win_width/2:
            p2_v = v_pc_player(p2[1]+p_height/2,ball,(limit_p2_up,limit_p2_down))
        else:
            p2_v = 0
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
                #ball_vy = min(ball_vy+p1_v,ball_v_limit)
                n_balls_touch += 1
            else:
                run = False
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
                #ball_vy = min(ball_vy+p1_v,ball_v_limit)
            else:
                run = False
                winner = True
        
        # Bola bater nas paredes verticais
        if ball[1] >= win_height or ball[1] <= 0:
            ball_vy = -ball_vy

        window.fill((0,0,0))
        pygame.draw.circle(window,(255,0,0),ball,ball_radius)
        pygame.draw.rect(window,(200,64,32),(p1[0],p1[1],p_width,p_height))
        pygame.draw.rect(window,(21,62,86),(p2[0],p2[1],p_width,p_height))
        pygame.display.update()
        pygame.time.delay(1)

        # Punir jogos longos parados
        if n_balls_touch >= 3:
            if zero_v_plays == n_balls_touch:
                run = False
                n_balls_touch = 0
                p1[1] = win_height*2

        # Impedir jogos inifinitos
        if n_balls_touch >= 20:
            run = False
            winner = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return []

    # Punir Maradonas
    if winner:
        score = np.exp(-n_walks/1000)
    else:
        score = n_balls_touch

    # winner, score, i_distance_to_ball
    winn = 1 if winner else 0
    i_distance_to_ball = 0 if winner else (win_height - abs((p1[1]+p_height/2)-ball[1]))
    
    pygame.quit()
    return [winn, score, i_distance_to_ball]

def generate_son(dad,mom):
    son = [0 for i in dad]
    nmutations = 0
    for i in range(len(dad)):
        dad_gen = dad[i]
        mom_gen = mom[i]
        if dad_gen == mom_gen:
            son[i] = dad_gen
        else:
            son_gen = dad_gen if random.random() >= 0.5 else mom_gen
            if random.random() <= 0.1:
                d = (son_gen+mom_gen)/2 + 2*(random.random()-1)
                nmutations += 1
                son_gen += d
            son[i] = round(son_gen,2)
    return son, nmutations

def train(n_best=0):
    if n_best == 0:
        input_file = "population.dat"
    else:
        input_file = "pop_by_fit.dat"
    with open(input_file,"r") as file:
        reader = file.read().split('\n')
        generation = int(reader[0])
        players = reader[1:len(reader)]
    file.close()

    round_results = []
    print("Generation: ",generation)
    if n_best == 0:
        n_best = len(players)
        output_file = "pop_by_fit.dat"
    else:
        output_file = "champion_of_pong.dat"

    for ip in range(n_best):
        p = players[ip]
        all = p.split(',')
        list1 = [float(f) for f in all[0:21]]

        # 1 layers, 4 neurons each
        layer1 = np.ndarray(shape=(3,7))

        layer1[0,:] = list1[0:7]
        layer1[1,:] = list1[7:14]
        layer1[2,:] = list1[14:21]

        r = pong(layer1)
        if len(r) > 0:
            round_results.append([r[0],r[1],r[2],p])
        else:
            print("Interrupt warning! The pong game was interrupted.")
            break

        print("Player {}/{}...Result: {}".format(ip+1,n_best,r))

    round_results.sort(reverse=True)

    with open(output_file,"w") as file:
        file.write(str(generation))
        file.write("\n")
        for r in round_results:
            file.write(r[3])
            file.write("\n")

    file.close()


def evolve(n_fittests,n_sons):
    with open("pop_by_fit.dat","r") as file:
        all = file.read().split("\n")
        generation = all[0]
        reproducers = [line.split(',') for line in all[1:n_fittests+1]]
        reproducers = [[float(j) for j in i[:-1]] for i in reproducers]
        print("Reproducing generation",generation)
        sons = []
        idad = 0
        imom = 0
        nmutat = 0
        while len(sons) < n_sons:
            imom += 1
            if imom == len(reproducers):
                idad += 1
                imom = 0
                if idad == len(reproducers):
                    idad = 0
                    imom = 0
            if imom != idad:
                dad = reproducers[idad]
                mom = reproducers[imom]
                son,imutat = generate_son(dad,mom)
                sons.append(son)
                nmutat += imutat
    file.close()

    with open("population.dat","w") as file:
        file.write(str(int(generation)+1))
        file.write("\n")
        for ison in range(len(sons)):
            son = sons[ison]
            for gen in son:
                file.write(str(gen))
                file.write(',')
            if ison < len(sons)-1:
                file.write("\n")
    file.close()
    print("Reproducing of {} new players complete. {} mutations happened!".format(n_sons,nmutat))

init_n_players_1_layer(n)

for generation in range(n_gen-1):
    train()
    evolve(n_fittests,n_sons)

train()
evolve(n_fittests,n_sons)
train(1)