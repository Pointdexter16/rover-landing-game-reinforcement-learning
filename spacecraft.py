
from tkinter import Y
import pygame
import time
import random
from math import sin,cos,radians,sqrt
import math
from  threading import Thread,get_ident

pygame.init()

clock=pygame.time.Clock()

WINDOW_X=1000
WINDOW_Y=650

window=pygame.display.set_mode((WINDOW_X,WINDOW_Y))

running=True

space_craft=pygame.image.load('space_ship.png') #dimensions->100X100px
bg=pygame.image.load('space.png')#dimensions->1000x650

space_craft_180=pygame.transform.rotate(space_craft,-20.5)

space_craft_x=50
space_craft_y=10
landing_gear_left_end_x=0
landing_gear_left_end_y=0
landing_gear_right_end_x=0
landing_gear_right_end_y=0

velocity_y=10
velocity_x=0
impact_velocity=0
orientation=0 #degrees
terrain_array=[]

MASS=15103
ACCE_MOON=1.62
LEN_LANDING_GEAR=60
acceptable_impact_vel=2
compression_on_accep_vel=LEN_LANDING_GEAR*cos(radians(45))*0.5
h=LEN_LANDING_GEAR*cos(radians(45))+50
K_BG=MASS*(acceptable_impact_vel**2)/(compression_on_accep_vel**2) + 2*MASS*ACCE_MOON*h/(compression_on_accep_vel**2)    #1/2*mv^2 + mgh = 1/2*kx^2 (energy equation)
K_BG=K_BG/2
radian_multiplier=6.28318531/WINDOW_X

spring_comp_l=0
spring_comp_r=0
spring_acc=0

gas_state='not vented'

font=pygame.font.Font('Organic_Relief.ttf',16) #text font 
textX=10
textY=10

gas_x=[] #tracks the gas particle position status
gas_y=[]
gas_dis=[]
gas_len_x=[]
gas_len_y=[]
gas_color=[]
upper_threshold=[]
lower_threshold=[]


def dist(A,B):
    dist=0
    for a,b in zip(A,B):
        dist+=(a-b)**2
    dist=sqrt(dist)
    return dist

def init():
    for i in range(30):
            gas_len_x.append(0)
            gas_len_y.append(5)
            gas_dis.append(0) #keeps track of the total distance covered by the gas particle
            lower_threshold.append(i*5) 
            upper_threshold.append(50+(i*5))
            gas_x.append(point_tracking(50,110,Y=False)) # gas x,y cordinate 
            gas_y.append(point_tracking(50,110,X=False))
            gas_color.append(random.randint(50,255))

def terrain():

    for i in range(WINDOW_X):
        t_y=WINDOW_Y-100*cos(i*radian_multiplier)
        terrain_array.append(t_y)

def engine_status(c:list):
    """
        arg->[center_x,center_y,raduis]
    """
    x=c[0]
    y=c[1]
    r=c[2]
    black=(0,0,0)
    white=(255,255,255)
    color=black if not(engine_active) else white
    pygame.draw.circle(window,white,(x,y),r+50)
    pygame.draw.circle(window,black,(x,y),r+49)
    pygame.draw.circle(window,white,(x,y),r)
    pygame.draw.circle(window,color,(x,y),r-1)

def stabilize():
    global change_orientation_left
    global change_orientation_right

    if orientation<0:
        change_orientation_right=0.5
        while orientation!=0:
            pass
        change_orientation_right=0
    elif orientation>0:
        change_orientation_left=-0.5
        while orientation!=0:
            pass
        change_orientation_left=0

