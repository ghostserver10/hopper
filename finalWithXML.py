import sys, random
import pymunk
import pymunkoptions
import pygame
from pygame.locals import *
from pymunk import Vec2d
import time
import math
import os
import render
import xmltodict
import pymunk.pygame_util
import random
touch = 0
running = True
def detect_touching(arbiter, space, data):
    global touch
    body = arbiter.shapes[1].body
    Distance = (body.position-arbiter.contact_point_set.points[0].point_a).length
    touch = 1
    return True


def end_game(arbiter, space, data):
    global running
    if(arbiter.total_ke>30000000):
        running = False
    #running = True

def applyTorque(body,Torque):
    body.apply_force_at_local_point((0,Torque),(10.0,0))
    body.apply_force_at_local_point((0,-Torque),(-10.0,0))
    

def add_floor(space):
    static = pymunk.Body(body_type=pymunk.Body.STATIC)
    shape = pymunk.Poly(static,[(-15000,-50),(15000,-50),(15000,20),(-15000,20)])
    shape.friction = 1.0
    shape.elasticity = 0.0
    space.add(shape)

    return shape

def draw_mouse_displacement(screen,mousePos,width,height):
    pygame.draw.line(screen,(74,223,114),(width,height - 50),(mousePos,height - 50))

def to_pygame(p):
    return int(p.x), int(-p.y+600)

def drawMap(renderer,map,colorMap):
    cnt = 0
    for i in map:
        renderer.setColor(colorMap[cnt][0], colorMap[cnt][1], colorMap[cnt][2])
        renderer.drawPolygon(i[0][0],i[0][1],i[1][0],i[1][1],i[2][0],i[2][1],i[3][0],i[3][1])
        cnt+=1

def add_object(space,polygon,friction):
    static = pymunk.Body(body_type=pymunk.Body.STATIC)
    shape = pymunk.Poly(static,polygon)
    shape.friction = friction
    shape.elasticity = 0.0
    space.add(shape)

    return shape    

def add_cubic(space,pos):
    body = pymunk.Body(100, 100000)
    body.position = pos
    shape = pymunk.Poly(body,[(-50,-50),(-50,50),(50,50),(50,-50)])
    shape.friction = 3
    #space.add(body,shape)
    return body




def add_player(space,pos):
    body = pymunk.Body(100, pymunk.inf)####Body
    body.position = pos
    bodyShape = pymunk.Circle(body,20,(0,0))
    bodyShape.friction = 0.1
    bodyShape.elasticity = 0.0
    bodyShape.filter = pymunk.ShapeFilter(mask=pymunk.ShapeFilter.ALL_MASKS ^ 1)
    bodyShape.collision_type = 1
    space.add(body, bodyShape)

    contact = pymunk.Body(10, 1000)####Sole
    contact.position = (pos[0],pos[1]-100)
    contactRadius = 2

    contactShape = pymunk.Segment(contact, (0,0),(0,100),4)
    # contactShape = pymunk.Circle(contact,4,(0,0))
    contactShape.filter = pymunk.ShapeFilter(categories=1)
    contactShape.friction = 3.5
    contactShape.elasticity = 0.0
    contactShape.collision_type = 2
    space.add(contact, contactShape)

##################Adding constraints to a system################    
    slider =  pymunk.GrooveJoint(contact, body, (0,-100), (0,200), (0,0))
    space.add(slider)
    spring = pymunk.DampedSpring(contact, body, (0,0), (0,0), 100,20000,200)
    space.add(spring)

    return [body,contact,spring]

def main():

#################Initializing#############
    global touch,running
    pygame.init()
    info = pygame.display.Info()
    screen_width,screen_height = info.current_w,info.current_h
    screen_width = 1000
    screen_height = 600
    renderer = render.Render(screen_width,screen_height,False)
    screen_width,screen_height = renderer.getDimHalf()
    pygame.display.set_caption("Hopper")
    clock = pygame.time.Clock()

    space = pymunk.Space()
    screen = renderer.get_render_target()
    space.gravity = (0.0, -900.0)###################!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    
########## Adding system to the world###################
    

###################################################################

#############Collision handler##################
    ch = space.add_collision_handler(0, 2)
    ch.pre_solve = detect_touching
    ch2 = space.add_collision_handler(0, 1)
    ch2.post_solve = end_game

