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
            to_explore = [(x, y)]
            corners = set()
            while to_explore:
                xx, yy = to_explore.pop()
                if done[xx][yy]:
                    continue
                done[xx][yy] = True
                section.area += 1

                def check_next(curx, cury, x0, y0):
                    # nonlocal perimeter
                    if in_bounds(x0, y0, xd, yd) and inp[x0][y0] == garden_section:
                        to_explore.append((x0, y0))
                        return 1
                    else:
                        section.perimeter += 1
                        return 0

                valid_edges = 0
                nextx, nexty = xx + 1, yy
                valid_edges += check_next(xx, yy, nextx, nexty)
                nextx, nexty = xx, yy + 1
                valid_edges += check_next(xx, yy, nextx, nexty)
                nextx, nexty = xx - 1, yy
                valid_edges += check_next(xx, yy, nextx, nexty)
                nextx, nexty = xx, yy - 1
                valid_edges += check_next(xx, yy, nextx, nexty)


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
        s += section.sides * section.area
    return s

# print(multiply_sections2(get_sections(parse_input(ex1))))
# print(multiply_sections2(get_sections(parse_input(ex2))))
# print(multiply_sections2(get_sections(parse_input(ex3))))
# print(multiply_sections2(get_sections(parse_input(ex4))))
print(multiply_sections2(get_sections(parse_input(ex5))))

# inp = open("d12.txt").read()
# print(multiply_sections2(get_sections(parse_input(inp))))
