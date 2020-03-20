from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

#create a blank dictionary called map
map = {}
# create explore method
def explore(player, moves):
# Make it into a bfs
    #initialize Queue
    queue = Queue()
    #add starting room to queue
    queue.enqueue([player.current_room.id])
    #initialize visited
    visited = set()
    #while the queue has places to go
    while queue.size() > 0:
        #as exploration continues, remove from queue
        route = queue.dequeue()
        #grab the last visited room
        last_visited = route[-1]
        #if the last room isn't in visited, add to visited
        if last_visited not in visited:
            visited.add(last_visited)
            # note the exits
            for exit in map[last_visited]:
                #if the exit in the map dict is ?, return route
                if map[last_visited][exit] == '?':
                    return route
                #otherwise, get rid of the explored route
                else:
                    #copy
                    been_there = list(route)
                    been_there.append(map[last_visited][exit])
                    queue.enqueue(been_there)    
    return []    

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
