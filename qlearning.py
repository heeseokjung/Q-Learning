import sys
import time
import random
import progressbar
from tkinter import *

# Global variables
map_size = 5
start = 0
bonus = 1.
decay = .9
max_iter = 10000

tk = None
canvas = None

def valid(row, col):
    global map_size
    if row < 0 or col < 0:
        return False
    if row >= map_size or col >= map_size:
        return False
    return True

def succ(map, state):
    global map_size
    row = state // map_size
    col = state % map_size
    
    while True:
        action = random.randint(0, 3)
        if action == 0 and valid(row-1, col):   # Up
            return action, (row-1)*map_size + col
        elif action == 1 and valid(row+1, col): # Down
            return action, (row+1)*map_size + col
        elif action == 2 and valid(row, col-1): # Left
            return action, row*map_size + col-1
        elif action == 3 and valid(row, col+1): # Right
            return action, row*map_size + col+1

def set_gui(map):
    global tk
    tk = Tk()
    tk.title('Q-learing process')
    tk.resizable(False, False)

    width, height = 550, 550
    x, y = (tk.winfo_screenwidth() - width) / 2, \
           (tk.winfo_screenheight() - height) / 2
    tk.geometry('%dx%d+%d+%d' % (width, height, x, y))

    global canvas
    canvas = Canvas(tk, width=width, height=height, bg='white')
    canvas.pack()

    for row in range(map_size):
        for col in range(map_size):
            state = row*map_size + col
            if map[state] == 'B':
                canvas.create_rectangle(col*100, row*100, col*100 + 100, row*100 + 100, fill='black')
            elif map[state] == 'T':
                canvas.create_rectangle(col*100, row*100, col*100 + 100, row*100 + 100, fill='yellow')
            elif map[state] == 'G':
                canvas.create_rectangle(col*100, row*100, col*100 + 100, row*100 + 100, fill='red')
            else:
                canvas.create_rectangle(col*100, row*100, col*100 + 100, row*100 + 100)

def draw_agent(state, delay):
    global map_size
    row = state // map_size
    col = state % map_size

    global tk, canvas
    agent = canvas.create_rectangle(col*100, row*100, col*100 + 100, row*100 + 100, fill='green')
    tk.update()
    time.sleep(delay)

    canvas.delete(agent)
    tk.update()

def qlearning(map, qtable):
    global start
    global bonus, decay
    global max_iter
    global tk, canvas

    state = start
    bar = progressbar.ProgressBar()
    for i in bar(range(max_iter)):
        draw_agent(state, 0.01)

        # Randomly choose next action
        action, next_state = succ(map, state)
        
        reward = 0.
        if map[next_state] == 'B':   # Bomb point
            reward = -100.
        elif map[next_state] == 'T': # Bonus point
            reward = bonus
        elif map[next_state] == 'G': # Goal point
            reward = 100.

        # Update Q-value
        qtable[state][action] = reward + decay*max(qtable[next_state])

        if map[next_state] == 'B' or map[next_state] == 'G':
            state = start
        else:
            state = next_state

def argmax(list):
    idx, mx = 0, list[0]
    for i, num in enumerate(list):
        if mx < num:
            idx = i
            mx = num
    return idx

def record_path(qtable):
    global map_size
    path = [0 for i in range(map_size * map_size)]

    for i, actions in enumerate(qtable):
        path[i] = argmax(actions)

    return path

def read_input(filename):
    global map_size, start
    map = []

    with open(filename, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
           
            for i in range(map_size):
                map.append(line[i])
                if line[i] == 'S':
                    start = len(map)-1

    return map

def visualize_output(map, qtable, path):
    global tk, canvas
    global start, map_size

    state = start
    while True:
        draw_agent(state, 0.5)

        if map[state] == 'G':
            break

        row = state // map_size
        col = state % map_size
        if path[state] == 0:   # UP
            state = (row-1)*map_size + col
        elif path[state] == 1: # Down
            state = (row+1)*map_size + col
        elif path[state] == 2: # Left
            state = row*map_size + col-1
        elif path[state] == 3: # Right
            state = row*map_size + col+1

def main():
    global map_size
    map = read_input('input.txt')
    qtable = [[0 for j in range(4)] \
              for i in range(map_size * map_size)]

    global tk, canvas
    set_gui(map)

    qlearning(map, qtable)
    path = record_path(qtable)

    visualize_output(map, qtable, path)
    
    tk.mainloop()

if __name__ == '__main__':
    main()