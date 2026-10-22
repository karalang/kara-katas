# Benchmark for #851: Loud and Rich -- Python twin of the Kāra ★ arm
# (memoised search up the richer-than graph).
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
    for pair in richer:
        richer_than[pair[1]].append(pair[0])
    answer = [-1] * n
    for x in range(n):
        answer_for(x, richer_than, quiet, answer)
    return answer


seed = 851


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count = 64
    rounds = 10000
    n = 500
    cases = []
    for g in range(count):
        odds = 2 << (g % 8)
        rank = list(range(n))
        for i in range(n - 1, 0, -1):
            j = next_random() % (i + 1)
            rank[i], rank[j] = rank[j], rank[i]
        richer = []
        for i in range(n):
            for j in range(i + 1, n):
                if next_random() % 1000 < odds:
                    richer.append([rank[i], rank[j]])
        quiet = list(range(n))
        for i in range(n - 1, 0, -1):
            j = next_random() % (i + 1)
            quiet[i], quiet[j] = quiet[j], quiet[i]
        cases.append((richer, quiet))
    total = 0
    checksum = 0
    for round_ in range(rounds):
        richer, quiet = cases[round_ % count]
        answer = loud_and_rich(richer, quiet)
        for a in answer:
            total += quiet[a]
            checksum = (checksum * 31 + a) % 1000000007
    print(f"{rounds} rounds of {count} cases: quietness sums to {total}, checksum {checksum}")


main()
