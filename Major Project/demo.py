import os
import random
import time
from tkinter import messagebox
from tkinter import *

#import the Turtle module
import turtle

import pygame

pygame.mixer.init()

# Import the other parts of your code here...

# Define a function to play background music
def play_background_music():
    pygame.mixer.music.load("song.mp3")
    pygame.mixer.music.play(-1)  # -1 means play indefinitely

# Start playing background music
play_background_music()

turtle.fd(0)
#set the animations speed to the maximum
turtle.speed(0)
#change the background color
turtle.bgcolor("black")
#change the window title
turtle.title("SPACESHOOTEER")
#hide the default turtle
turtle.ht()
#this save memory
turtle.setundobuffer(1)
#this speeds up drawing
turtle.tracer(0)


class Sprite(turtle.Turtle):
    def __init__(self,spriteshape, color, startx, starty):
        turtle.Turtle.__init__(self, shape = spriteshape)
        self.speed(0)
        self.penup()
        self.color(color)
        self.fd(0)
        self.goto(startx, starty)
        self.speed = 1

    def move(self):
        self.fd(self.speed)

        #boundary detection
        if self.xcor() > 280:
            self.setx(280)
            self.rt(60)

        if self.xcor() < -280:
            self.setx(-280)
            self.rt(60)

        if self.ycor() > 280:
            self.sety(280)
            self.rt(60)

        if self.ycor() < -280:
            self.sety(-280)
            self.rt(60)

    def is_collision(self, other):
        if(self.xcor() >= (other.xcor() -20)) and \
        (self.xcor() <= (other.xcor() +20)) and  \
        (self.ycor() >= (other.ycor() -20)) and \
        (self.ycor() <= (other.ycor() +20)):
            return True
        else:
            return False
            
class Player(Sprite):
    def __init__(self,spriteshape, color, startx, starty):
        Sprite.__init__(self,spriteshape, color, startx, starty)
        self.shapesize(stretch_wid = 1, stretch_len = 1.5, outline = None)
        self.speed = 1
        self.lives = 3

    def turn_left(self):
        self.lt(45)


    def turn_right(self):
        self.rt(45)

    def accelerate(self):
        self.speed += 1

    def decelerate(self):
        self.speed -= 1


class Enemy(Sprite):
    def __init__(self,spriteshape, color, startx, starty):
        Sprite.__init__(self,spriteshape, color, startx, starty)
        self.speed = 4
        self.setheading(random.randint(0,360))


class Ally(Sprite):
    def __init__(self,spriteshape, color, startx, starty):
        Sprite.__init__(self,spriteshape, color, startx, starty)
        self.speed = 8
        self.setheading(random.randint(0,360))

    def move(self):
        self.fd(self.speed)

        #boundary detection
        if self.xcor() > 280:
            self.setx(280)
            self.lt(60)

        if self.xcor() < -280:
            self.setx(-280)
            self.lt(60)

        if self.ycor() > 280:
            self.sety(280)
            self.lt(60)

        if self.ycor() < -280:
            self.sety(-280)
            self.lt(60)


class Missile(Sprite):
    def __init__(self,spriteshape, color, startx, starty):
        Sprite.__init__(self,spriteshape, color, startx, starty)
        self.shapesize(stretch_wid = 0.3, stretch_len = 0.4, outline=None)
        self.speed = 20
        self.status = "ready"
        self.goto(-1000, 1000)

    def fire(self):
        if self.status == "ready":
            self.goto(player.xcor(), player.ycor())
            self.setheading(player.heading())
            self.status = "firing"

    def move(self):

        if self.status == "ready":
            self.goto(-1000, 1000)

        if self.status == "firing":
            self.fd(self.speed)

        #boder check
        if self.xcor() < -290 or self.xcor() > 290 or \
           self.ycor() < -290 or self.ycor() > 290:
           self.goto(-1000, 1000)
           self.status = "ready"
        
