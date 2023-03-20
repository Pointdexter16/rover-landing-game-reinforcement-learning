import pygame
import time
import random
from math import sin,cos,tan
import math

pygame.init()

clock=pygame.time.Clock()

window=pygame.display.set_mode((1000,700))

running=True

space_craft=pygame.image.load('space_ship.png')

space_craft_180=pygame.transform.rotate(space_craft,-20.5)

space_craft_x=500
space_craft_y=10

velocity_y=10
velocity_x=0
impact_velocity=10
orientation=0 #degrees


ACCE_MOON=1.62

gas_state='not vented'

font=pygame.font.Font('Organic_Relief.ttf',16)
textX=10
textY=10

gas_x=[]
gas_y=[]
gas_dis=[]
gas_len_x=[]
gas_len_y=[]
gas_color=[]
upper_threshold=[]
lower_threshold=[]

def space_craft_movement(image,acceleration,side_acceleration):
    global space_craft_y
    global space_craft_x
    global velocity_y
    global velocity_x
    global orientation
    global impact_velocity
    global movement

    orientation=orientation+change_orientation_right+change_orientation_left

    net_acceleration_y=ACCE_MOON+acceleration*cos(orientation*(math.pi/180))+side_acceleration*sin(orientation*(math.pi/180))
    net_acceleration_x=acceleration*sin(orientation*(math.pi/180))+side_acceleration*cos(orientation*(math.pi/180))

    s_x=(velocity_x*(1/60)+0.5*net_acceleration_x*((1/60)**2))*10
    s_y=(velocity_y*(1/60)+0.5*net_acceleration_y*((1/60)**2))*10

    velocity_y=velocity_y+net_acceleration_y*(1/60)
    velocity_x=velocity_x+net_acceleration_x*(1/60)

    space_craft_y+=s_y
    space_craft_x+=s_x

    if orientation>360 or orientation<-360:
        orientation=0
    if space_craft_y>600:
        space_craft_y=600
        if movement==0:
            impact_velocity=velocity_y
            movement=1
        velocity_y=0
        velocity_x=0

    image=pygame.transform.rotate(image,orientation)
    window.blit(image,(space_craft_x,space_craft_y))

def gas_exhaust():
    global gas_state

    if gas_state=='not vented':
        for i in range(30):
            gas_len_x.append(0)
            gas_len_y.append(5)
            gas_dis.append(0)
            lower_threshold.append(i*5)
            upper_threshold.append(50+(i*5))
            gas_x.append(space_craft_x+50)
            gas_y.append(space_craft_y+100)
            gas_color.append(random.randint(50,255))
        gas_state='vented'
    

def status():
    velocity_lander=font.render(f'VELOCITY: {velocity_y:.1f}',True,(255,255,255))
    orientation_lander=font.render(f'ORIENTATION: {orientation:.1f}',True,(255,255,255))
    coordinates_lander=font.render(f'(X,Y): ({space_craft_x/10:.1f},{space_craft_y/10:.1f})M',True,(255,255,255))
    impact_velocity_lander=font.render(f'IMPACT VELOCITY: {impact_velocity:.1f}',True,(255,255,255))
    window.blit(velocity_lander,(textX,textY))
    window.blit(orientation_lander,(textX,textY+30))
    window.blit(coordinates_lander,(textX,textY+60))
    window.blit(impact_velocity_lander,(textX,textY+90))


fps=0

initial=time.time()

thrust=0
thrust_left=0
thrust_right=0
change_orientation_left=0
change_orientation_right=0

second_count=1

movement=0
thrust_right=0
thrust_left=0

while running:
    window.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        if event.type == pygame.KEYDOWN:
            movement=0
            if event.key == pygame.K_UP:
                thrust=-15
                gas_exhaust()
            if event.key == pygame.K_LEFT:
                change_orientation_left=0.5
            if event.key == pygame.K_RIGHT:
                change_orientation_right=-0.5
            if event.key == pygame.K_d:
                thrust_right=5
            if event.key == pygame.K_a:
                thrust_left=-5
        if event.type == pygame.KEYUP:
            if event.key ==  pygame.K_UP:
                thrust=0
                gas_state='not vented'
            if event.key == pygame.K_LEFT:
                change_orientation_left=0
            if event.key == pygame.K_RIGHT:
                change_orientation_right=0
            if event.key == pygame.K_d:
                thrust_right=0
            if event.key == pygame.K_a:
                thrust_left=0
                
    thrust_side=thrust_left+thrust_right
    if gas_state=='vented':
        for i in range(30):
            gas_dis[i]+=5
            gas_y[i]+=gas_len_y[i]
            gas_x[i]+=tan(orientation*(math.pi/180))*gas_len_y[i]
            if lower_threshold[i]<gas_dis[i]<upper_threshold[i]:
                if gas_y[i]-space_craft_y-30<0 or gas_y[i]-space_craft_y>random.randint(100,200):
                    pass
                else:
                    pygame.draw.circle(window,(gas_color[i],100,100),(gas_x[i],gas_y[i]),5)
            elif gas_dis[i]>=upper_threshold[i]:
                gas_dis[i]=0
                gas_x[i],gas_y[i]=space_craft_x+50,space_craft_y+100

    
   
    space_craft_movement(space_craft,thrust,thrust_side)
    status()
    # window.blit(space_craft_180,(250,250))
    pygame.display.update()
    clock.tick(60)
    fps+=1
    
    # if int(time.time()-initial) == second_count:
    #     print(fps)
    #     fps=0
    #     second_count+=1