def point_tracking(x_off_set_val,y_off_set_val,X=True,Y=True):
    """
        return formate x,y
    """   
    if 0>=orientation>-90:
        norientation=-orientation
        x=space_craft_x+(100*cos(radians(90-norientation)))+(x_off_set_val*cos(radians(norientation)))-(y_off_set_val*sin(radians(norientation)))
        y=space_craft_y+(x_off_set_val*sin(radians(norientation)))+(y_off_set_val*cos(radians(norientation))) 
    elif 0<orientation<90:
        x=space_craft_x+(x_off_set_val*cos(radians(orientation)))+(y_off_set_val*sin(radians(orientation)))
        y=space_craft_y+(100*cos(radians(90-orientation)))-(x_off_set_val*sin(radians(orientation)))+(y_off_set_val*cos(radians(orientation)))  
    elif -90>=orientation>-180:
        norientation=(-orientation)-90
        x=space_craft_x+100*(sqrt(2)*cos(radians((90-(2*norientation))/2)))-(x_off_set_val*sin(radians(norientation)))-(y_off_set_val*cos(radians(norientation)))
        y=space_craft_y+(100*cos(radians(90-norientation)))+(x_off_set_val*cos(radians(norientation)))-(y_off_set_val*sin(radians(norientation)))
    elif 90<=orientation<180:
        norientation=orientation-90
        x=space_craft_x+100*(cos(radians(90-norientation)))-x_off_set_val*(sin(radians(norientation)))+y_off_set_val*(cos(radians(norientation)))
        y=space_craft_y+100*(sqrt(2)*cos(radians((90-(2*norientation))/2)))-(x_off_set_val*cos(radians(norientation)))-(y_off_set_val*sin(radians(norientation)))        
    elif -180>=orientation>-270:
        norientation=(-orientation)-180
        x=space_craft_x+(100*cos(radians(norientation)))-(x_off_set_val*cos(radians(norientation)))+(y_off_set_val*sin(radians(norientation)))
        y=space_craft_y+100*(sqrt(2)*cos(radians((90-(2*norientation))/2)))-(x_off_set_val*sin(radians(norientation)))-(y_off_set_val*cos(radians(norientation)))
    elif 180<=orientation<270:
        norientation=orientation-180
        x=space_craft_x+100*(sqrt(2)*cos(radians((90-(2*norientation))/2)))-(x_off_set_val*cos(radians(norientation)))-(y_off_set_val*sin(radians(norientation)))
        y=space_craft_y+100*(cos(radians(norientation)))+(x_off_set_val*sin(radians(norientation)))-(y_off_set_val*cos(radians(norientation)))
    elif -270>=orientation>=-361:
        norientation=(-orientation)-270
        x=space_craft_x+(x_off_set_val*sin(radians(norientation)))+(y_off_set_val*cos(radians(norientation)))
        y=space_craft_y+(100*cos(radians(norientation)))-(x_off_set_val*cos(radians(norientation)))+(y_off_set_val*sin(radians(norientation)))
    elif 270<=orientation<=361:
        norientation=orientation-270
        x=space_craft_x+(100*cos(radians(norientation)))+(x_off_set_val*sin(radians(norientation)))-(y_off_set_val*cos(radians(norientation)))
        y=space_craft_y+(x_off_set_val*cos(radians(norientation)))+(y_off_set_val*sin(radians(norientation)))
    if X and Y:
        return x,y
    elif X:
        return x
    else:
        return y

def number(num):
    i=0
    while(True):
        q=num/10       
        i+=1
        if q<1:
            break
    return int(str(num)[:2])/100,i-1


def rotate_image_at_center(image,angle,x,y)->pygame.surface:

    rotated_image=pygame.transform.rotate(image,angle)
    new_rect=rotated_image.get_rect(center=image.get_rect(center=(x,y)).center)
    return rotated_image,new_rect

def net_energy_tracker():
    k_e=(1/2)*MASS*(velocity_y)**2
    p_e=MASS*ACCE_MOON*(WINDOW_Y-center_y)
    spring_e=-1/2*K_BG*((spring_comp_r+spring_comp_l)**2)
    t_e=k_e+p_e+spring_e
    return t_e

