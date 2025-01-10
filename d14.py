ex1 = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""

from dataclasses import dataclass


@dataclass
class Config:
    width: int
    height: int


config1 = Config(101, 103)

exconfig = Config(11, 7)


@dataclass
class Vec2:
    x: int
    y: int

    def __add__(self, o):
        return Vec2(self.x + o.x, self.y + o.y)
    
    def __sub__(self, o):
        return Vec2(self.x - o.x, self.y - o.y)

    def __rmul__(self, o):
        return Vec2(o * self.x, o * self.y)

    def __hash__(self):
        return hash((self.x, self.y))


@dataclass
class Robot:
    p: Vec2
    v: Vec2

import re


def parse_inpt(line: str):
    m = re.match(r"p=(\d+),(\d+) v=([\d-]+),([\d-]+)", line)
    return Robot(
        Vec2(int(m.group(1)), int(m.group(2))), Vec2(int(m.group(3)), int(m.group(4)))
    )


# list([print(parse_inpt(x)) for x in ex1.splitlines()])

def print_grid(robots: list[Robot], config: Config, count: bool=True):
    for y in range(config.height):
        for x in range(config.width):
            num_robots = sum((1 if r.p == Vec2(x, y) else 0) for r in robots)
            if num_robots == 0:
                print(".", end="")
            else:
                if count:
                    print(num_robots, end="")
                else:
                    print("#", end="")
        print("")

def print_grid2(robots: list[Vec2], config: Config, count: bool=True):
    x_moment = 0
    y_moment = 0
    for y in range(config.height):
        for x in range(config.width):
            if Vec2(x, y) in robots:
                print("#", end="")
                x_moment += x * x
                y_moment += y * y
            else:
                print(".", end="")
                pass
        print("")
    return x_moment, y_moment

def get_closest(robots: list[Vec2], config: Config):
    s = 0
    for robot in robots:
        for robot2 in robots:
            diff = robot - robot2
            s += abs(diff.x) + abs(diff.y)
    return s


from functools import reduce
from operator import mul
from matplotlib import pyplot as plt
from tqdm import tqdm
def parse_all_lines(inpt: str, config: Config = config1):
    robots = [parse_inpt(x) for x in inpt.splitlines()]
    # print_grid(robots, config)
    # print()
    x_moments = []
    y_moments = []
    diffs = []
    for second in tqdm(range(10000)):
        points = set()
        for robot in robots:
            robot.p += robot.v
            # print(robot.p)
            robot.p.x = robot.p.x % (config.width)
            robot.p.y = robot.p.y % (config.height)
            points.add(robot.p)
        # if second >= 100:
        if True:
            print(second)
            # print_grid(robots, config, count=False)
            x_moment, y_moment = print_grid2(points, config)
            print(flush=True)
            x_moments.append(x_moment)
            y_moments.append(y_moment)
            diffs.append(get_closest(points, config))
    # print_grid(robots, config)
    sectors = [0, 0, 0, 0]
    for robot in robots:
        # print(robot.p)
        if robot.p.x < config.width // 2 and robot.p.y < config.height // 2:
            sectors[0] += 1
        elif robot.p.x > config.width // 2 and robot.p.y < config.height // 2:
            sectors[1] += 1
        elif robot.p.x < config.width // 2 and robot.p.y > config.height // 2:
            sectors[2] += 1
        elif robot.p.x > config.width // 2 and robot.p.y > config.height // 2:
            sectors[3] += 1
    print(sectors)
    print(reduce(mul, sectors, 1))
    # plt.plot(x_moments)
    # plt.plot(y_moments)
    plt.plot(diffs)
    plt.show()



# parse_all_lines(ex1, exconfig)
inp = open("d14.txt").read()
parse_all_lines(inp, config1)
