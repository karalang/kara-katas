# LeetCode #1718: Construct the Lexicographically Largest Valid Sequence
# -- the bench (sequence.kara): the first empty slot filled with the
# largest number that fits, backtracking when none does.
import sys

sys.setrecursionlimit(10000)


def place(seq, used, at, n):
    while at < len(seq) and seq[at] != 0:
        at += 1
    if at == len(seq):
        return True
    for v in range(n, 0, -1):
        if used[v]:
            continue
        if v > 1 and (at + v >= len(seq) or seq[at + v] != 0):
            continue
        used[v] = True
        seq[at] = v
        if v > 1:
            seq[at + v] = v
        if place(seq, used, at + 1, n):
            return True
        used[v] = False
        seq[at] = 0
        if v > 1:
            seq[at + v] = 0
    return False


def construct_distanced_sequence(n):
    seq = [0] * (2 * n - 1)
    used = [False] * (n + 1)
    place(seq, used, 0, n)
    return seq


def main():
    rounds = 2000
    values = 0
    check = 0
    for r in range(rounds):
        for n in range(1, 21):
            for v in construct_distanced_sequence(n):
                values += 1
                check = (check * 31 + v + r) % 1000000007
    print(f"every n from 1 to 20, {rounds} rounds: {values} values, checksum {check}")


main()
