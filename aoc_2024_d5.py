# inp = input()
import functools
from collections import defaultdict

inp = """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

inp = open("d5.txt").read()

rules_s, updates_s = inp.split("\n\n")

rules = []
for rule_s in rules_s.splitlines():
    if not rule_s: continue
    before, after = [int(x) for x in rule_s.split("|")]
    rules.append((before, after))

# print(rules)

updates = []
for update_s in updates_s.splitlines():
    if not update_s: continue
    # print(update_s)
    update_pages = [int(x) for x in update_s.split(",")]
    updates.append(update_pages)

def passes(updates: list[int], rules: tuple[int, int]):
    for rule in rules:
        if rule[0] not in updates or rule[1] not in updates:
            continue
        before_idx = updates.index(rule[0])
        after_idx = updates.index(rule[1])
        if before_idx > after_idx: return False
    return True

passing_updates = [
    x for x in updates if passes(x, rules)
]

# print(passing_updates)

def middle(x):
    return x[len(x) // 2]

print(sum(middle(x) for x in passing_updates))

failing_updates = [
    x for x in updates if not passes(x, rules)
]

def updates_comparison(rules, a, b):
    if a not in rules:
        return 1
    if b in rules[a]:
        return -1
    else:
        return 1
    

def sort_updates(updates: list[int], rules: dict[int, int]):
    updates_sorted = sorted(updates, key=functools.cmp_to_key(lambda a, b: updates_comparison(rules, a, b)))
    return updates_sorted

rules_h = defaultdict(list)
for before, after in rules:
    rules_h[before].append(after)

sorted_failing_updates = [
    sort_updates(x, rules_h) for x in failing_updates
]

print(sorted_failing_updates)

print(sum(middle(x) for x in sorted_failing_updates))