# Benchmark: LeetCode #948 Bag of Tokens -- the ★ arm, sorted and played
# from both ends, on bags of 1000 tokens, LeetCode's largest. Mirrors
# bag_of_tokens_score.kara, .c, .rs and go-seq/.


def bag_of_tokens_score(tokens, power):
    t = sorted(tokens)
    lo = 0
    hi = len(t) - 1
    p = power
    score = 0
    best = 0
    while lo <= hi:
        if p >= t[lo]:
            p -= t[lo]
            lo += 1
            score += 1
            best = max(best, score)
        elif score > 0 and lo < hi:
            p += t[hi]
            hi -= 1
            score -= 1
        else:
            break
    return best


seed = 948


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds, count, n = 500, 20, 1000
    bags = []
    powers = []
    for _ in range(count):
        bags.append([next_random() % 10000 for _ in range(n)])
        powers.append(next_random() % 10000)
    total = 0
    check = 0
    for r in range(rounds):
        for i in range(count):
            b = (r + i) % count
            s = bag_of_tokens_score(bags[b], powers[b])
            total += s
            check = (check * 1000003 + s) % 1000000007
    print(f"{rounds} rounds over {count} bags of {n} tokens: scores adding to {total}, checksum {check}")


main()
