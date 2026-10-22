# LeetCode #851: Loud and Rich -- Python mirror of the ★ arm and its harness.
import sys

sys.setrecursionlimit(10000)


def answer_for(x, richer_than, quiet, answer):
    if answer[x] < 0:
        best = x
        for y in richer_than[x]:
            candidate = answer_for(y, richer_than, quiet, answer)
            if quiet[candidate] < quiet[best]:
                best = candidate
        answer[x] = best
    return answer[x]


def loud_and_rich(richer, quiet):
    n = len(quiet)
    richer_than = [[] for _ in range(n)]
    for a, b in richer:
        richer_than[b].append(a)
    answer = [-1] * n
    for x in range(n):
        answer_for(x, richer_than, quiet, answer)
    return answer


def fmt(v):
    if isinstance(v, list):
        return "[" + ", ".join(fmt(x) for x in v) + "]"
    return str(v)


def show(richer, quiet):
    print(f"{fmt(richer)}, {fmt(quiet)} -> {fmt(loud_and_rich(richer, quiet))}")


seed = 851


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def shuffled(n):
    order = list(range(n))
    for i in range(n - 1, 0, -1):
        j = next_random() % (i + 1)
        order[i], order[j] = order[j], order[i]
    return order


def random_case(n, keep):
    rank = shuffled(n)
    richer = []
    for i in range(n):
        for j in range(i + 1, n):
            if next_random() % 100 < keep:
                richer.append([rank[i], rank[j]])
    m = len(richer)
    for i in range(m - 1, 0, -1):
        j = next_random() % (i + 1)
        richer[i], richer[j] = richer[j], richer[i]
    return richer, shuffled(n)


def digest(answer):
    check = 0
    for a in answer:
        check = (check * 31 + a + 1) % 1000000007
    return check


def main():
    show([[1, 0], [2, 1], [3, 1], [3, 7], [4, 3], [5, 3], [6, 3]], [3, 2, 5, 4, 6, 1, 7, 0])
    show([], [0])
    show([[0, 1]], [1, 0])
    show([[0, 1]], [0, 1])
    show([], [2, 0, 1])
    show([[0, 1], [1, 2], [2, 3]], [3, 2, 1, 0])
    show([[0, 1], [1, 2], [2, 3]], [0, 1, 2, 3])
    show([[0, 3], [1, 3], [2, 3]], [2, 0, 1, 3])
    show([[0, 1], [0, 2], [0, 3]], [3, 0, 1, 2])
    show([[1, 0], [2, 0], [3, 1], [3, 2]], [3, 2, 1, 0])
    show([[0, 2], [1, 2], [2, 3], [2, 4]], [4, 3, 2, 1, 0])
    n = 500
    chain = [[i - 1, i] for i in range(1, n)]
    quiet_up = list(range(n))
    quiet_down = [n - 1 - i for i in range(n)]
    print(f"a chain of 500, quieter going down: digest {digest(loud_and_rich(chain, quiet_down))}")
    chain.reverse()
    print(f"the same chain, its pairs reversed, louder going down: digest {digest(loud_and_rich(chain, quiet_up))}")
    dense, dense_quiet = random_case(n, 50)
    print(f"500 people, {len(dense)} pairs: digest {digest(loud_and_rich(dense, dense_quiet))}")
    sparse, sparse_quiet = random_case(n, 1)
    print(f"500 people, {len(sparse)} pairs: digest {digest(loud_and_rich(sparse, sparse_quiet))}")
    total = 0
    check = 0
    for _ in range(300):
        size = 1 + next_random() % 12
        keep = next_random() % 101
        richer, quiet = random_case(size, keep)
        answer = loud_and_rich(richer, quiet)
        for a in answer:
            total += quiet[a]
        check = (check * 31 + digest(answer)) % 1000000007
    print(f"300 random cases: the answers' quietness sums to {total}, checksum {check}")


main()
