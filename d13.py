ex1 = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""

import re
from dataclasses import dataclass


@dataclass
class Button:
    cost: int
    x: int
    y: int


@dataclass
class Machine:
    a: Button
    b: Button
    prize: tuple[int, int]


def parse_inputs(inp):
    machines_split = inp.split("\n\n")

    machines: list[Machine] = []
    for machine_s in machines_split:
        line_split = machine_s.split("\n")
        m = re.match(r"Button A: X\+(\d+), Y\+(\d+)", line_split[0])
        a = Button(3, int(m.group(1)), int(m.group(2)))
        m = re.match(r"Button B: X\+(\d+), Y\+(\d+)", line_split[1])
        b = Button(1, int(m.group(1)), int(m.group(2)))
        m = re.match(r"Prize: X=(\d+), Y=(\d+)", line_split[2])
        machine = Machine(a, b, (int(m.group(1)), int(m.group(2))))
        machines.append(machine)
    # print(machines)
    return machines


def divb(a: Button, p: tuple[int, int]):
    divx = p[0] / a.x
    remx = p[0] % a.x
    if remx != 0:
        return False
    divy = p[1] / a.y
    remy = p[1] % a.y
    if remy != 0:
        return False
    if divx != divy:
        return False
    return divx


def psub(p: tuple[int, int], a: Button, n: int):
    return (p[0] - a.x * n, p[1] - a.y * n)


def p1(machine: Machine, limit: int = 100):
    for a_presses in range(limit):
        p = psub(machine.prize, machine.a, a_presses)
        if b_presses := divb(machine.b, p):
            return a_presses * 3 + b_presses * 1
    return False


def pp1(inpt: str):
    inpts = parse_inputs(inpt)
    # print(inpts)
    s = 0
    for machine in inpts:
        c = solve_p1(machine)
        s += c
        # print(c)
    print(int(s))

def solve_p1(machine: Machine):
    # Check for linear independence
    if machine.a.x / machine.b.x == machine.a.y / machine.b.y:
        if machine.prize[0] / machine.b.x == machine.prize[1] / machine.b.y and \
            machine.prize[0] % machine.b.x == 0:
            return int(machine.prize[0] / machine.b.x)
        else:
            return False
    # solve
    a_prod = machine.a.x * machine.a.y
    b_prod = machine.b.x * machine.a.y
    c_prod = machine.prize[0] * machine.a.y

    a_prod2 = machine.a.y * machine.a.x
    b_prod2 = machine.b.y * machine.a.x
    c_prod2 = machine.prize[1] * machine.a.x
    b_cnt = (c_prod2 - c_prod) / (b_prod2 - b_prod)
    if (c_prod2 - c_prod) % (b_prod2 - b_prod) != 0:
        return False
    p_rem = psub(machine.prize, machine.b, b_cnt)
    if a_cnt := divb(machine.a, p_rem):
        return a_cnt * 3 + b_cnt * 1
    else:
        return False


def pp2(inpt: str):
    inpts = parse_inputs(inpt)
    # print(inpts)
    s = 0
    for machine in inpts:
        machine.prize = (
            machine.prize[0] + 10000000000000,
            machine.prize[1] + 10000000000000,
        )
        c = solve_p1(machine)
        s += c
        # print(c)
    print(int(s))

pp1(ex1)
pp1(open("d13.txt").read())
pp2(ex1)
pp2(open("d13.txt").read())
