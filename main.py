import tkinter
import time
from queue import PriorityQueue
from tkinter import Tk, Canvas, BOTTOM
import random

import bottom as bottom
import canvas as canvas

A_D_C_ = '#A2D3C2'
#start = (3, 1)
start = None
# 17
#end = (23, 48)
end = None

#functions to find end and start point of maze
def findStartPoint(maze):
    x = 0
    y = 0
    for row in maze:
        y=0
        for col in row:
            if col == 's':
                return (x, y)
            y += 1
        x += 1

def findEndPoint(maze):
    x = 0
    y = 0
    for row in maze:
        y = 0
        for col in row:
            if col == 'e':
                return (x, y)
            y += 1
        x += 1

# function to draw the maze
def drawMaze(maze, canvas: object):
    x1 = 0
    y1 = 0
    x2 = 30
    y2 = 30
    x = 0
    y = 0
    for row in maze:
        x1 = 0
        x2 = 30
        y = 0
        for i in row:
            if i == '+':
                canvas.create_rectangle(x1, y1, x2, y2, fill='#22333B', outline='black')
            elif i == 's':
                canvas.create_text(x1 - 25, y1 + 32, anchor="nw", angle=90, text="START", fill="white",
                                   font=('Helvetica 15 bold'))
            elif i == 'e':
                canvas.create_text(x1 - 60, y1 , text="FIN", fill="white", font=('Helvetica 15 bold'))
                canvas.create_text(x1 - 60, y1 + 20, text="ISH", fill="white", font=('Helvetica 15 bold'))

            else:
                canvas.create_rectangle(x1, y1, x2, y2, fill='white', outline='black')
            x1 = x1 + 30
            x2 = x2 + 30
            y = y + 1

        x = x + 1
        y1 = y1 + 30
        y2 = y2 + 30
    canvas.create_text(x1 - 800, y1 + 40, text="Main Menu", fill="Red", font=('Helvetica 30 bold'))
    canvas.create_text(x1 - 300, y1 + 40, text="NOTE: please run single algo at a time", fill="Red", font=('Helvetica 15 bold'))

def get_maze():
    with open("mazetrix.txt") as f:
        lines = f.read().splitlines()
        return [line.strip() for line in lines]


# function to draw visited node/child in maze
def drawChild(canvas, x, y):
    x = x * 30
    y = y * 30
    canvas.create_rectangle(y, x, y + 30, x + 30, fill=('#A2D3C2'), outline='black')
    root.update()
    time.sleep(0.010)


# draw final path from start to end point
def drawPath(canvas, x, y):
    X = x * 30
    Y = y * 30
    # outline = '#CBA328'
    canvas.create_rectangle(Y, X, Y + 30, X + 30, fill='#CBA328', outline='black')
    # if matrix[x][y+1]==' ' or matrix[x][y-1]==' ':
    #     if matrix[x][y + 1] == ' ':
    #         X = (x) * 30
    #         Y = (y+1) * 30
    #     else:
    #         X = (x) * 30
    #         Y = (y - 1) * 30
    #     canvas.create_rectangle(Y, X, Y + 30, X + 30, fill='#CBA328', outline='#CBA328')
    root.update()
    time.sleep(0.010)


# function to trace back the final path
def TracePathBack(algoPath):
    cell = end
    path = {}
    while cell != start:
        path[algoPath[cell]] = cell
        cell = algoPath[cell]
    cell = end
    drawPath(canvas, cell[0], cell[1])

    while cell != start:
        index = path[algoPath[cell]]
        drawPath(canvas, index[0], index[1])
        cell = algoPath[cell]


