from dataclasses import dataclass

ex1 = """AAAA
BBCD
BBCC
EEEC"""

ex2 = """OOOOO
OXOXO
OOOOO
OXOXO
OOOOO"""

ex3 = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""


ex4 = """EEEEE
EXXXX
EEEEE
EXXXX
EEEEE"""

ex5 = """AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA"""


def parse_input(input_string):
    return [list(row) for row in input_string.split("\n")]


@dataclass
class Section:
    plant: str
    perimeter: int
    area: int
    sides: int = 0


DOWN = 0  # +x
LEFT = 1  # -y
UP = 2  # -x
RIGHT = 3  # +y
NUM_DIRS = 4


def rh(dir):
    return (dir + 1) % NUM_DIRS


def lh(dir):
    return (dir - 1) % NUM_DIRS


class Vec:
    def __init__(self, el):
        self.el = el

    def __hash__(self):
        return hash(self.el)

    def __eq__(self, value: "Vec"):
        return self.el == value.el

    def __repr__(self):
        return f"{self.el}"


class Vec2(Vec):
    def __init__(self, x, y):
        super().__init__((x, y))

    def go(self, dir):
        assert dir < NUM_DIRS
        if dir == DOWN:
            return Vec2(self.el[0] + 1, self.el[1])
        elif dir == LEFT:
            return Vec2(self.el[0], self.el[1] - 1)
        elif dir == UP:
            return Vec2(self.el[0] - 1, self.el[1])
        elif dir == RIGHT:
            return Vec2(self.el[0], self.el[1] + 1)


# DFS each
def get_sections(inp):
    def in_bounds(x, y, xd, yd):
        return 0 <= x < xd and 0 <= y < yd

    sections = []
    xd = len(inp)
    yd = len(inp[0])
    done = [[False for y in range(yd)] for x in range(xd)]
    for x in range(xd):
        for y in range(yd):
            if done[x][y]:
                continue
            garden_section = inp[x][y]
            section = Section(garden_section, 0, 0, 0)
            to_explore = [Vec2(x, y)]
            edges = set()
            while to_explore:
                v = to_explore.pop()
                xx, yy = v.el
                if done[xx][yy]:
                    continue
                done[xx][yy] = True
                section.area += 1

                def check_next(dir: int, v_new: Vec2, v_old: Vec2):
                    x0, y0 = v_new.el
                    if in_bounds(x0, y0, xd, yd) and inp[x0][y0] == garden_section:
                        to_explore.append(v_new)
                    else:
                        section.perimeter += 1
                        # v_edge = Vec2(max(v_new.el[0], v_old.el[0]), max(v_new.el[1], v_old.el[1])) 
                        v_edge = v_old
                        assert (dir, v_edge) not in edges
                        edges.add((dir, v_edge))

                for dir in range(NUM_DIRS):
                    v_new = v.go(dir)
                    check_next(dir, v_new, v)
            edge1 = None
            sides = 0
            # print(f"Edges {garden_section} {len(edges)}")
            while edges or edge1 is not None:
                if edge1 is None:
                    edge1 = edges.pop()
                    # print("pop1")
                    dir, v = edge1
                    # Check behind
                    l_dir = lh(dir)
                    v_behind = v.go(l_dir)
                    if (dir, v_behind) in edges:
                        # print(f"at {dir} {v} looking for {v_behind} behind")
                        sides -= 1
                dir, v = edge1
                r_dir = rh(dir)
                v_next = v.go(r_dir)
                # print(f"at {dir} {v} looking for {v_next}")
                if (dir, v_next) in edges:
                    edge1 = (dir, v_next)
                    # print("remove")
                    edges.remove((dir, v_next))
                else:
                    # print("Adding side")
                    sides += 1
                    edge1 = None
            section.sides = sides
            sections.append(section)
    return sections


def multiply_sections(sections: list[Section]):
    s = 0
    for section in sections:
        s += section.perimeter * section.area
    return s


# print(multiply_sections(get_sections(parse_input(ex1))))
# print(multiply_sections(get_sections(parse_input(ex2))))
# print(multiply_sections(get_sections(parse_input(ex3))))

# inp = open("d12.txt").read()
# print(multiply_sections(get_sections(parse_input(inp))))


def multiply_sections2(sections: list[Section]):
    s = 0
    for section in sections:
        print(f"Section {section.plant} sides {section.sides} area {section.area}")
        s += section.sides * section.area
    return s


print(multiply_sections2(get_sections(parse_input(ex1))))
print(multiply_sections2(get_sections(parse_input(ex2))))
print(multiply_sections2(get_sections(parse_input(ex3))))
print(multiply_sections2(get_sections(parse_input(ex4))))
print(multiply_sections2(get_sections(parse_input(ex5))))

inp = open("d12.txt").read()
print(multiply_sections2(get_sections(parse_input(inp))))
# print(multiply_sections(get_sections(parse_input(inp))))
