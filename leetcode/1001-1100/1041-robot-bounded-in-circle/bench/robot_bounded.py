# Benchmark lane for LeetCode 1041 -- Python mirror of robot_bounded.kara.


def is_robot_bounded(instructions):
    x = 0
    y = 0
    # north, east, south, west
    facing = 0
    for c in instructions:
        if c == "G":
            if facing == 0:
                y += 1
            elif facing == 1:
                x += 1
            elif facing == 2:
                y -= 1
            else:
                x -= 1
        elif c == "L":
            facing = (facing + 3) % 4
        else:
            facing = (facing + 1) % 4
    return (x == 0 and y == 0) or facing != 0


def main():
    count, size, rounds = 2000, 100, 500
    seed = 1041
    strings = []
    for k in range(count):
        chars = []
        for _ in range(size):
            seed = (seed * 1103515245 + 12345) % 2147483648
            r = (seed // 65536) % 10
            if k % 2 == 0:
                c = "GLR"[r % 3]
            elif r < 8:
                c = "G"
            elif r == 8:
                c = "L"
            else:
                c = "R"
            chars.append(c)
        strings.append("".join(chars))
    bounded = 0
    check = 0
    for _ in range(rounds):
        for instructions in strings:
            answer = is_robot_bounded(instructions)
            if answer:
                bounded += 1
            check = (check * 131 + (2 if answer else 1)) % 1000000007
    print(f"{count} strings of {size} instructions, {rounds} rounds: {bounded} bounded, checksum {check}")


main()
