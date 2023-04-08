import pygame
import time
import random
from math import sin,cos,tan,radians,sqrt
import math

pygame.init()

clock=pygame.time.Clock()

window=pygame.display.set_mode((1000,650))

running=True

space_craft=pygame.image.load('space_ship.png') #dimensions->100X100px
bg=pygame.image.load('space.png')#dimensions->1000x650

space_craft_180=pygame.transform.rotate(space_craft,-20.5)

space_craft_x=500
space_craft_y=10

velocity_y=10
velocity_x=0
impact_velocity=0
orientation=0 #degrees


ACCE_MOON=1.62

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

def point_tracking(x_off_set_val,y_off_set_val,orientation):    
    if 0>=orientation>-90:
        norientation=-orientation
        landing_gear_x=space_craft_x+(y_off_set_val*cos(radians(90-norientation)))+(x_off_set_val*cos(radians(norientation)))-(y_off_set_val*sin(radians(norientation)))
        landing_gear_y=space_craft_y+(x_off_set_val*sin(radians(norientation)))+(y_off_set_val*cos(radians(norientation))) 
    elif 0<orientation<90:
        landing_gear_x=space_craft_x+(x_off_set_val*cos(radians(orientation)))+(y_off_set_val*sin(radians(orientation)))
        landing_gear_y=space_craft_y+(y_off_set_val*cos(radians(90-orientation)))-(x_off_set_val*sin(radians(orientation)))+(y_off_set_val*cos(radians(orientation)))  
    elif -90>=orientation>-180:
        norientation=(-orientation)-90
        landing_gear_x=space_craft_x+y_off_set_val*(sqrt(2)*cos(radians((90-(2*norientation))/2)))-(x_off_set_val*sin(radians(norientation)))-(y_off_set_val*cos(radians(norientation)))
        landing_gear_y=space_craft_y+(y_off_set_val*cos(radians(90-norientation)))+(x_off_set_val*cos(radians(norientation)))-(y_off_set_val*sin(radians(norientation)))
    elif 90<=orientation<180:
        norientation=orientation-90
        landing_gear_x=space_craft_x+y_off_set_val*(cos(radians(90-norientation)))-x_off_set_val*(sin(radians(norientation)))+y_off_set_val*(cos(radians(norientation)))
        landing_gear_y=space_craft_y+y_off_set_val*(sqrt(2)*cos(radians((90-(2*norientation))/2)))-(x_off_set_val*cos(radians(norientation)))-(y_off_set_val*sin(radians(norientation)))        
    elif -180>=orientation>-270:
        norientation=(-orientation)-180
        landing_gear_x=space_craft_x+(y_off_set_val*cos(radians(norientation)))-(x_off_set_val*cos(radians(norientation)))+(y_off_set_val*sin(radians(norientation)))
        landing_gear_y=space_craft_y+y_off_set_val*(sqrt(2)*cos(radians((90-(2*norientation))/2)))-(x_off_set_val*sin(radians(norientation)))-(y_off_set_val*cos(radians(norientation)))
    elif 180<=orientation<270:
        norientation=orientation-180
        landing_gear_x=space_craft_x+y_off_set_val*(sqrt(2)*cos(radians((90-(2*norientation))/2)))-(x_off_set_val*cos(radians(norientation)))-(y_off_set_val*sin(radians(norientation)))
        landing_gear_y=space_craft_y+y_off_set_val*(cos(radians(norientation)))+(x_off_set_val*sin(radians(norientation)))-(y_off_set_val*cos(radians(norientation)))
    elif -270>=orientation>=-360:
        norientation=(-orientation)-270
        landing_gear_x=space_craft_x+(x_off_set_val*sin(radians(norientation)))+(y_off_set_val*cos(radians(norientation)))
        landing_gear_y=space_craft_y+(y_off_set_val*cos(radians(norientation)))-(x_off_set_val*cos(radians(norientation)))+(y_off_set_val*sin(radians(norientation)))
    elif 270<=orientation<=360:
        norientation=orientation-270
        landing_gear_x=space_craft_x+(y_off_set_val*cos(radians(norientation)))+(x_off_set_val*sin(radians(norientation)))-(y_off_set_val*cos(radians(norientation)))
        landing_gear_y=space_craft_y+(x_off_set_val*cos(radians(norientation)))+(y_off_set_val*sin(radians(norientation)))
    return landing_gear_x,landing_gear_y

def rotate_image_at_center(image,angle,x,y)->pygame.surface:

    rotated_image=pygame.transform.rotate(image,angle)
    new_rect=rotated_image.get_rect(center=image.get_rect(center=(x,y)).center)
    return rotated_image,new_rect

