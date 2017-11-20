try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

import random

height = 400
width = 400
pos = [[200, 200], [240, 200], [280, 200]]
vel = 10
case = 3
score = 0
food_position = [[0, 0], [0, 0], [0,0], [0,0]]
move_dir = [3, 3, 3]

def food_generator():
	global height, width, food_position
	position1 = [random.randrange(5, height - 15, 10), random.randrange(5, width - 15, 10)]
	food_position = [position1, [position1[0] + 10, position1[1]], [position1[0] + 10, position1[1] + 10], [position1[0], position1[1] + 10]]


def draw(canvas):
    global food_position, pos
    canvas.draw_polyline(pos, 10, 'Blue')
    canvas.draw_polygon(food_position, 1, 'Green', 'Green')

def timer_handler():
    global case, vel_x, vel_y, pos
    if case == 0:
        vel_x = 0
        vel_y = vel
    elif case == 1:
        vel_x = 0
        vel_y = -vel
    elif case == 2:
        vel_x = vel
        vel_y = 0
    elif case == 3:
        vel_x = -vel
        vel_y = 0
    move()
    win_check()
    loss_check()
        
def move():
    global pos, vel_x, vel_y, width, height
    for i in range(len(pos)-1, -1, -1):
    	if i == 0:
    		move_dir[0] = case
    		pos[i][0] = pos[i][0] + vel_x
    		pos[i][1] = pos[i][1] + vel_y
    		if pos[i][0] <= 0 or pos[i][0] >= width or pos[i][1] <= 0 or pos[i][1] >= height:
    			print(pos)
    			label2.set_text('Game over')
    			timer.stop()
    	else:
    		pos[i][0] = pos[i-1][0]
    		pos[i][1] = pos[i-1][1]
    		move_dir[i] = move_dir[i-1]
    
def win_check():
    global food_position, pos, score, case
    food_centre = [(food_position[0][0] + food_position[2][0])/2, (food_position[0][1] + food_position[2][1])/2]
    if food_centre[0] == pos[0][0] and food_centre[1] == pos[0][1]:
    	score = score + 1
    	label1.set_text('Score: ' + str(score))
    	food_generator()
    	if move_dir[len(move_dir) - 1] == 0:
    		last_position = [pos[len(pos) - 1][0] , pos[len(pos) - 1][1] - 10]
    	elif move_dir[len(move_dir) - 1] == 1:
    		last_position = [pos[len(pos) - 1][0] , pos[len(pos) - 1][1] + 10]
    	elif move_dir[len(move_dir) - 1] == 2:
    		last_position = [pos[len(pos) - 1][0] - 10, pos[len(pos) - 1][1]]
    	elif move_dir[len(move_dir) - 1] == 3:
    		last_position = [pos[len(pos) - 1][0] + 10, pos[len(pos) - 1][1]]
    	dir = move_dir[len(move_dir) - 1]
    	pos.append(last_position)
    	move_dir.append(dir)

def loss_check():
	global pos
	for i in range(0, len(pos)):
		for j in range(0, len(pos)):
			if i != j:
				if pos[i][0] == pos[j][0] and pos[i][1] == pos[j][1]:
					print (pos)
					label2.set_text('Game over')
					timer.stop()

def keydown(key):
    global case
    if key == simplegui.KEY_MAP['down'] and case != 1:
        case = 0
    elif key == simplegui.KEY_MAP['up'] and case != 0:
        case = 1 
    elif key == simplegui.KEY_MAP['right'] and case != 3:
        case = 2
    elif key == simplegui.KEY_MAP['left'] and case != 2:
        case = 3

food_generator()
frame = simplegui.create_frame("Game", width, height)
frame.set_canvas_background('White')
frame.set_keydown_handler(keydown)
timer = simplegui.create_timer(100, timer_handler)
timer.start()
label3 = frame.add_label('How to play: Use arrow keys to move the snake. Do not touch the edges or you will lose.')
label1 = frame.add_label('Score: ' + str(score))
label2 = frame.add_label('')
frame.set_draw_handler(draw)
frame.start()