def space_craft_movement(image,acceleration,side_acceleration):
    global space_craft_y #all the variable are global as the scope of these varibles is outside the function
    global space_craft_x
    global velocity_y
    global velocity_x
    global orientation
    global impact_velocity
    global movement
    global landing_gear_y_left
    global landing_gear_y_right
    global center_y
    global spring_comp_l
    global spring_comp_r
    global impact_velocity
    global landing_gear_left_end_x
    global landing_gear_left_end_y
    global landing_gear_right_end_x
    global landing_gear_right_end_y
    global spring_acc
    global main_thruster_x
    global main_thruster_y

    orientation=orientation+change_orientation_right+change_orientation_left

    

    #           /
    #  \    \  / *                spaceship
    #   \    \ --------
    #    \    \
    # 
    #       |*\ thrust, *-> theta = orientation, cos(theta)=along y axis, sin(theta)=along x axis
    #       |  \ 

    
    
    
    
    main_thruster_x,main_thruster_y=point_tracking(50,100)
    landing_gear_x_left,landing_gear_y_left=point_tracking(25,100)
    landing_gear_x_right,landing_gear_y_right=point_tracking(75,100)
    center_x,center_y=point_tracking(50,50)
    landing_gear_angle_right=radians(45+orientation)
    landing_gear_angle_left=radians(-45+orientation)
    landing_gear_left_end_x=landing_gear_x_left+(LEN_LANDING_GEAR*sin(landing_gear_angle_left))
    landing_gear_left_end_y=landing_gear_y_left+(LEN_LANDING_GEAR*cos(landing_gear_angle_left))
    landing_gear_right_end_x=landing_gear_x_right+(LEN_LANDING_GEAR*sin(landing_gear_angle_right))
    landing_gear_right_end_y=landing_gear_y_right+(LEN_LANDING_GEAR*cos(landing_gear_angle_right))
    


    for i,t_y in enumerate(terrain_array):
        if int(landing_gear_left_end_x)==i and t_y<650:
            spring_comp_l=0 if (t_y-landing_gear_y_left>=LEN_LANDING_GEAR*cos(radians(45)) and i==int(landing_gear_left_end_x)) else LEN_LANDING_GEAR*cos(radians(45))-(t_y-landing_gear_y_left)
        elif int(landing_gear_left_end_x)==i and t_y>=650:
            spring_comp_l=0 if WINDOW_Y-landing_gear_y_left>=LEN_LANDING_GEAR*cos(radians(45)) else LEN_LANDING_GEAR*cos(radians(45))-(WINDOW_Y-landing_gear_y_left)
        if int(landing_gear_right_end_x)==i and t_y<650:
            spring_comp_r=0 if (t_y-landing_gear_y_right>=LEN_LANDING_GEAR*cos(radians(45)) and i==int(landing_gear_right_end_x)) else LEN_LANDING_GEAR*cos(radians(45))-(t_y-landing_gear_y_right)
        elif int(landing_gear_right_end_x)==i and t_y>=650:
            spring_comp_r=0 if WINDOW_Y-landing_gear_y_right>=LEN_LANDING_GEAR*cos(radians(45)) else LEN_LANDING_GEAR*cos(radians(45))-(WINDOW_Y-landing_gear_y_right)
        if (landing_gear_left_end_y>t_y and i==int(landing_gear_left_end_x))or(landing_gear_right_end_y>t_y and i==int(landing_gear_right_end_x)):
                if landing_gear_left_end_y>t_y and i==int(landing_gear_left_end_x): landing_gear_left_end_y=t_y;
                if landing_gear_right_end_y>t_y and i==int(landing_gear_right_end_x): landing_gear_right_end_y=t_y;
                if movement==0 and not(engine_active):             # After hitting the ground if movement is 0 impact velocity is registered and movement is assigned 1 then if any arrow key is pressed except for down then movement becomes 0 again
                    impact_velocity=velocity_y
                    movement=1
                    velocity_x=0
        pygame.draw.circle(window,(255,255,255),(i,t_y),1)
      



    if orientation>360 or orientation<-360:
        orientation=0 # recalibrate oritentation after exceeding 360 or -360 back to 0 
    if landing_gear_left_end_y>WINDOW_Y or landing_gear_right_end_y>WINDOW_Y:
        if landing_gear_left_end_y>WINDOW_Y: landing_gear_left_end_y=WINDOW_Y
        if landing_gear_right_end_y>WINDOW_Y: landing_gear_right_end_y=WINDOW_Y
        if movement==0 and not(engine_active):             # After hitting the ground if movement is 0 impact velocity is registered and movement is assigned 1 then if any arrow key is pressed except for down then movement becomes 0 again
            impact_velocity=velocity_y
            movement=1
            velocity_x=0
    if space_craft_y>=550:
        space_craft_y=550
        velocity_x=0
        velocity_y=0

    spring_acc=K_BG*(spring_comp_r+spring_comp_l)/MASS

    net_acceleration_y=ACCE_MOON+acceleration*cos(orientation*(math.pi/180))+side_acceleration*sin(orientation*(math.pi/180))-spring_acc-4*velocity_y*movement # math.pi/180->degree to radian
    # print(net_acceleration_y)
    net_acceleration_x=acceleration*sin(orientation*(math.pi/180))+side_acceleration*cos(orientation*(math.pi/180))
    velocity_y=velocity_y+net_acceleration_y*(1/60) #v=u+at as there are 60 frames in one second 1 frame is of 1/60 second so t=1/60
    velocity_x=velocity_x+net_acceleration_x*(1/60)

    s_x=(velocity_x*(1/60)+0.5*net_acceleration_x*((1/60)**2))*10 #s=ut+1/2at^2
    s_y=(velocity_y*(1/60)+0.5*net_acceleration_y*((1/60)**2))*10

    space_craft_y+=s_y #cordinates of spacecraft gets updated by the dispacement calculated in every frame
    space_craft_x+=s_x
    
            
    image=pygame.transform.rotate(image,orientation)
    pygame.draw.circle(window,(255,0,0),(space_craft_x,space_craft_y),2)
    pygame.draw.aaline(window,(255,255,255),(landing_gear_x_right,landing_gear_y_right),(landing_gear_right_end_x,landing_gear_right_end_y),7)
    pygame.draw.aaline(window,(255,255,255),(landing_gear_x_left,landing_gear_y_left),(landing_gear_left_end_x,landing_gear_left_end_y),7)
    window.blit(image,(space_craft_x,space_craft_y))
    pygame.draw.circle(window,(255,0,0),(center_x,center_y),2)
    pygame.draw.line(window,(255,255,255),(WINDOW_X/2-75,WINDOW_Y),(WINDOW_X/2+75,WINDOW_Y),10)
    engine_status([900,100,10])


