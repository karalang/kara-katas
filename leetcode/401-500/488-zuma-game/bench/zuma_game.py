# Benchmark for #488: Python mirror of the ★ arm (breadth first); see
# zuma_game.kara.


def shrink(board):
    b = list(board)
    while True:
        kept = []
        removed = False
        i = 0
        while i < len(b):
            j = i
            while j < len(b) and b[j] == b[i]:
                j += 1
            if j - i >= 3:
                removed = True
            else:
                kept.extend(b[i:j])
            i = j
        b = kept
        if not removed:
            return b


def find_min_step(board, hand):
    boards = [list(board)]
    hands = [sorted(hand)]
    seen = set()
    steps = 0
    while boards:
        steps += 1
        next_boards = []
        next_hands = []
        for b, h in zip(boards, hands):
            for t, c in enumerate(h):
                if t > 0 and h[t - 1] == c:
                    continue
                for i in range(len(b) + 1):
                    starts_run = i < len(b) and b[i] == c and (i == 0 or b[i - 1] != c)
                    splits_pair = 0 < i < len(b) and b[i - 1] == b[i] and b[i] != c
                    if not starts_run and not splits_pair:
                        continue
                    after = shrink(b[:i] + [c] + b[i:])
                    if not after:
                        return steps
                    rest = h[:t] + h[t + 1:]
                    state = "".join(after) + "|" + "".join(rest)
                    if state not in seen:
                        seen.add(state)
                        next_boards.append(after)
                        next_hands.append(rest)
        boards = next_boards
        hands = next_hands
    return -1


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    colours = ["R", "Y", "B", "G", "W"]
    boards = []
    hands = []
    seed = [488]
    for c in range(60):
        palette = 2 + c % 3
        balls = []
        while len(balls) < 16:
            ball = colours[next_random(seed) % palette]
            if len(balls) >= 2 and balls[-1] == ball and balls[-2] == ball:
                continue
            balls.append(ball)
        boards.append("".join(balls))
        hands.append("".join(colours[next_random(seed) % palette] for _ in range(5)))
    cleared = 0
    total = 0
    checksum = 0
    for board, hand in zip(boards, hands):
        steps = find_min_step(board, hand)
        if steps >= 0:
            cleared += 1
            total += steps
        checksum = (checksum * 31 + steps + 2) % 1000000007
    print(f"60 cases of 16 balls and a hand of 5: {cleared} cleared with {total} balls, checksum {checksum}")


main()