# bfs implementation
def bfs(maze, canvas):
    queue = [start]
    explored = [start]
    drawChild(canvas, 3, 1)
    bfspath = {}
    while len(queue) > 0:
        currCell = queue.pop(0)
        if matrix[currCell[0]][currCell[1]] == 'e':
            drawChild(canvas, currCell[0], currCell[1])
            #bfspath[currCell] = (22, 17)
            break

        if matrix[currCell[0]][currCell[1]] != '+':
            # check up
            if currCell[0] > 0:
                if matrix[currCell[0] - 1][currCell[1]] == ' ' or matrix[currCell[0] - 1][currCell[1]] == 'e':
                    childcell = (currCell[0] - 1, currCell[1])
                    if childcell not in explored:
                        queue.append(childcell)
                        explored.append(childcell)
                        bfspath[childcell] = currCell
                        drawChild(canvas, currCell[0] - 1, currCell[1])

            # check down
            if matrix[currCell[0] + 1][currCell[1]] == ' ' or matrix[currCell[0] + 1][currCell[1]] == 'e':
                childcell = (currCell[0] + 1, currCell[1])
                if childcell not in explored:
                    queue.append(childcell)
                    explored.append(childcell)
                    bfspath[childcell] = currCell
                    drawChild(canvas, currCell[0] + 1, currCell[1])

            # check right
            if matrix[currCell[0]][currCell[1] + 1] == ' ' or matrix[currCell[0]][currCell[1] + 1] == 'e':
                childcell = (currCell[0], currCell[1] + 1)
                if childcell not in explored:
                    queue.append(childcell)
                    explored.append(childcell)
                    bfspath[childcell] = currCell
                    drawChild(canvas, currCell[0], currCell[1] + 1)

            # check left
            if currCell[1] > 0:
                if matrix[currCell[0]][currCell[1] - 1] == ' ' or matrix[currCell[0]][currCell[1] - 1] == 'e':
                    childcell = (currCell[0], currCell[1] - 1)
                    if childcell not in explored:
                        queue.append(childcell)
                        explored.append(childcell)
                        bfspath[childcell] = currCell
                        drawChild(canvas, currCell[0], currCell[1] - 1)
    canvas.create_text(start[0] * 30, (start[1] * 30) - 60, text="S", fill="black", font=('Helvetica 15 bold'))
    TracePathBack(bfspath)


def dfs(maze, canvas):
    queue = [start]
    explored = [start]
    drawChild(canvas, 3, 1)
    dfspath = {}
    while len(queue) > 0:
        currCell = queue.pop()
        if matrix[currCell[0]][currCell[1]] == 'e':
            drawChild(canvas, currCell[0], currCell[1])
            #dfspath[currCell] = (22, 17)
            break

        if matrix[currCell[0]][currCell[1]] != '+':
            # check up
            if currCell[0] > 0:
                if matrix[currCell[0] - 1][currCell[1]] == ' ' or matrix[currCell[0] - 1][currCell[1]] == 'e':
                    childcell = (currCell[0] - 1, currCell[1])
                    if childcell not in explored:
                        queue.append(childcell)
                        explored.append(childcell)
                        dfspath[childcell] = currCell
                        drawChild(canvas, currCell[0] - 1, currCell[1])

            # check down
            if matrix[currCell[0] + 1][currCell[1]] == ' ' or matrix[currCell[0] + 1][currCell[1]] == 'e':
                childcell = (currCell[0] + 1, currCell[1])
                if childcell not in explored:
                    queue.append(childcell)
                    explored.append(childcell)
                    dfspath[childcell] = currCell
                    drawChild(canvas, currCell[0] + 1, currCell[1])

            # check right
            if matrix[currCell[0]][currCell[1] + 1] == ' ' or matrix[currCell[0]][currCell[1] + 1] == 'e':
                childcell = (currCell[0], currCell[1] + 1)
                if childcell not in explored:
                    queue.append(childcell)
                    explored.append(childcell)
                    dfspath[childcell] = currCell
                    drawChild(canvas, currCell[0], currCell[1] + 1)

            # check left
            if currCell[1] > 0:
                if matrix[currCell[0]][currCell[1] - 1] == ' ' or matrix[currCell[0]][currCell[1] - 1] == 'e':
                    childcell = (currCell[0], currCell[1] - 1)
                    if childcell not in explored:
                        queue.append(childcell)
                        explored.append(childcell)
                        dfspath[childcell] = currCell
                        drawChild(canvas, currCell[0], currCell[1] - 1)
    canvas.create_text(start[0] * 30, (start[1] * 30) - 60, text="S", fill="black", font=('Helvetica 15 bold'))

    TracePathBack(dfspath)

#node to store location of cell and cost/heuristic
class node:
    def __init__(self):
        self.loc = None
        self.cost = 0

#priority queue implementation to prioritize nodes on the basis of cost/heuristic
class myPriorityQueue:
    def __init__(self):
        self.queue = []

    def isEmpty(self):
        if not self.queue:
            return True
        else:
            return False

    def checkBetterNode(self, loc, cost):
        for node in self.queue:
            if node.loc == loc:
                if node.cost < cost:
                    return True
                else:
                    return False
        return False

    def inQueue(self, loc):
        if loc in self.queue:
            return True
        else:
            return False

    def pop(self):
        return self.queue.pop(0)

    def push(self, location, cost):
        index = 0
        mynode = node()
        mynode.loc = location
        mynode.cost = cost
        for i in self.queue:
            if cost < i.cost:
                self.queue.insert(index, mynode)
                index += 1
                return
            else:
                index += 1
        self.queue.append(mynode)

    def print(self):
        print(self.queue)


