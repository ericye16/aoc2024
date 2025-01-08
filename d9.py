inpt = """2333133121414131402"""

inpt = open("d9.txt").read().strip()

disk = []

file_id = 0
for ch in range(len(inpt)):
    file_size = int(inpt[ch])
    if ch % 2 == 0:
        for _ in range(file_size):
            disk.append(file_id)
        file_id += 1
    else:
        for _ in range(file_size):
            disk.append(".")

# print(disk)
# compact
first_space = 0
back_idx = len(disk) - 1
while back_idx >= first_space:
    if disk[back_idx] == ".":
        back_idx -= 1
        continue
    if disk[first_space] != ".":
        first_space += 1
        continue
    disk[first_space] = disk[back_idx]
    disk[back_idx] = "."
    first_space += 1
    back_idx -= 1

# print(disk)

# checksum
checksum = 0
for chidx, ch in enumerate(disk):
    if ch == ".":
        break
    checksum += chidx * ch
print(checksum)

file_id = 0
cur_idx = 0
file_map = {}
area_map = {}
for ch in range(len(inpt)):
    file_size = int(inpt[ch])
    if ch % 2 == 0:
        area_map[cur_idx] = (file_id, file_size)
        file_map[file_id] = cur_idx
        file_id += 1
    else:
        area_map[cur_idx] = (".", file_size)
    cur_idx += file_size

print(area_map)
print(file_map)

num_files = file_id

def print_arr(m):
    idx_ = 0
    while idx_ in m:
        file_id, le = m[idx_]
        for _ in range(le):
            print(file_id, end="")
        idx_ += le
    print()

# print(area_map)
# print_arr(area_map)
for file_id in reversed(range(num_files)):
    file_idx = file_map[file_id]
    file_size = area_map[file_idx][1]
    free_idx = 0
    while free_idx in area_map:
        free_id, free_size = area_map[free_idx]
        if free_id != ".":
            free_idx += free_size
            continue
        if free_idx > file_idx:
            free_idx += free_size
            continue
        if free_size >= file_size:
            if free_size > file_size:
                area_map[free_idx + file_size] = (".", free_size - file_size)
            area_map[free_idx] = (file_id, file_size)
            file_map[file_id] = free_idx
            area_map[file_idx] = (".", file_size)
            # print(f"File {file_id} from {file_idx} to {free_idx}")
            # print(area_map)
            # print_arr(area_map)
            break
        free_idx += free_size
    # this is redundant
    do_again = True
    while do_again:
        do_again = False
        free_idx = 0
        while free_idx in area_map:
            file_id, free_size = area_map[free_idx]
            if file_id != ".":
                free_idx += free_size
                continue
            if free_idx + free_size in area_map and area_map[free_idx + free_size][0] == ".":
                area_map[free_idx] = (".", free_size + area_map[free_idx + free_size][1])
                del area_map[free_idx + free_size]
                do_again = True
                break
            free_idx += free_size

# print(file_map)
# print(area_map)
checksum = 0
for file_id in range(num_files):
    cur_idx = file_map[file_id]
    # print(cur_idx)
    file_size = area_map[cur_idx][1]
    for idx in range(cur_idx, cur_idx + file_size):
        checksum += idx * file_id

print(checksum)