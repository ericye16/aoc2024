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


@dataclass
class Vec2:
    x: int
    y: int

    def __add__(self, o):
        return Vec2(self.x + o.x, self.y + o.y)


def parse_map(map: str) -> list[list[str]]:
    return [list(x) for x in map.splitlines()]


def parse_instrs(instrs: str) -> str:
    return "".join(instrs.splitlines())


def parse(inpt: str) -> tuple[list[list[str]], str]:
    ma, instrs = inpt.split("\n\n")
    return parse_map(ma), parse_instrs(instrs)

def print_map(map: list[list[str]]) -> None:
    for x in map:
        print("".join(x))

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

# print(calc_gps(run1(*parse(ex2))))
r = open("d15.txt").read()
print(calc_gps(run1(*parse(r))))


