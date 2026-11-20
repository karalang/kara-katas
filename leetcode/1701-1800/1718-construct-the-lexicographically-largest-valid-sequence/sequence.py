# LeetCode #1718: Construct the Lexicographically Largest Valid Sequence --
# the Python mirror of the ★ arm (sequence.kara): the first empty slot
# filled with the largest number still free that fits, backtracking when
# none does.


def construct_distanced_sequence(n):
    seq = [0] * (2 * n - 1)
    used = [False] * (n + 1)

    def place(at):
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
            if place(at + 1):
                return True
            used[v] = False
            seq[at] = 0
            if v > 1:
                seq[at + v] = 0
        return False

    place(0)
    return seq


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    # LeetCode's two examples, then the smallest two and the largest
    print(show(construct_distanced_sequence(3)))
    print(show(construct_distanced_sequence(5)))
    print(show(construct_distanced_sequence(1)))
    print(show(construct_distanced_sequence(2)))
    print(show(construct_distanced_sequence(20)))
    # every n the constraints allow
    values = 0
    check = 0
    for n in range(1, 21):
        for v in construct_distanced_sequence(n):
            values += 1
            check = (check * 31 + v) % 1000000007
    print(f"every n from 1 to 20: {values} values, checksum {check}")


main()
