#f = path.cost + estimated cost of the cheapest path
#from curr state to goal state
#distance from each number in the init to the pos its
#supposed to be in the goal
#so 7 in init is at (1,0) and 7 in Goal is at (2,1)
distance = 0
for x in range(len(board)):
    for y in range(len(board)):
        gX, gY = get_goal_coord(board[i][j])
        total += (abs(x - gX) + abs(y - gY))

def get_goal_coord(num, goal):
    for i in range(len(goal)):
        for i in range(len(goal)):
            if goal[i][j] == num:
                return i,j
class State:
    def __init__(self, parent, board, path_cost, action, f):
        self.parent = parent
        self.board = board
        self.path_cost = path_cost
        self.action = action
        self.f = f
        
    def __lt__(self, other):
        return self.f < other.f