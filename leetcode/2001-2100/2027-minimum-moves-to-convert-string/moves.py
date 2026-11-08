# LeetCode #2027: Minimum Moves to Convert String -- a Python mirror of the
# ★ arm (moves.kara): take a move at the leftmost X and jump three places.
# Same output, byte for byte.


def minimum_moves(s):
    moves = 0
    i = 0
    while i < len(s):
        if s[i] == "X":
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


def key_of(length, x_in_100):
    return "".join("X" if next_random() % 100 < x_in_100 else "O" for _ in range(length))


def main():
    examples = ["XXX", "XXOX", "OOOO", "XOXOXO", "OXOOX", "OXX", "XOO", "OOXOOOXXXXOX"]
    for s in examples:
        print(f"{s} -> {minimum_moves(s)}")
    total = 0
    check = 0
    for _ in range(3000):
        length = next_random() % 28 + 3
        share = next_random() % 101
        moves = minimum_moves(key_of(length, share))
        total += moves
        check = (check * 31 + moves) % 1000000007
    print(f"3000 strings of up to 30 places: {total} moves, checksum {check}")
    total = 0
    check = 0
    for a in range(6):
        moves = minimum_moves(key_of(1000, [1, 10, 33, 50, 90, 100][a]))
        total += moves
        check = (check * 31 + moves) % 1000000007
    print(f"6 strings of 1000 places: {total} moves, checksum {check}")


main()
