# LeetCode #2027: Minimum Moves to Convert String -- the ★ arm in Python, the
# same algorithm and workload as moves.kara.


def minimum_moves(s):
    key = list(s)
    moves = 0
    i = 0
    while i < len(key):
        if key[i] == "X":
            moves += 1
            i += 3
        else:
            i += 1
    return moves


seed = 2027


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    strings = []
    for _ in range(2000):
        share = next_random() % 101
        strings.append("".join("X" if next_random() % 100 < share else "O" for _ in range(1000)))
    calls = total = check = 0
    for _ in range(50):
        for s in strings:
            moves = minimum_moves(s)
            calls += 1
            total += moves
            check = (check * 31 + moves) % 1000000007
    print(f"{calls} calls: {total} moves, checksum {check}")


main()
