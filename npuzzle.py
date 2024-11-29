import copy
import queue
from cProfile import Profile
from pstats import SortKey, Stats
#import re

N=8
ROW=3
COL=3

class State:
    def __init__(self, parent, board, path_cost, action, f):
        self.parent = parent
        self.board = board
        self.path_cost = path_cost
        self.action = action
        self.f = f
        
    '''def __lt__(self, other):
        return self.path_cost < other.path_cost'''
    
    '''def __lt__(self, other):
        return self.f < other.f'''
    
    def return_coords(self):
        for i in range(ROW):
            for j in range(COL):
                if (self.board[i][j] == 0):
                    return i,j
    
    def can_move_up(self):
        for i in range(ROW):
            for j in range(COL):
                if (self.board[i][j] == 0) and (i==2 or i==1):
                    return True
        return False
    
    def can_move_down(self):
        for i in range(ROW):
            for j in range(COL):
                if (self.board[i][j] == 0) and (i==0 or i==1):
                    return True
        return False
    
    def can_move_left(self):
        for i in range(ROW):
            for j in range(COL):
                if (self.board[i][j] == 0) and (j==2 or j==1):
                    return True
        return False
    
    def can_move_right(self):
        for i in range(ROW):
            for j in range(COL):
                if (self.board[i][j] == 0) and (j==0 or j==1):
                    return True
        return False
    
    def move_up(self):
        for i in range(ROW):
            for j in range(COL):
                if self.board[i][j]==0 and i!=0:
                    self.board[i][j]=self.board[i-1][j]
                    self.board[i-1][j]=0
        print('moved up')
        return
    
    def move_down(self):
        for i in range(ROW):
            for j in range(COL):
                if self.board[i][j]==0 and i!=2:
                    self.board[i][j]=self.board[i+1][j]
                    self.board[i+1][j]=0
        print('moved down')
        return
    
    def move_left(self):
        for i in range(ROW):
            for j in range(COL):
                if self.board[i][j]==0 and j!=0:
                    self.board[i][j]=self.board[i][j-1]
                    self.board[i][j-1]=0
        print('moved left')
        return
    
    def move_right(self):
        for i in range(ROW):
            for j in range(COL):
                if self.board[i][j]==0 and j!=2:
                    self.board[i][j]=self.board[i][j+1]
                    self.board[i][j+1]=0
        print('moved right')
        return
        
    def possible_actions(self):
        actions=[]
        if self.can_move_right():
            actions.append('right')
        if self.can_move_left():
            actions.append('left')
        if self.can_move_up():
            actions.append('up')
        if self.can_move_down():
            actions.append('down')
        print("possible actions: ", actions)
        return(actions)
    
    def print_board(self):
        print("Current Board: ")
        for row in self.board:
            print(row)
            print(row, end='\n')

def result(act, state):
    new_state = copy.deepcopy(state)
    new_state.parent = state
    new_state.path_cost = state.path_cost+1
    
    if act == 'up':
        new_state.move_up()
        new_state.action = 'up'
        return new_state
    if act == 'down':
        new_state.move_down()
        new_state.action = 'down'
        return new_state
    if act == 'left':
        new_state.move_left()
        new_state.action = 'left'
        return new_state
    if act == 'right':
        new_state.move_right()
        new_state.action = 'right'
        return new_state
    
def expand(state):
    states = []
    actions = state.possible_actions()
    for action in actions:
        print("action:",action)
        states.append(result(action, state))
    print('states after expansion: ')
    for state in states:
        print(state.board)
    return states

def is_cycle(state):
    prev = state.parent
    level = state.path_cost - 1
    while(level > 0):
        if prev.board == state.board:
            return True
        prev = prev.parent
        level -= 1
 
def breadth_first_search(init, goal):
    node = State(None, init, 0, 0, 0)
    if init == goal:
        print("already at goal state")
        return node.board
    frontier = queue.Queue(maxsize=0)
    frontier.put(node)
    reached = [init]
    while(not(frontier.empty())):
        node = frontier.get()
        for child in expand(node):
            s = child.board
            if s == goal:
                print("goal reached")
                print(s)
                #return child
                return endgame(child)
            if s not in reached:
                reached.append(s)
                print('reached: ',reached)
                frontier.put(child)
    print("fail")
    return

def iterative_deepening_search(init, goal):
    for depth in range(100):
        result = depth_limited_search(init, goal, depth)
        if (not(result == 'cutoff')):
            return result

def depth_limited_search(init, goal, l):
    frontier = queue.LifoQueue(maxsize=0)
    node = State(None, init, 0, 0, 0)
    frontier.put(node)
    result = 'fail'
    while(not(frontier.empty())):
        node = frontier.get()
        if node.board == goal:
            print('goal reached', node.board)
            return 'Done!', endgame(node)
        if node.path_cost > l:
            result = 'cutoff'
        elif (not(is_cycle(node))):
            for child in expand(node):
                frontier.put(child)
    return result

def calc_f(node,h,goal):
    f = 0
    if h == 'nmt':
        f = node.path_cost + number_of_misplaced_tiles(node.board,goal)
    if h == 'md':
        f = node.path_cost + manhattan_distance(node.board, goal)
    return f

def a_star(init, goal, h):
    node = State(None, init, 0, None, 0)
    node.f = calc_f(node,h,goal)
    pq = [node]
    reached = {str(node.board): node}
    while (len(pq)!= 0):
        pq.sort(key=lambda x: x.f, reverse=True)
        node = pq.pop()
        if node.board == goal:
            print('goal reached')
            return endgame(node)
        for child in expand(node):
            s = child.board
            child.f = calc_f(child, h, goal)
            if (str(s) not in reached) or (child.f < reached[str(s)].f):
                reached[str(s)] = child
                pq.append(child)
    return 'fail'       
        
