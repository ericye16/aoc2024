ex1 = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""

score1 = 7036

ex2 = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""

score2 = 11048

from dataclasses import dataclass
from enum import Enum
from heapq import *

@dataclass(frozen=True, order=True)
class Vec2:
    x: int
    y: int

    def __add__(self, o):
        return Vec2(self.x + o.x, self.y + o.y)

class OrderedEnum(Enum):
    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented
    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented
    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

class Dir(OrderedEnum):
    Up = Vec2(-1, 0)
    Down = Vec2(1, 0)
    Right = Vec2(0, 1)
    Left = Vec2(0, -1)


@dataclass(frozen=True, order=True)
class State:
    pos: Vec2
    dir: Dir

Maze = list[str]

def parse_map(inpt: str) -> Maze:
    return inpt.splitlines()

def in_map(maze: Maze, v: Vec2) -> str:
    return maze[v.x][v.y]

neighbors = {
    Dir.Up: [Dir.Left, Dir.Right],
    Dir.Down: [Dir.Left, Dir.Right],
    Dir.Left: [Dir.Up, Dir.Down],
    Dir.Right: [Dir.Up, Dir.Down],
}

def solve_p1(map: Maze) -> int:
    # find S
    start = None
    for x in range(len(map)):
        for y in range(len(map[0])):
            if map[x][y] == "S":
                start = Vec2(x, y)
                break
        if start is not None:
            break
    assert start is not None
    start = State(pos=start, dir=Dir.Right)
    to_visit = []
    visited = set()
    heappush(to_visit, (0, start))
    final_score = float("inf")
    while to_visit:
        score, state = heappop(to_visit)
        if state in visited:
            continue
        visited.add(state)
        if in_map(map, state.pos) == "E":
            final_score = score
            break
        # go forward
        next_state = state.pos + state.dir.value
        if in_map(map, next_state) != "#":
            heappush(to_visit, (score + 1, State(next_state, state.dir)))
        for neighbor in neighbors[state.dir]:
            heappush(to_visit, (score + 1000, State(state.pos, neighbor)))
    return final_score

from copy import deepcopy
def solve_p2(map: Maze) -> int:
    # find S
    start = None
    for x in range(len(map)):
        for y in range(len(map[0])):
            if map[x][y] == "S":
                start = Vec2(x, y)
                break
        if start is not None:
            break
    assert start is not None
    start = State(pos=start, dir=Dir.Right)
    to_visit = []
    visited = {}
    heappush(to_visit, (0, start, frozenset()))
    final_score = None
    all_final_visited = set()
    while to_visit:
        score, state, this_visited = heappop(to_visit)
        # if state in this_visited:
        #     continue
        if state not in visited:
            visited[state] = score
        elif score > visited[state]:
            continue
        print(f"\r{score} {len(visited)}", end="")
        # visited.add(state)
        new_this_visited = this_visited.union([state.pos])
        if final_score is not None and score > final_score:
            # print(f"score is {score} final score is {final_score}")
            break
        if in_map(map, state.pos) == "E" and final_score is None:
            final_score = score
            all_final_visited.update(new_this_visited)
        elif in_map(map, state.pos) == "E" and score == final_score:
            all_final_visited.update(new_this_visited)
        # go forward
        next_state = state.pos + state.dir.value
        if in_map(map, next_state) != "#":
            heappush(to_visit, (score + 1, State(next_state, state.dir), new_this_visited))
        for neighbor in neighbors[state.dir]:
            heappush(to_visit, (score + 1000, State(state.pos, neighbor), new_this_visited))
    print()
    for x in range(len(map)):
        for y in range(len(map[0])):
            if Vec2(x, y) in all_final_visited:
                print("O", end="")
            else:
                print(in_map(map, Vec2(x, y)), end="")
        print()
    return final_score, len(all_final_visited)


print(solve_p2(parse_map(ex1)))
print(solve_p2(parse_map(ex2)))

r = open("d16.txt").read()
print(solve_p2(parse_map(r)))