###############Control variables initialization##### 
    Torque = 0
    A = open('maps//1302_2.xml','r')
    All = []
    map = []
    colorMap = []
    doc = xmltodict.parse(A.read())
    for i in doc['map']['Hopper']:
        X = float(doc['map']['Hopper']['position']['x'])
        Y = float(doc['map']['Hopper']['position']['y'])
    [body,contact,spring] = add_player(space,(X,Y))
    for i in doc['map']['Polygon']:
        Temp = []
        List = [0,1,2,3]
        for j in List:
            Temp.append((float(i['vertices']['x'][j]),float(i['vertices']['y'][j])))
        friction = (float(i['params']['friction']))
        red = (float(i['params']['red']))
        green = (float(i['params']['green']))
        blue = (float(i['params']['blue']))
        colorMap.append((red,green,blue))
        add_object(space,Temp,friction)
        map.append(Temp)
    A.close()
    replay = True
    All = []
    cnt = 0
    length = 0


    
    #pygame.mouse.set_visible(0)
    NewMousePos = 0
    Sensitivity = 1/screen_width
    Random = 0
    cubic = add_cubic(space,(300,300))
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit(0)
        MousePos = pygame.mouse.get_pos()[0]
        RightButton = pygame.mouse.get_pressed()[2]
        LeftButton = pygame.mouse.get_pressed()[0]
        Jump = pygame.key.get_pressed()[K_SPACE]
        if(replay):
            pass
            #A.write(str(MousePos)+","+str(RightButton)+","+str(Jump)+"\n")
        else:
            if(cnt<flength):
                MousePos = int(All[cnt][0])
                RightButton = int(All[cnt][1])
                Jump = int(All[cnt][2])
        cnt+=1
        
        Angle = contact.angle
        AngleSpeed = contact.angular_velocity

        if(RightButton):
            body.position = (X, Y)
            contact.position = (X, Y-100)
            running = True
            body.velocity = (0,0)
            contact.velocity = (0,0)
            contact.angle = 0 
            contact.angular_velocity = 0
            NewMousePos = 0

        jump = Jump*20
        deltaVector = body.position - contact.position
        length = deltaVector.length
        NewMousePos+=pygame.mouse.get_rel()[0]
        print(body.velocity.x)
        if(touch):
            Random = random.uniform(-1,1)

            cK = (deltaVector.normalized().cross((-1,0)))
            if(cK<0.3):
                cK = 0.3
            cK = 1
            spring.damping = 200
            spring.rest_length = 100 + (20/cK + jump)
            if(LeftButton):
                spring.rest_length = 100# + (20/cK + jump)
    
            Torque = 0

        else:
            
            spring.rest_length = 100
            spring.damping = 600
    
            DesiredSpeed = (MousePos-screen_width)/screen_width
            DesiredDisplacement = (-body.velocity[0]/1000 + DesiredSpeed)
            if(abs(DesiredDisplacement)>0.98):
                DesiredDisplacement = math.copysign(0.98, DesiredDisplacement)######Linear controller
            DesiredAngle = math.asin(DesiredDisplacement)
            ErrorAngle = DesiredAngle + Angle
            Torque = ErrorAngle*1000000 + AngleSpeed*100000

        if(abs(Torque)>10000000):
            Torque = math.copysign(10000000,Torque)
        if not running:
            Torque = 0
            spring.rest_length = 100
        #Torque = 0
        #print(Torque)
        applyTorque(body,Torque)
        applyTorque(contact,-Torque)
##################################################################################
        touch = 0
        Distance = 0
        # space.debug_draw(draw_options)
        renderer.setCameraPos(body.position[0], -body.position[1])
        renderer.setCameraAffection(1)
        renderer.setColor(223, 162, 12)
        renderer.drawCircle(body.position[0],-body.position[1], 20)
        renderer.drawCircle(contact.position[0],-contact.position[1], 4)
        renderer.setColor(221, 5, 223)
        newVector = []
        # for v in [(-50,-50),(-50,50),(50,50),(50,-50)]:
        #     v = Vec2d(v[0],v[1])
        #     x,y = v.rotated(cubic.angle)
        #     newVector.append(Vec2d(cubic.position.x+x+500,300-cubic.position.y-y))
        # pygame.draw.polygon(renderer.get_render_target(),(0,255,0),newVector)
        for v in [(-50,-50),(-50,50),(50,50),(50,-50)]:
            v = Vec2d(v[0],v[1]) + cubic.position
            newVector.append(v)
        renderer.drawPolygon(newVector[0][0],newVector[0][1],newVector[1][0],newVector[1][1],newVector[2][0],newVector[2][1],newVector[3][0],newVector[3][1])
        #renderer.drawLine(body.position[0],-body.position[1],contact.position[0],-contact.position[1])
        Rotation_vector = contact.rotation_vector
        Rotation_vector.rotate_degrees(-90)
        renderer.drawLine(contact.position[0]-Rotation_vector[0]*length,-contact.position[1]+Rotation_vector[1]*length,contact.position[0],-contact.position[1])
        renderer.setColor(86, 125, 70)
        drawMap(renderer,map,colorMap)
        renderer.draw(running)
        


        draw_mouse_displacement(renderer.get_render_target(),MousePos,screen_width,screen_height)
        space.step(0.016666666666666666)
        clock.tick(60)
        #print(clock.get_fps())
        

if __name__ == '__main__':
    main()
