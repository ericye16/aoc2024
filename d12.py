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
            edges = set()
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
                    else:
                        section.perimeter += 1
                        if curx == x0:
                            dir = "V"
                        else:
                            dir = "H"
                        edges.add((dir, max(curx, x0), max(cury, y0)))

                nextx, nexty = xx + 1, yy
                check_next(xx, yy, nextx, nexty)
                nextx, nexty = xx, yy + 1
                check_next(xx, yy, nextx, nexty)
                nextx, nexty = xx - 1, yy
                check_next(xx, yy, nextx, nexty)
                nextx, nexty = xx, yy - 1
                check_next(xx, yy, nextx, nexty)

            if True:
                print(f"Section {garden_section}")
                for x0 in range(xd + 1):
                    for y0 in range(yd + 1):
                        if ("H", x0, y0) in edges and ("V", x0, y0) in edges:
                            print("┌", end="")
                        elif ("H", x0, y0) in edges:
                            print("─", end="")
                        elif ("V", x0, y0) in edges:
                            print("│", end="")
                        else:
                            print(".", end="")
                    print("")
                

            def find_edge(nedge, edges):
                if nedge in edges:
                    edges.remove(nedge)
                    return True
                else:
                    return False

            edge1 = None
            sides = 0

            while edges:
                if edge1 is None:
                    edge1 = edges.pop()
                    if edge1[0] == "H":
                        if ("H", edge1[1], edge1[2] + 1) in edges and (
                            "H",
                            edge1[1],
                            edge1[2] - 1,
                        ) in edges:
                            sides += 0
                        else:
                            sides += 1
                    else:
                        assert edge1[0] == "V"
                        if ("V", edge1[1] + 1, edge1[2]) in edges and (
                            "V",
                            edge1[1] - 1,
                            edge1[2],
                        ) in edges:
                            sides += 0
                        else:
                            sides += 1
                if edge1[0] == "H":
                    nedge = ("H", edge1[1], edge1[2] + 1)
                    if find_edge(nedge, edges):
                        edge1 = nedge
                        continue
                    nedge = ("H", edge1[1], edge1[2] - 1)
                    if find_edge(nedge, edges):
                        edge1 = nedge
                        continue
                    # not
                    sides += 1
                    nedge = ("V", edge1[1] - 1, edge1[2])
                    if find_edge(nedge, edges):
                        edge1 = nedge
                        continue
                    nedge = ("V", edge1[1], edge1[2])
                    if find_edge(nedge, edges):
                        edge1 = nedge
                        continue
                    nedge = ("V", edge1[1] - 1, edge1[2] + 1)
                    if find_edge(nedge, edges):
                        edge1 = nedge
                        continue
                    nedge = ("V", edge1[1], edge1[2] + 1)
                    if find_edge(nedge, edges):
                        edge1 = nedge
                        continue
                    sides -= 1
                    edge1 = None
                    # print(edge1)
                    # print(edges)
                    # raise ValueError("uhhh")
                else:
                    assert edge1[0] == "V"
                    nedge = ("V", edge1[1] + 1, edge1[2])
                    if nedge in edges:
                        edges.remove(nedge)
                        edge1 = nedge
                        continue
                    nedge = ("V", edge1[1] - 1, edge1[2])
                    if nedge in edges:
                        edges.remove(nedge)
                        edge1 = nedge
                        continue
                    sides += 1
                    nedge = ("H", edge1[1], edge1[2] - 1)
                    if find_edge(nedge, edges):
                        edge1 = nedge
                        continue
                    nedge = ("H", edge1[1], edge1[2])
                    if find_edge(nedge, edges):
                        edge1 = nedge
                        continue
                    nedge = ("H", edge1[1] + 1, edge1[2] - 1)
                    if find_edge(nedge, edges):
                        edge1 = nedge
                        continue
                    nedge = ("H", edge1[1] + 1, edge1[2])
                    if find_edge(nedge, edges):
                        edge1 = nedge
                        continue
                    sides -= 1
                    edge1 = None
                    # print(edge1)
                    # print(edges)
                    # raise ValueError("fdsfds")
            section.sides = sides
            print(f"Sides: {sides}")
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