class Particle(Sprite):
    def __init__(self,spriteshape, color, startx, starty):
        Sprite.__init__(self,spriteshape, color, startx, starty)
        self.shapesize(stretch_wid = 0.2, stretch_len = 0.2, outline=None)
        self.goto(-1000, -1000)
        self.frame = 0

    def explode(self, startx, starty):
        self.goto(startx, starty)
        self.setheading(random.randint(0, 360))

    def move(self):
        if self.frame > 0:
            self.fd(10)
            self.frame += 1

        if self.frame < 20:
            self.frame = 0
            self.goto(-1000, -1000)
            
class Game():
    def __init__(self):
        global playerName
        global bg
        self.level = 1
        self.score = 0
        self.lives  = 3
        self.state = "playing"
        self.pen = turtle.Turtle()
        self.l = turtle.Turtle()
        self.s=1
        self.control2=0 #controlling level2 message variable
        self.control3=0 #controlling level 3 message 
#name
        self.n=turtle.Turtle()
        self.lives = 3
        self.currentLevel=1
        self.level=turtle.Turtle()

    def draw_border(self):
        #draw border
        self.pen.speed(0)
        self.pen.color("red")
        self.pen.pensize(3)
        self.pen.penup()
        self.pen.goto(-300,300)
        self.pen.pendown()
        for side in range(4):
            self.pen.fd(600)
            self.pen.rt(90)
        self.pen.penup()
        self.pen.ht()
        self.pen.pendown()

        

    def show_status(self):
     #name
        """self.p1=playerName.upper()
        self.n.hideturtle()
        
        """
        
        self.n.color("red")
        self.n.penup()
        self.n.hideturtle()
        
        self.pen.undo()
        self.level.undo()
        self.level.penup()
        self.level.hideturtle()
        self.l.undo()
        self.l.color("red")
        self.level.color("blue")
        self.l.hideturtle()
        msg = "SCORE: %s" %(self.score)
        msg2= "LIVES: %s" %(self.lives)
        msg3="LEVEL : %s" %(self.currentLevel)
        self.pen.penup()
        self.n.goto(-370,310)
        self.pen.goto(-300, 310)
        self.n.write(playerName.upper(),font = ("Arial", 16, "normal"))
        self.pen.write(msg, font = ("Arial", 16, "normal"))
        self.l.penup()
        self.l.goto(200, 310)
        self.level.goto(-50,310)
        self.l.write(msg2, font = ("Arial", 16, "normal"))
        if self.score>=0 and self.score<40:
            if self.s==1:
                messagebox.showinfo("Level 1","THIS IS LEVEL 1")
            self.level.write(msg3, font = ("Arial", 16, "normal"))
            self.s=0
        if self.score>=40 and self.score<90:
            if self.score>=50 and self.score<61:
                if self.control2==0:
                    messagebox.showinfo("Level 2","THIS IS LEVEL 2")
                    player.color="red"
                    bg.shape(img4)
                self.control2=1
            self.currentLevel=2
            self.level.write(msg3, font = ("Arial", 16, "normal"))
        if self.score>=90 and self.score<140:
            if self.score>=100 and self.score<111:
                if self.control3==0:
                    messagebox.showinfo("Level 3","THIS IS LEVEL 3")
                    bg.shape(img5)
                self.control3=1
            self.currentLevel=3
            self.level.write(msg3, font = ("Arial", 16, "normal"))
        
        if game.lives==0:
            messagebox.showinfo("BETTER LUCK NEXT TIME"," GAME OVER :)")
         
            turtle.bye()
        

    

def help():
    messagebox.showinfo("GAME INFO"," 1-Press right and left arrow keys to move the turtle left and right respectively .2-Press space bar to fire Press UP and DOWN to increase the speed of turtle .3-If you shoot the DEVIL successfully then you earn a score. 4-If you SHOOT ANGEL then your lives will decrease you have only 3 lives in game is you will use your all 3 lives then the game is over. 5- However, you can play the game again by reopening it again ")
    

 #game is starting
