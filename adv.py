from room import Room
from player import Player
from world import World

import random
from ast import literal_eval
from typing import List

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

traversal_path = []

# copy paste from utils from graphs 
class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value) -> None:
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self) -> int:
        return len(self.stack)
    def peek(self):
        return self.stack[-1]

# dictionary to hold inverse directions for backing up part
reverse_directions = {'n':'s', 's':'n', 'w':'e', 'e':'w'}

def traverse_graph() -> List[str]:
    traversal_path = []
    # hold rooms and the path to the rooms
    s = Stack()

    # store k,v pairs of rooms and path to rooms
    visited_graph = {}
    s.push(value=(player.current_room, None))
    while s.size() > 0:
        curr = s.peek()
        room, direction_traveled = curr[0], curr[1]
        if room.id not in visited_graph:
            visited_graph[room.id] = set() # initial set of directions we've gone, use set to avoid duplicates
        if direction_traveled:
            visited_graph[room.id].add(direction_traveled)
        # break if we visit all the rooms
        if len(visited_graph) == len(room_graph):
            break
        # Use depth first search to get unexplored branches
        unexplored_branches = [direction for direction in room.get_exits() if direction not in visited_graph[room.id]]
        if unexplored_branches:
            random_direction = random.choice(unexplored_branches)
            print("Found at least one possible direction, choosing at random if more than one is found:",random_direction)
            visited_graph[room.id].add(random_direction)
            # push the room and path to room
            s.push(value=(room.get_room_in_direction(random_direction), reverse_directions[random_direction]))
            traversal_path.append(random_direction)
        # when at dead end, begin backing up to spot with untraveled directions
        else:
            print("Reached dead-end, backing up to directions not yet traveled by traveling:", direction_traveled)
            traversal_path.append(direction_traveled)
            s.pop()
    return traversal_path

traversal_path = traverse_graph()


# TRAVERSAL TEST - DO NOT MODIFY
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
"""player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")"""