def space_craft_movement(image,landing_gear,acceleration,side_acceleration):
    global space_craft_y #all the variable are global as the scope of these varibles is outside the function
    global space_craft_x
    global velocity_y
    global velocity_x
    global orientation
    global impact_velocity
    global movement

    orientation=orientation+change_orientation_right+change_orientation_left


    #           /
    #  \    \  / *                spaceship
    #   \    \ --------
    #    \    \
    # 
    #       |*\ thrust, *-> theta = orientation, cos(theta)=along y axis, sin(theta)=along x axis
    #       |  \ 


    net_acceleration_y=ACCE_MOON+acceleration*cos(orientation*(math.pi/180))+side_acceleration*sin(orientation*(math.pi/180)) # math.pi/180->degree to radian
    net_acceleration_x=acceleration*sin(orientation*(math.pi/180))+side_acceleration*cos(orientation*(math.pi/180))

    s_x=(velocity_x*(1/60)+0.5*net_acceleration_x*((1/60)**2))*10 #s=ut+1/2at^2
    s_y=(velocity_y*(1/60)+0.5*net_acceleration_y*((1/60)**2))*10

    velocity_y=velocity_y+net_acceleration_y*(1/60) #v=u+at as there are 60 frames in one second 1 frame is of 1/60 second so t=1/60
    velocity_x=velocity_x+net_acceleration_x*(1/60)

    space_craft_y+=s_y #cordinates of spacecraft gets updated by the dispacement calculated in every frame
    space_craft_x+=s_x



    if orientation>360 or orientation<-360:
        orientation=0 # recalibrate oritentation after exceeding 360 or -360 back to 0 
    if space_craft_y>500:
        space_craft_y=500
        if movement==0:             # After hitting the ground if movement is 0 impact velocity is registered and movement is assigned 1 then if any arrow key is pressed except for down then movement becomes 0 again
            impact_velocity=velocity_y
            movement=1
        velocity_y=0  # velocity becomes zero as the craft has hit the ground
        velocity_x=0

    image=pygame.transform.rotate(image,orientation)
    landing_gear=pygame.transform.rotate(landing_gear,orientation)
    landing_gear_x_left,landing_gear_y_left=point_tracking(25,100,orientation)
    landing_gear_x_right,landing_gear_y_right=point_tracking(75,100,orientation)
    pygame.draw.circle(window,(255,0,0),(space_craft_x,space_craft_y),2)
    len_of_landing_gear=60
    landing_gear_angle_right=radians(45+orientation)
    landing_gear_angle_left=radians(-45+orientation)
    pygame.draw.line(window,(255,255,255),(landing_gear_x_right,landing_gear_y_right),(landing_gear_x_right+(len_of_landing_gear*sin(landing_gear_angle_right)),landing_gear_y_right+(len_of_landing_gear*cos(landing_gear_angle_right))),7)
    pygame.draw.line(window,(255,255,255),(landing_gear_x_left,landing_gear_y_left),(landing_gear_x_left+(len_of_landing_gear*sin(landing_gear_angle_left)),landing_gear_y_left+(len_of_landing_gear*cos(landing_gear_angle_left))),7)
    window.blit(image,(space_craft_x,space_craft_y))


#scope of optimizaton
def gas_exhaust():
    global gas_state

    if gas_state=='not vented':
        for i in range(30):
            gas_len_x.append(0)
            gas_len_y.append(5)
            gas_dis.append(0) #keeps track of the total distance covered by the gas particle
            lower_threshold.append(i*5) 
            upper_threshold.append(50+(i*5))
            gas_x.append(space_craft_x+50) # gas x,y cordinate 
            gas_y.append(space_craft_y+100)
            gas_color.append(random.randint(50,255))
        gas_state='vented'
    

def status():
    #this part is pretty obvious
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

while running:
    window.blit(bg,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        # while key is pressed
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
        # when key is released
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
    #scope of optimization
    if gas_state=='vented':
        for i in range(30):
            gas_dis[i]+=5 #as in every iteration the gas particles move by 5px so it is incremented by 5 everytime
            gas_y[i]+=gas_len_y[i]
            gas_x[i]+=tan(orientation*(math.pi/180))*gas_len_y[i]
            if lower_threshold[i]<gas_dis[i]<upper_threshold[i]: #limits the range of motion of gas particles
                if gas_y[i]-space_craft_y-30<0 or gas_y[i]-space_craft_y>random.randint(100,200):# all the gas particle will be rendered untill they have covered a distance of 30px after that the permitted distance will be randomlly decided
                    pass
                else:
                    pygame.draw.circle(window,(gas_color[i],100,100),(gas_x[i],gas_y[i]),5)
            elif gas_dis[i]>=upper_threshold[i]:
                gas_dis[i]=0 #recaliberate all the variables one the gas particle has hit the upper_threshold
                gas_x[i],gas_y[i]=space_craft_x+50,space_craft_y+100

    
   
    space_craft_movement(space_craft,landing_gear,thrust,thrust_side)
    status()
    # window.blit(space_craft_180,(250,250))
    pygame.display.update()
    clock.tick(60)
    fps+=1
    
    # if int(time.time()-initial) == second_count:
    #     print(fps)
    #     fps=0
    #     second_count+=1
