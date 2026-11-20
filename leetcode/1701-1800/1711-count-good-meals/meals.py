# LeetCode #1711: Count Good Meals -- the Python mirror of the ★ arm
# (meals.kara): one pass, each dish paired with the earlier dishes that
# make each power of two with it, counted in a map.


def count_pairs(deliciousness):
    seen = {}
    pairs = 0
    for d in deliciousness:
        for b in range(22):
            pairs += seen.get((1 << b) - d, 0)
        seen[d] = seen.get(d, 0) + 1
    return pairs % 1000000007


def next_random(state):
    state[0] = (state[0] * 1103515245 + 12345) % 2147483648
    return state[0] // 65536


def batch(count, most, top, seed):
    total = 0
    check = 0
    for _ in range(count):
        n = next_random(seed) % most + 1
        deliciousness = []
        for _ in range(n):
            a = next_random(seed)
            deliciousness.append((a * 32768 + next_random(seed)) % (top + 1))
        answer = count_pairs(deliciousness)
        total += answer
        check = (check * 31 + answer + n) % 1000000007
    print(f"{count} lists of up to {most} dishes up to {top}: answers sum to {total}, checksum {check}")


def main():
    # LeetCode's two examples, then one dish, two zeros, and two dishes
    # of 2^20, the largest
    print(count_pairs([1, 3, 5, 7, 9]))
    print(count_pairs([1, 1, 1, 3, 3, 3, 7]))
    print(count_pairs([1]))
    print(count_pairs([0, 0]))
    print(count_pairs([1048576, 1048576]))
    seed = [1711]
    batch(3000, 12, 16, seed)
    batch(300, 1000, 4096, seed)
    batch(10, 100000, 1000, seed)


main()