# ucs implementation
def ucs(maze, canvas):
    pQueue = myPriorityQueue()
    pQueue.push(start, 0)

    explored = [start]
    drawChild(canvas, 3, 1)
    ucsPath = {}
    while pQueue.isEmpty() == False:
        node = pQueue.pop()
        currCell = node.loc
        if matrix[currCell[0]][currCell[1]] == 'e':
            drawChild(canvas, currCell[0], currCell[1])
            #ucsPath[currCell] = (22, 17)
            break

        if matrix[currCell[0]][currCell[1]] != '+':
            # check up
            if currCell[0] > 0:
                if matrix[currCell[0] - 1][currCell[1]] == ' ' or matrix[currCell[0] - 1][currCell[1]] == 'e':
                    childcell = (currCell[0] - 1, currCell[1])
                    if childcell not in explored:
                        pQueue.push(childcell, node.cost + 1)
                        # frontier.append(childcell)
                        explored.append(childcell)
                        ucsPath[childcell] = currCell
                        drawChild(canvas, currCell[0] - 1, currCell[1])

            # check down
            if matrix[currCell[0] + 1][currCell[1]] == ' ' or matrix[currCell[0] + 1][currCell[1]] == 'e':
                childcell = (currCell[0] + 1, currCell[1])
                if childcell not in explored:
                    pQueue.push(childcell, node.cost + 1)
                    explored.append(childcell)
                    ucsPath[childcell] = currCell
                    drawChild(canvas, currCell[0] + 1, currCell[1])

            # check right
            if matrix[currCell[0]][currCell[1] + 1] == ' ' or matrix[currCell[0]][currCell[1] + 1] == 'e':
                childcell = (currCell[0], currCell[1] + 1)
                if childcell not in explored:
                    pQueue.push(childcell, node.cost + 1)
                    explored.append(childcell)
                    ucsPath[childcell] = currCell
                    drawChild(canvas, currCell[0], currCell[1] + 1)

            # check left
            if currCell[1] > 0:
                if matrix[currCell[0]][currCell[1] - 1] == ' ' or matrix[currCell[0]][currCell[1] - 1] == 'e':
                    childcell = (currCell[0], currCell[1] - 1)
                    if childcell not in explored:
                        pQueue.push(childcell, node.cost + 1)
                        explored.append(childcell)
                        ucsPath[childcell] = currCell
                        drawChild(canvas, currCell[0], currCell[1] - 1)
    canvas.create_text(start[0] * 30, (start[1] * 30) - 60, text="S", fill="black", font=('Helvetica 15 bold'))
    TracePathBack(ucsPath)

#function to calculate heurisitc
def getHeuristic(location, goal):
    return abs(location[0] - goal[0]) + abs(location[1] - goal[1])


# greedy implementation
def greedy(maze, canvas):
    queue = myPriorityQueue()
    queue.push(start, getHeuristic(start, end))
    explored = [start]
    drawChild(canvas, 3, 1)
    greedyPath = {}
    while queue.isEmpty() == False:
        temp = queue.pop()
        currCell = temp.loc
        drawChild(canvas, currCell[0], currCell[1])
        if matrix[currCell[0]][currCell[1]] == 'e':

            # time.sleep(100)
            # drawChild(canvas, currCell[0], currCell[1])
            #(22, 48)
            #bfspath[currCell] = (end[0]-1,end[1])
            break

        if matrix[currCell[0]][currCell[1]] != '+':
            # check up
            if currCell[0] > 0:
                if matrix[currCell[0] - 1][currCell[1]] == ' ' or matrix[currCell[0] - 1][currCell[1]] == 'e':
                    childcell = (currCell[0] - 1, currCell[1])
                    if childcell not in explored:
                        queue.push(childcell, getHeuristic(childcell, end))
                        explored.append(childcell)
                        greedyPath[childcell] = currCell
                        # drawChild(canvas, currCell[0] - 1, currCell[1])

            # check down
            if matrix[currCell[0] + 1][currCell[1]] == ' ' or matrix[currCell[0] + 1][currCell[1]] == 'e':
                childcell = (currCell[0] + 1, currCell[1])
                if childcell not in explored:
                    queue.push(childcell, getHeuristic(childcell, end))
                    explored.append(childcell)
                    greedyPath[childcell] = currCell
                    # drawChild(canvas, currCell[0] + 1, currCell[1])

            # check right
            if matrix[currCell[0]][currCell[1] + 1] == ' ' or matrix[currCell[0]][currCell[1] + 1] == 'e':
                childcell = (currCell[0], currCell[1] + 1)
                if childcell not in explored:
                    queue.push(childcell, getHeuristic(childcell, end))
                    explored.append(childcell)
                    greedyPath[childcell] = currCell
                    # drawChild(canvas, currCell[0], currCell[1] + 1)

            # check left
            if currCell[1] > 0:
                if matrix[currCell[0]][currCell[1] - 1] == ' ' or matrix[currCell[0]][currCell[1] - 1] == 'e':
                    childcell = (currCell[0], currCell[1] - 1)
                    if childcell not in explored:
                        queue.push(childcell, getHeuristic(childcell, end))
                        explored.append(childcell)
                        greedyPath[childcell] = currCell
                        # drawChild(canvas, currCell[0], currCell[1] - 1)
    canvas.create_text(start[0] * 30, (start[1] * 30) - 60, text="S", fill="black", font=('Helvetica 15 bold'))

    TracePathBack(greedyPath)


