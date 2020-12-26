#CS133 Test 11
#Raafi Rahman

#Pong

from tkinter import *
from random import choice
import time as tm

def clock():
    return tm.perf_counter()

#Score
p1Score = 0
p2Score = 0
winner = False

# Ball and its velocity
ball, velx, vely = None, 100, 100
field = None
previousTime = 0
keyboard = {'Up': False, 'Down': False, 'W': False, 'S': False}

paddles = []

# NEW: checks which side of the paddle was hit
def hitPaddle(paddle, x0, y0, x1, y1):
    bx0, by0, bx1, by1 = field.coords(paddle)
    if bx0 <= x1 <= bx1 and by0 <= y1 <= by1:
        if y0 < by0:
            return 'top'
        elif y0 > by1:
            return 'bottom'
        elif x0 < bx0:
            return 'left'
        else:
            return 'right'
    else:
        return 'no-collision'

# returns position of the *center* of the ball
x1, y1, x2, y2 = 0, 0, 0, 0
def ballPosition():
    x1, y1, x2, y2 = list(field.coords(ball))
    return [(x1+x2)/2, (y1+y2)/2]

def startGame():
    global field, ball, previousTime, paddle1, paddle2, score
    root = Tk()
    root.title('Pong')
    root['bg'] = 'black'
    root.geometry("520x342")
    score = Label(text = "Score: {0} - {1}".format(p1Score, p2Score), bg = 'black', fg = 'white', pady = 5 )
    score.pack()
    field = Canvas(root, width=500, height=300, bg='black')
    field.pack()
    # place ball at random
    upperLeftX = choice(list(range(290)))
    upperLeftY = choice(list(range(290)))
    ball = field.create_oval(upperLeftX, upperLeftY, upperLeftX+10, upperLeftY+10, fill='white')
  
    # NEW: add paddles
    paddle1 = field.create_rectangle(10, 100, 20, 150, fill='white')
    paddles.append(paddle1)
    paddle2 = field.create_rectangle(480, 100, 490, 150, fill='white')
    paddles.append(paddle2)

    def key_press(event):
        if event.keysym == 'Up':
            keyboard['Up'] = True
        if event.keysym == 'Down':
            keyboard['Down'] = True
        if event.keysym == 'w':
            keyboard['W'] = True
        if event.keysym == 's':
            keyboard['S'] = True
    
    def key_release(event):
        if event.keysym == 'Up':
            keyboard['Up'] = False
        if event.keysym == 'Down':
            keyboard['Down'] = False
        if event.keysym == 'w':
            keyboard['W'] = False
        if event.keysym == 's':
            keyboard['S'] = False

    root.bind("<Key>", key_press) 
    root.bind("<KeyRelease>", key_release) 
    previousTime = clock()
    animate()

def animate():
    global vely1, vely2, p1Score, p2Score, ball, velx, vely, score, winner
    
    vely1 = 0
    vely2 = 0

    # === Measuring the elapsed time more accurately ===
    global previousTime
    time = clock()
    dt = time - previousTime # dt is the time elapsed since the previous update
    previousTime = time      # ball displacement is vel*dt

    # === Process keyboard events ===
    acceleration = 300
    if keyboard['Up']:
        vely2 = -200
    if keyboard['Down']:
        vely2 = 200
    if keyboard['W']:
        vely1 = -200
    if keyboard['S']:
        vely1 = 200

    # === Update the game state ===
    x, y = ballPosition()

    #If player 1 scores
    if x >= 490:
        if winner == True:
            p1Score = 0
            p2Score = 0
            winner = False
        p1Score += 1
        field.delete(ball)
        upperLeftX = 250
        upperLeftY = 150
        velx = 100
        vely = choice(range(-100, -10))
        score['text'] = "Score: {0} - {1}".format(p1Score, p2Score)
        ball = field.create_oval(upperLeftX, upperLeftY, upperLeftX+10, upperLeftY+10, fill='white')
    
    #If player 2 scores
    elif x <= 10:
        if winner == True:
            p1Score = 0
            p2Score = 0
            winner = False
        p2Score += 1
        field.delete(ball)
        upperLeftX = 250
        upperLeftY = 150
        velx = -100
        vely = choice(range(10, 100))
        score['text'] = "Score: {0} - {1}".format(p1Score, p2Score)
        ball = field.create_oval(upperLeftX, upperLeftY, upperLeftX+10, upperLeftY+10, fill='white')

    #If player 1 wins
    if p1Score == 11:
        winner = True

    #If player 2 wins
    if p2Score == 11:
        winner = True

    # collisions with walls
    if x+velx*dt>=500 or x+velx*dt<0:
        velx *= -1 
    if y+vely*dt>=300 or y+vely*dt<0:
        vely *= -1 
   
    # NEW: collisions with paddles
    x1 = x + velx*dt
    y1 = y + vely*dt
    for paddle in paddles:
        res = hitPaddle(paddle, x, y, x1, y1)
        if res == 'left' or res == 'right':
            velx *= -1.1 # dissipating collisions
        elif res == 'top' or res == 'bottom':
            vely *= -1.1 # dissipating collisions

    field.move(ball, velx*dt, vely*dt) 

    if field.coords(paddle1)[1] <= 4:
        field.move(paddle1, 0, 20*dt)
    elif field.coords(paddle1)[3] >= 300:
        field.move(paddle1, 0, -20*dt)
    else:
        field.move(paddle1, 0, vely1*dt)

    if field.coords(paddle2)[1] <= 4:
        field.move(paddle2, 0, 20*dt)
    elif field.coords(paddle2)[3] >= 300:
        field.move(paddle2, 0, -20*dt)
    else:
        field.move(paddle2, 0, vely2*dt)

    field.after(20, animate)



startGame()
mainloop()

