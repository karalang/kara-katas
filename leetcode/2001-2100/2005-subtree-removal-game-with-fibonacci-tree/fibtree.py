# LeetCode #2005: Subtree Removal Game with Fibonacci Tree -- the mirror of
# the ★ arm, fibtree.kara; its output is byte-identical.


def find_game_winner(n):
    # value[k] is order(k)'s value; value[0] is unused
    value = [0] * (n + 1)
    for k in range(2, n + 1):
        left = value[k - 2] + 1 if k >= 3 else 0
        value[k] = left ^ (value[k - 1] + 1)
    return value[n] != 0


seed = 2005


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(b):
    return "true" if b else "false"


def main():
    # LeetCode's three examples
    for n in [3, 1, 2]:
        print(f"n = {n} -> {show(find_game_winner(n))}")
    # every n the constraints allow, A where Alice wins and B where Bob does
    print("".join("A" if find_game_winner(n) else "B" for n in range(1, 101)))
    # random queries
    alice = check = 0
    for _ in range(50000):
        n = next_random() % 100 + 1
        wins = find_game_winner(n)
        if wins:
            alice += 1
        check = (check * 31 + (n if wins else 0)) % 1000000007
    print(f"50000 queries: Alice wins {alice}, checksum {check}")


main()