def best_first_search(init, goal):
    node = State(None, init, 0, None, 0)
    pq = [node]
    reached = {str(node.board): node}
    while (len(pq)!= 0):
        pq.sort(key=lambda x: x.path_cost, reverse=True)
        for i in pq:
            print(i.board)
        node = pq.pop()
        if node.board == goal:
            print('goal reached')
            return endgame(node)
        for child in expand(node):
            s = child.board
            #child.f = calc_f(child, h, goal)
            if (str(s) not in reached) or (child.path_cost < reached[str(s)].path_cost):
                reached[str(s)] = child
                pq.append(child)
    return 'fail'

def breadth_first_search_optimal_moves(init,goal):
    moves = []
    state = breadth_first_search(init,goal)
    level = state.path_cost
    moves.append(state.action)
    while(state.path_cost > 1):
        state = state.parent
        moves.append(state.action)
    #return moves[::-1]
    print("Breadth First Search Optimal Moves: ", moves)
    print("Sequence of Actions: ", action_sequence)
    return

def number_of_misplaced_tiles(init, goal):
    misplaced_tiles = 0
    for tile in range(len(init)):
        if (init[tile] != 0) and (init[tile] != goal[tile]):
            misplaced_tiles += 1
    return misplaced_tiles

def get_goal_coord(num, goal):
    for i in range(3):
        for j in range(3):
            if goal[i][j] == num:
                return i,j
                
def manhattan_distance(board,goal):
    distance = 0
    for x in range(3):
        for y in range(3):
            gX, gY = get_goal_coord(board[x][y], goal)
            distance += (abs(x - gX) + abs(y - gY))
    return distance


Puzzle0 = [[3,1,2],
           [7,0,5],
           [4,6,8]]

Puzzle1 = [[7,2,4],
           [5,0,6],
           [8,3,1]]

Puzzle2 = [[6,7,3],
           [1,5,2],
           [4,0,8]]

Puzzle3 = [[0,7,3],
           [4,1,3],
           [7,2,5]]

Puzzle4 = [[7,3,4],
           [2,5,1],
           [6,8,0]]

Puzzle5 = [[1,3,8],
           [4,7,5],
           [6,0,2]]

Puzzle6 = [[8,7,6],
           [5,4,3],
           [2,1,0]]

Goal_Board = [[0,1,2],
              [3,4,5],
              [6,7,8]]

def pb(ss):
    for s in ss:
        for row in s:
            print(row, end='\n')
        print(end='\n')
            
def endgame(s):
    action_sequence = []
    state_sequence = []
    print("Path Cost: ", s.path_cost)
    while(s.path_cost>0):
        action_sequence.append([s.action, s.parent.return_coords()[0], s.parent.return_coords()[1]])
        state_sequence.append(s.board)
        s = s.parent
    print("Actions: ", action_sequence[::-1])
    print("States: ", pb(state_sequence[::-1]))
    return

h1 = 'nmt'
h2 = 'md'
'''
with Profile() as profile:
    print(f"{breadth_first_search(Puzzle0, Goal_Board) = }")
    (
        Stats(profile)
        .strip_dirs()
        .sort_stats(SortKey.CALLS)
        .print_stats()
    )'''
'''
with Profile() as profile:
    print(f"{iterative_deepening_search(Puzzle0, Goal_Board) = }")
    (
        Stats(profile)
        .strip_dirs()
        .sort_stats(SortKey.CALLS)
        .print_stats()
    )'''
'''
with Profile() as profile:
    print(f"{a_star(Puzzle1, Goal_Board, h2) = }")
    (
        Stats(profile)
        .strip_dirs()
        .sort_stats(SortKey.CALLS)
        .print_stats()
    )'''

#print('Breadth First Search: ', breadth_first_search(Puzzle0, Goal_Board))
#print('Breadth First Search: ', breadth_first_search(Puzzle1, Goal_Board))

#print('Iterative Deepening Search: ', iterative_deepening_search(Puzzle0, Goal_Board))
#print('Iterative Deepening Search: ', iterative_deepening_search(Puzzle1, Goal_Board))

#print('Best First Search: ', best_first_search(Puzzle0, Goal_Board))
#print('Best First Search: ', best_first_search(Puzzle1, Goal_Board))

#print('A* Search: ', a_star(Puzzle0, Goal_Board, h1))
#print('A* Search: ', a_star(Puzzle0, Goal_Board, h2))

#print('A* Search: ', a_star(Puzzle1, Goal_Board, h1))
print('A* Search: ', a_star(Puzzle1, Goal_Board, h2))

#print('A* Search: ', a_star(Puzzle2, Goal_Board, h1))
#print('A* Search: ', a_star(Puzzle2, Goal_Board, h2))

#print('A* Search: ', a_star(Puzzle3, Goal_Board, h1))
#print('A* Search: ', a_star(Puzzle3, Goal_Board, h2))

#print('A* Search: ', a_star(Puzzle4, Goal_Board, h1))
#print('A* Search: ', a_star(Puzzle4, Goal_Board, h2))

#print('A* Search: ', a_star(Puzzle5, Goal_Board, h1))
#print('A* Search: ', a_star(Puzzle5, Goal_Board, h2))

#print('A* Search: ', a_star(Puzzle6, Goal_Board, h1))
#print('A* Search: ', a_star(Puzzle6, Goal_Board, h2))

#print(number_of_misplaced_tiles(Puzzle0, Goal_Board))
#print(manhattan_distance(Puzzle0, Goal_Board))