#scope of optimizaton
def gas_exhaust():
    global gas_state

    if gas_state=='not vented':
        for i in range(30):
            gas_dis[i]=0 #keeps track of the total distance covered by the gas particle
            gas_x[i]=point_tracking(50,100,Y=False) # gas x,y cordinate 
            gas_y[i]=point_tracking(50,100,X=False)
            gas_color[i]=random.randint(50,255)
        gas_state='vented'
    

def status():
    #this part is pretty obvious
    velocity_lander=font.render(f'VELOCITY: {velocity_y:.1f}',True,(255,255,255))
    orientation_lander=font.render(f'ORIENTATION: {orientation:.1f}',True,(255,255,255))
    coordinates_lander=font.render(f'(X,Y): ({space_craft_x:.1f},{space_craft_y:.1f})M',True,(255,255,255))
    impact_velocity_lander=font.render(f'IMPACT VELOCITY: {impact_velocity:.1f}',True,(255,255,255))
    energy=font.render(f'TOTAL ENERGY: {total_energy/(10**6):.1f}MJ',True,(255,255,255))
    window.blit(velocity_lander,(textX,textY))
    window.blit(orientation_lander,(textX,textY+30))
    window.blit(coordinates_lander,(textX,textY+60))
    window.blit(impact_velocity_lander,(textX,textY+90))
    window.blit(energy,(textX,textY+120))


fps=0

initial=time.time()

thrust=0
thrust_left=0
thrust_right=0
change_orientation_left=0
change_orientation_right=0

second_count=1

movement=0

engine_active=False

_,landing_gear_y_left=point_tracking(25,100)
_,landing_gear_y_right=point_tracking(75,100)
_,center_y=point_tracking(50,50)
main_thruster_x,main_thruster_y=point_tracking(50,100)

terrain()
init()

while running:
    window.blit(bg,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        # while key is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                movement=0
                engine_active=True
                thrust=-45000
                gas_exhaust()
            if event.key == pygame.K_LEFT:
                if not(movement):change_orientation_left=0.5
            if event.key == pygame.K_RIGHT:
                if not(movement):change_orientation_right=-0.5
            if event.key == pygame.K_d:
                thrust_right=5
            if event.key == pygame.K_a:
                thrust_left=-5
            if event.key==pygame.K_s:
                thread_s=Thread(target=stabilize)
                thread_s.start()
        # when key is released
        if event.type == pygame.KEYUP:
            if event.key ==  pygame.K_UP:
                engine_active=False
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
    #scope of optimization
    if gas_state=='vented':
        for i in range(30):
            gas_dis[i]+=5 #as in every iteration the gas particles move by 5px so it is incremented by 5 everytime
            gas_y[i]+=gas_len_y[i]*cos(radians(orientation))
            gas_x[i]+=sin(radians(orientation))*gas_len_y[i]
            diff=dist([gas_x[i],gas_y[i]],[main_thruster_x,main_thruster_y])
            if lower_threshold[i]<gas_dis[i]<upper_threshold[i]: #limits the range of motion of gas particles
                if diff>random.randint(100,200):# all the gas particle will be rendered untill they have covered a distance of 30px after that the permitted distance will be randomlly decided
                    pass
                else:
                    pygame.draw.circle(window,(gas_color[i],100,100),(gas_x[i],gas_y[i]),5)
            elif gas_dis[i]>=upper_threshold[i]:
                gas_dis[i]=0 #recaliberate all the variables once the gas particle has hit the upper_threshold
                gas_x[i],gas_y[i]=point_tracking(50,100)
    space_craft_movement(space_craft,thrust/MASS,thrust_side)
    total_energy=net_energy_tracker()
    status()
    # window.blit(space_craft_180,(250,250))
    pygame.display.update()
    clock.tick(60)
    fps+=1
    
    # if int(time.time()-initial) == second_count:
    #     print(fps)
    #     fps=0
    #     second_count+=1
# or diff>random.randint(100,200)