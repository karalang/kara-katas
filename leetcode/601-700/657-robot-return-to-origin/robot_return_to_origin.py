# LeetCode #657: Robot Return to Origin -- walk the moves.
# Mirrors the ★ arm (robot_return_to_origin.kara) and its test harness.


def judge_circle(moves):
    x = y = 0
    for m in moves:
        if m == "U":
            y += 1
        elif m == "D":
            y -= 1
        elif m == "L":
            x -= 1
        else:
            x += 1
    return x == 0 and y == 0


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(moves):
    print(f'"{moves}" -> {"true" if judge_circle(moves) else "false"}')


def random_moves(n, balanced):
    letters = ["U", "D", "L", "R"]
    steps = []
    if balanced:
        for _ in range(n // 2):
            pair = next_random() % 2
            steps.append(letters[pair * 2])
            steps.append(letters[pair * 2 + 1])
        i = len(steps) - 1
        while i > 0:
            j = next_random() % (i + 1)
            steps[i], steps[j] = steps[j], steps[i]
            i -= 1
    else:
        for _ in range(n):
            steps.append(letters[next_random() % 4])
    return "".join(steps)


def word(b):
    return "true" if b else "false"


def main():
    global seed
    for s in ["UD", "LL", "U", "UDLR", "RRDDLLUU", "LRLRU", "LDRRLRUULR"]:
        show(s)
    seed = 657
    back = 0
    total = 0
    for k in range(300):
        n = 1 + next_random() % 60
        moves = random_moves(n, k % 2 == 0)
        at = judge_circle(moves)
        if at:
            back += 1
        total = (total * 7 + len(moves) * 2 + (1 if at else 0)) % 1000000007
    print(f"300 random strings: {back} back at the origin, checksum {total}")
    moves = random_moves(20000, True)
    print(f"20000 balanced: {word(judge_circle(moves))}")
    changed = "".join(("L" if c == "U" else "U") if i == 12345 else c for i, c in enumerate(moves))
    print(f"20000 with one move changed: {word(judge_circle(changed))}")
    print(f"20000 at random: {word(judge_circle(random_moves(20000, False)))}")


main()
