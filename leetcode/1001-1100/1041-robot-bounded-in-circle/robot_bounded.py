# LeetCode #1041: Robot Bounded In Circle -- Python mirror of
# robot_bounded.kara (one pass of the instructions), same harness.


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


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def instructions_of(code, n):
    out = []
    c = code
    for _ in range(n):
        out.append("GLR"[c % 3])
        c //= 3
    return "".join(out)


def b(v):
    return "true" if v else "false"


def main():
    examples = ["GGLLGG", "GG", "GL", "L", "R", "G", "GRGRGRG", "GRGRGRGR", "GLGLGGLGL", "LLGRR"]
    for instructions in examples:
        print(f"{instructions} -> {b(is_robot_bounded(instructions))}")
    for n in range(1, 9):
        count = 3**n
        bounded = 0
        check = 0
        for code in range(count):
            answer = is_robot_bounded(instructions_of(code, n))
            if answer:
                bounded += 1
            check = (check * 131 + (2 if answer else 1)) % 1000000007
        print(f"all {count} of length {n}: {bounded} bounded, checksum {check}")
    seed = [1041]
    bounded = 0
    check = 0
    for k in range(500):
        n = next_random(seed) % 100 + 1
        chars = []
        for _ in range(n):
            r = next_random(seed) % 10
            if k % 2 == 0:
                c = "GLR"[r % 3]
            elif r < 8:
                c = "G"
            elif r == 8:
                c = "L"
            else:
                c = "R"
            chars.append(c)
        answer = is_robot_bounded("".join(chars))
        if answer:
            bounded += 1
        check = (check * 131 + (2 if answer else 1)) % 1000000007
    print(f"500 random strings: {bounded} bounded, checksum {check}")
    print(f"G x 100: {b(is_robot_bounded('G' * 100))}")
    print(f"GL x 50: {b(is_robot_bounded('GL' * 50))}")


main()
