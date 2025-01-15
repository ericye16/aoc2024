ex1 = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""

ex2 = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""

from dataclasses import dataclass
from copy import deepcopy


@dataclass(frozen=True)
class Vec2:
    x: int
    y: int

    def __add__(self, o):
        return Vec2(self.x + o.x, self.y + o.y)
    
    def __sub__(self, o):
        return Vec2(self.x - o.x, self.y - o.y)

def parse_map(map: str) -> list[list[str]]:
    return [list(x) for x in map.splitlines()]


def parse_instrs(instrs: str) -> str:
    return "".join(instrs.splitlines())


def parse(inpt: str) -> tuple[list[list[str]], str]:
    ma, instrs = inpt.split("\n\n")
    return parse_map(ma), parse_instrs(instrs)

def print_map(map: list[list[str]], moved: list[Vec2] = None, dir = None, has_moved = False) -> None:
    if moved is None:
        moved = []
    if dir is None:
        dir = Vec2(0, 0)
    for xi, x in enumerate(map):
        for yi, y in enumerate(x):
            if has_moved and Vec2(xi, yi) - dir in moved:
                y = f"\033[5m{y}\033[0m"
            print(y, end="")
        print()

do_prints = False
def run1(map: list[list[str]], insts: str) -> list[list[str]]:
    robot_loc = None
    for x in range(len(map)):
        for y in range(len(map[0])):
            if map[x][y] == "@":
                robot_loc = Vec2(x, y)
                break
        if robot_loc is not None:
            break
    else:
        raise ValueError("Couldn't find robot")
    dirs = {"<": Vec2(0, -1), "v": Vec2(1, 0), ">": Vec2(0, 1), "^": Vec2(-1, 0)}
    for instr in insts:
        dir = dirs[instr]
        cursor = robot_loc
        to_move = []
        at_cursor = map[cursor.x][cursor.y]
        can_move = False
        while at_cursor != "#" and at_cursor != ".":
            to_move.append(deepcopy(cursor))
            cursor += dir
            at_cursor = map[cursor.x][cursor.y]
        if at_cursor == ".":
            can_move = True
        if can_move:
            for to_movee in reversed(to_move):
                dest = to_movee + dir
                map[dest.x][dest.y] = map[to_movee.x][to_movee.y]
            map[robot_loc.x][robot_loc.y] = "."
            robot_loc += dir
        if do_prints:
            print(instr)
            print_map(map)
    return map

def calc_gps(map: list[list[str]]) -> int:
    s = 0
    for x in range(len(map)):
        for y in range(len(map[0])):
            if map[x][y] == "O":
                s += x * 100 + y
    return s

# p2

def expand_map(map: list[list[str]]) -> list[list[str]]:
    mapo = []
    for x in range(len(map)):
        mapo.append([])
        for y in range(len(map[0])):
            imap = map[x][y]
            if imap == "@":
                mapo[x].extend(["@", "."])
            elif imap == "#":
                mapo[x].extend(["#", "#"])
            elif imap == "O":
                mapo[x].extend(["[", "]"])
            elif imap == ".":
                mapo[x].extend([".", "."])
    return mapo

ex3 = """#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^"""

from collections import deque
do_prints = True
def run2(map: list[list[str]], insts: str) -> list[list[str]]:
    robot_loc = None
    for x in range(len(map)):
        for y in range(len(map[0])):
            if map[x][y] == "@":
                robot_loc = Vec2(x, y)
                break
        if robot_loc is not None:
            break
    else:
        raise ValueError("Couldn't find robot")
    if do_prints:
        print_map(map)
    dirs = {"<": Vec2(0, -1), "v": Vec2(1, 0), ">": Vec2(0, 1), "^": Vec2(-1, 0)}
    for instr in insts:
        dirupdown = instr == "^" or instr == "v"
        dir = dirs[instr]
        cursor = robot_loc
        to_move = []
        to_visit = deque()
        to_visit.append(cursor)
        visited = set()
        at_cursor = map[cursor.x][cursor.y]
        can_move = True
        while to_visit:
            cursor = to_visit.popleft()
            if cursor in visited:
                continue
            visited.add(cursor)
            at_cursor = map[cursor.x][cursor.y]
            if at_cursor == "." or at_cursor == "#":
                continue
            to_move.append(deepcopy(cursor))
            if at_cursor == "[" and dirupdown:
                to_visit.appendleft(cursor + dirs[">"])
            elif at_cursor == "]" and dirupdown:
                to_visit.appendleft(cursor + dirs["<"])
            cursor += dir
            at_cursor = map[cursor.x][cursor.y]
            if at_cursor == "#":
                can_move = False
            to_visit.append(deepcopy(cursor))
        if can_move:
            for to_movee in reversed(to_move):
                dest = to_movee + dir
                map[dest.x][dest.y] = map[to_movee.x][to_movee.y]
                map[to_movee.x][to_movee.y] = "."
                # map[robot_loc.x][robot_loc.y] = "."
            robot_loc += dir
        if do_prints:
            print(instr)
            print_map(map, to_move, dir, can_move)
    return map

def calc2_gps(map: list[list[str]]) -> int:
    s = 0
    for x in range(len(map)):
        for y in range(len(map[0])):
            if map[x][y] == "[":
                s += x * 100 + y
    return s
# print(calc_gps(run1(*parse(ex2))))
r = open("d15.txt").read()
# print(calc_gps(run1(*parse(r))))
ma, insts = parse(ex2)
ma2 = expand_map(ma)
out2 = run2(ma2, insts)
print(calc2_gps(out2))
# print_map(ma2)


