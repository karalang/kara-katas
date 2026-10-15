# Benchmark for #657: walk the moves, as the Kara ★ arm.


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


seed = 657


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


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


def main():
    inputs, rounds = 8, 100
    strings = [random_moves(1000000, k % 2 == 0) for k in range(inputs)]
    back = 0
    checksum = 0
    for r in range(rounds):
        pick = (r * 3) % inputs
        at = judge_circle(strings[pick])
        if at:
            back += 1
        checksum = (checksum * 31 + pick * 2 + (1 if at else 0)) % 1000000007
    print(f"{inputs} strings of 1000000, {rounds} rounds: {back} back, checksum {checksum}")


main()
