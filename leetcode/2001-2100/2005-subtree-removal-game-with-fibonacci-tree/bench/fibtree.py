# LeetCode #2005: Subtree Removal Game with Fibonacci Tree -- the benchmark's
# Python twin, the same algorithm as fibtree.kara here.


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


def main():
    # 500000 values of n from 1 to 100 drawn once, then the ★ arm on each, 10 rounds
    queries = [next_random() % 100 + 1 for _ in range(500000)]
    calls = alice = check = 0
    for _ in range(10):
        for n in queries:
            wins = find_game_winner(n)
            calls += 1
            if wins:
                alice += 1
            check = (check * 31 + (n if wins else 0)) % 1000000007
    print(f"{calls} calls: Alice wins {alice}, checksum {check}")


main()