#functions to help implement buttons in GUI
def runGreedy():
    drawMaze(matrix,canvas)
    greedy(matrix,canvas)
def runUCS():
    drawMaze(matrix, canvas)
    ucs(matrix,canvas)
def runBFS():
    drawMaze(matrix, canvas)
    bfs(matrix,canvas)
def runDFS():
    drawMaze(matrix, canvas)
    dfs(matrix,canvas)
def quit():
    root.quit()
def clearMaze():
    drawMaze(matrix,canvas)

#main
root = tkinter.Tk()
canvas = tkinter.Canvas()
canvas.configure(height=5000, width=5000, bg="#fff")
matrix = get_maze()
drawMaze(matrix, canvas)
start=findStartPoint(matrix)
end=findEndPoint(matrix)

canvas.pack()
root.update()

#All Buttons

button = tkinter.Button(root,text="Run BFS",font="Helvetica 10 bold",fg="Black",command=runBFS,bd = '5',width=30)
button.place(x=100, y=830)

button = tkinter.Button(root,text="Run DFS",font="Helvetica 10 bold",fg="Black",command=runDFS,bd = '5',width=30)
button.place(x=400, y=830)

button = tkinter.Button(root,text="Clear Maze",font="Helvetica 10 bold",fg="Black",command=clearMaze,bd = '5',width=30)
button.place(x=400, y=880)

button = tkinter.Button(root,text="Run UCS",font="Helvetica 10 bold",fg="Black",command=runUCS,bd = '5',width=30)
button.place(x=700, y=830)

button = tkinter.Button(root,text="Quit",font="Helvetica 10 bold",fg="Black",command=quit,bd = '5',width=30)
button.place(x=700, y=880)

button = tkinter.Button(root,text="Run Greedy",font="Helvetica 10 bold",fg="Black",command=runGreedy,bd = '5',width=30)
button.place(x=1000, y=830)


canvas.pack()
root.update()

root.mainloop()

# while True:
#     print("Select an Algorithm: ")
#     print("1.BFS\n2.DFS\n3.UCS\n4.Greedy\n5.exit")
#     choice = int(input("your Choice: "))
#     if choice == 1:
#         drawMaze(matrix, canvas)
#         bfs(matrix, canvas)
#         # canvas.pack()
#         # root.update()
#
#     elif choice == 2:
#         drawMaze(matrix, canvas)
#         dfs(matrix, canvas)
#         # canvas.pack()
#         # root.update()
#
#     elif choice == 3:
#         drawMaze(matrix, canvas)
#         ucs(matrix, canvas)
#         # canvas.pack()
#         # root.update()
#
#     elif choice == 4:
#         drawMaze(matrix, canvas)
#         greedy(matrix, canvas)
#         # canvas.pack()
#         # root.update()
#
#     elif choice == 5:
#         root.quit()
#         break
#     else:
#         print("please enter a valid choice!!!")

# bfs(matrix, canvas)
# dfs(matrix, canvas)
# ucs(matrix, canvas)
# greedy(matrix,canvas)
# def drawbfs():
#     bfs(matrix,canvas)
# B = tkinter.Button(root, text ="Hello", command = drawbfs)
# B.pack()
