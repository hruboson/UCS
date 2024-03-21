from pprint import pprint
from copy import deepcopy

class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not isinstance(other, Node):
            return NotImplemented
        
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return int(str(self.x) + str(self.y))

class Node:
    def __init__(self, coord, rating, parent):
        self.coord = coord
        self.rating = rating
        self.parent = parent

    def __eq__(self, other):
        if not isinstance(other, Node):
            return NotImplemented
        
        return self.coord == other.coord and self.rating == other.rating and self.parent == other.parent

# MAX 10x10 MATRIX
# Z means unreachable node (wall)
matrix_str = """9 9 7 6 3 7 9 8 9 9
                8 9 9 9 9 3 9 6 7 8
                8 9 Z Z Z 3 9 6 7 8
                6 9 Z 6 5 3 8 5 7 8
                7 9 Z 2 4 3 8 7 5 8
                Z Z Z Z Z 3 Z Z Z Z
                9 9 Z 8 3 9 9 Z 8 9
                9 9 Z 9 3 4 2 Z 7 7
                9 9 Z 9 3 Z Z Z 8 7
                9 9 9 9 3 9 8 7 7 8"""
    
start = Coord(3, 4)
end = Coord(6, 7)

if __name__ == "__main__":    
    rows = matrix_str.split('\n')

    matrix = []
    r = 0
    for row in rows:
        values = row.split()
        matrix.append([])
        for v in values:
            if v != "Z": # Change this character if you want different wall character
                matrix[r].append(int(v))
            else:
                matrix[r].append(None)
        r += 1

    opened = {}
    closed = {}

    #pprint(matrix)

    opened[hash(start)] = (Node(start, 0, None))

    iteration = 1

    while iteration <= 21:
        min = list(opened.values())[len(opened.values())-1]
        for n in opened.values():
            if n.rating < min.rating:
                min = n
        
        if min.coord.x == end.x and min.coord.y == end.y:
            closed[min.coord] = min
            break

        # Expand min
        now = Coord(min.coord.x, min.coord.y)
        if now.y+1 >= 0 and now.x-1 >= 0 and now.y+1 <= 9 and now.x-1 <= 9:
            if matrix[now.y+1][now.x-1] != None:
                new = Node(Coord(now.x-1, now.y+1), matrix[now.y+1][now.x-1] + min.rating, deepcopy(min))  # left up
                if hash(new.coord) not in closed and hash(new.coord) not in opened:
                    opened[hash(new.coord)] = new
        if now.y+1 >= 0 and now.x >= 0 and now.y+1 <= 9 and now.x <= 9:
            if matrix[now.y+1][now.x] != None:
                new = Node(Coord(now.x, now.y+1), matrix[now.y+1][now.x] + min.rating, deepcopy(min))  # up
                if hash(new.coord) not in closed and hash(new.coord) not in opened:
                    opened[hash(new.coord)] = new
        if now.y+1 >= 0 and now.x+1 >= 0 and now.y+1 <= 9 and now.x+1 <= 9:
            if matrix[now.y+1][now.x+1] != None:
                new = Node(Coord(now.x+1, now.y+1), matrix[now.y+1][now.x+1] + min.rating, deepcopy(min))  # right up
                if hash(new.coord) not in closed and hash(new.coord) not in opened:
                    opened[hash(new.coord)] = new
        if now.y >= 0 and now.x-1 >= 0 and now.y <= 9 and now.x-1 <= 9:
            if matrix[now.y][now.x-1] != None:
                new = Node(Coord(now.x-1, now.y), matrix[now.y][now.x-1] + min.rating, deepcopy(min))  # left
                if hash(new.coord) not in closed and hash(new.coord) not in opened:
                    opened[hash(new.coord)] = new
        if now.y >= 0 and now.x+1 >= 0 and now.y <= 9 and now.x+1 <= 9:
            if matrix[now.y][now.x+1] != None:
                new = Node(Coord(now.x+1, now.y), matrix[now.y][now.x+1] + min.rating, deepcopy(min))  # right
                if hash(new.coord) not in closed and hash(new.coord) not in opened:
                    opened[hash(new.coord)] = new
        if now.y-1 >= 0 and now.x-1 >= 0 and now.y-1 <= 9 and now.x-1 <= 9:
            if matrix[now.y-1][now.x-1] != None: 
                new = Node(Coord(now.x-1, now.y-1), matrix[now.y-1][now.x-1] + min.rating, deepcopy(min))  # down left
                if hash(new.coord) not in closed and hash(new.coord) not in opened:
                    opened[hash(new.coord)] = new
        if now.y-1 >= 0 and now.x >= 0 and now.y-1 <= 9 and now.x <= 9:
            if matrix[now.y-1][now.x] != None:
                new = Node(Coord(now.x, now.y-1), matrix[now.y-1][now.x] + min.rating, deepcopy(min))  # down
                if hash(new.coord) not in closed and hash(new.coord) not in opened:
                    opened[hash(new.coord)] = new
        if now.y-1 >= 0 and now.x+1 >= 0 and now.y-1 <= 9 and now.x+1 <= 9:
            if matrix[now.y-1][now.x+1] != None:
                new = Node(Coord(now.x+1, now.y-1), matrix[now.y-1][now.x+1] + min.rating, deepcopy(min))  # right down
                if hash(new.coord) not in closed and hash(new.coord) not in opened:
                    opened[hash(new.coord)] = new


        unique_nodes = {}
    
        for node in opened.values():
            coord = hash(node.coord)
            if coord in unique_nodes:
                if node.rating < unique_nodes[coord].rating:
                    unique_nodes[coord].rating = node.rating
            else:
                unique_nodes[coord] = node

        #for node in unique_nodes.values():
        #    print(f"([{node.coord.x}, {node.coord.y}], {node.rating},")#[{node.parent.coord.x}, {node.parent.coord.y}])")

        # Update opened list with unique nodes
        opened = unique_nodes
        del opened[hash(min.coord)]
        closed[hash(min.coord)] = deepcopy(min)

        if min.parent != None:
            print(f"Iteration {iteration} | Node ([{min.coord.x}, {min.coord.y}], {min.rating},[{min.parent.coord.x}, {min.parent.coord.y}])")
        else:
            print(f"Iteration {iteration} | Node ([{min.coord.x}, {min.coord.y}], {min.rating},NULL)")
        print("OPEN:")
        for key, node in opened.items():
            if node.parent != None:
                print(f"\t{key}:([{node.coord.x}, {node.coord.y}], {node.rating},[{node.parent.coord.x}, {node.parent.coord.y}])")
            else:
                print(f"\t{key}:([{node.coord.x}, {node.coord.y}], {node.rating}, NULL)")
        print("CLOSED:")
        for key, node in closed.items():
            if node.parent != None:
                print(f"\t{key}:([{node.coord.x}, {node.coord.y}], {node.rating},[{node.parent.coord.x}, {node.parent.coord.y}])")
            else:
                print(f"\t{key}:([{node.coord.x}, {node.coord.y}], {node.rating}, NULL)")

        iteration += 1
    if min.parent != None:
        print(f"Iteration {iteration} | Node ([{min.coord.x}, {min.coord.y}], {min.rating},[{min.parent.coord.x}, {min.parent.coord.y}])")
    else:
        print(f"Iteration {iteration} | Node ([{min.coord.x}, {min.coord.y}], {min.rating},NULL)")
    print("OPEN:")
    for node in opened.values():
        if node.parent != None:
            print(f"\t([{node.coord.x}, {node.coord.y}], {node.rating},[{node.parent.coord.x}, {node.parent.coord.y}])")
        else:
            print(f"\t([{node.coord.x}, {node.coord.y}], {node.rating}, NULL)")
    print("CLOSED:")
    for node in closed.values():
        if node.parent != None:
            print(f"\t([{node.coord.x}, {node.coord.y}], {node.rating},[{node.parent.coord.x}, {node.parent.coord.y}])")
        else:
            print(f"\t([{node.coord.x}, {node.coord.y}], {node.rating}, NULL)")


    
