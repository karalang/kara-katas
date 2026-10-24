# LeetCode #948: Bag of Tokens -- sorted, played from both ends.
# Mirrors bag_of_tokens_score.kara (the ★ arm) and its harness.


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


def show(tokens):
    return "[" + ",".join(str(v) for v in tokens) + "]"


def main():
    examples = [
        [100],
        [200, 100],
        [100, 200, 300, 400],
        [],
        [0, 0, 0],
        [5, 5, 5],
        [1, 10, 10, 10, 100],
        [100, 200, 300, 400],
    ]
    powers = [50, 150, 200, 9999, 0, 5, 1, 1000]
    for i in range(len(examples)):
        score = bag_of_tokens_score(examples[i], powers[i])
        print(f"{show(examples[i])} with power {powers[i]}: score {score}")
    count = 0
    total = 0
    check = 0
    for _ in range(300):
        n = next_random() % 41
        tokens = [next_random() % 100 for _ in range(n)]
        power = next_random() % 200
        score = bag_of_tokens_score(tokens, power)
        count += n
        total += score
        check = (check * 31 + score) % 1000000007
    print(f"300 random bags of {count} tokens: scores adding to {total}, checksum {check}")
    random = []
    total_sum = 0
    for _ in range(1000):
        v = next_random() % 10000
        random.append(v)
        total_sum += v
    print(f"1000 random tokens, power 5000: score {bag_of_tokens_score(random, 5000)}")
    print(f"1000 random tokens, power 0: score {bag_of_tokens_score(random, 0)}")
    print(f"1000 random tokens, power their sum {total_sum}: score {bag_of_tokens_score(random, total_sum)}")
    rising = [i + 1 for i in range(1000)]
    print(f"tokens 1 to 1000, power 1: score {bag_of_tokens_score(rising, 1)}")
    same = [9999] * 1000
    print(f"1000 tokens of 9999, power 9999: score {bag_of_tokens_score(same, 9999)}")


main()