playerName=turtle.textinput("Name","Enter your gaming name")
s=0
messagebox.showinfo("Play the game"," The game will start now")
s=1
if(s==1):       
        #create game object
    game = Game()

        #draw the game border
    game.draw_border()

        #show the game status
    game.show_status()

        #Implementing pictures
    screen=turtle.Screen()
    img1="my angel.gif"
    img2="devils.gif"
    img3="bg1.gif"
    img4="bg2.gif"
    img5="bg3.gif"
    bg=turtle.Turtle()

        #screen.addshape(img) #img=Figher
    screen.addshape(img1)#img1=Red Invader
    screen.addshape(img2)#img2=Green Invader
    screen.addshape(img3)
    screen.addshape(img4)
    screen.addshape(img5)
    bg.shape(img3)
    bg.goto(0,0)
        #create my sprites
    player = Player("turtle", "gold", 0, 0)
        #enemy = Enemy("circle", "red",-100, 0)
    missile = Missile("triangle", "yellow", 0, 0)
        #ally = Ally("square", "blue", 0, 0)
    loopControl=1
    e=0
    f=0
    allino=2
    allies = []
    for i in range(allino):
        allies.append(Ally(img1, "blue", 0, 0))


    enemies=[]
    for i in range(8):
        enemies.append(Enemy(img2, "red",-100, 0))


    particles = []
    for i in range(20):
        particles.append(Particle("circle", "white",0, 0))


        #keyboard binding
    turtle.onkey(player.turn_left, "Left")
    turtle.onkey(player.turn_right, "Right")
    turtle.onkey(player.accelerate, "Up")
    turtle.onkey(player.decelerate, "Down")
    turtle.onkey(missile.fire, "space")
    turtle.listen()

        #main game loop
    textPen=turtle.Turtle()
    textPen.penup()
    textPen.color("white")
    textPen.goto(-650,50)
    t="Press H To See The Help Menu"
    textPen.write(t,font = ("Arial", 16, "normal"))
    textPen.hideturtle()
    
    
    while True:
        turtle.update()
        time.sleep(0.03)
        player.move()
        missile.move()
        
        
        turtle.onkey(help, "h")

        if(e==0):
            if game.score>=50 and game.score<100:
                allino=2
                loopControl=0
                e+=1
        if(f==0):
            if game.score>=100 and game.score<150:
                allino=3
                loopControl=0
                f+=1
        if loopControl==0:
            for i in range(allino):
                allies.append(Ally(img1, "blue", 0, 0))
            loopControl+=1        


        for enemy in enemies:
            enemy.move()

                #check for a colision with the player
            if player.is_collision(enemy):
                x = random.randint(-250, 250)
                y = random.randint(-250, 250)
                enemy.goto(x,y)
                    
                     

                #check for a collision between the missile and the enemy
            if missile.is_collision(enemy):
                x = random.randint(-250, 250)
                y = random.randint(-250, 250)
                enemy.goto(x,y)
                missile.status = "ready"
                    #increase the score
                game.score += 10
                game.show_status()
                    #do the explosion
                for particle in particles:
                    particle.explode(missile.xcor(), missile.ycor())
                    particle.setheading(random.randint(0,360))
        for ally in allies:
            ally.move()

             #check for a collision between the missile and the ally
            if missile.is_collision(ally):
                x = random.randint(-250, 250)
                y = random.randint(-250, 250)
                enemy.goto(x,y)   
                missile.status = "ready"
                    #increase the score
                game.lives -= 1
                game.show_status()
                
        for particle in particles:
            particle.move()

            #check for a colision with the player
        if player.is_collision(enemy):
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            enemy.goto(x,y)
            

            #check for a collision between the missile and the enemy
        if missile.is_collision(enemy):
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            enemy.goto(x,y)
            missile.status = "ready"
                #increase the score
            game.score += 10
            game.show_status()
                

            #check for a collision between the missile and the ally
        if missile.is_collision(ally):
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            enemy.goto(x,y)   
            missile.status = "ready"
                #increase the score
            game.lives -= 1
            game.show_status() 
           
                
                
                    
          

            

    delay = raw_input("press enter to finish.>")



