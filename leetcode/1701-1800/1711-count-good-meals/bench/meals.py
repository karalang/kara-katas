# LeetCode #1711: Count Good Meals -- the Python mirror of the bench
# (meals.kara): one pass, each dish paired with the earlier dishes that
# make each of the 22 powers with it, counted in a dict, on 10 random
# lists of 100000 dishes, each answered 3 times.


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


def main():
    count = 10
    rounds = 3
    n = 100000
    top = 1 << 20
    seed = [1711]
    lists = []
    for _ in range(count):
        values = []
        for _ in range(n):
            a = next_random(seed)
            values.append((a * 32768 + next_random(seed)) % (top + 1))
        lists.append(values)
    total = 0
    check = 0
    for r in range(rounds):
        for deliciousness in lists:
            answer = count_pairs(deliciousness)
            total += answer
            check = (check * 31 + answer + r) % 1000000007
    print(f"{count} lists of {n} dishes, {rounds} rounds: answers sum to {total}, checksum {check}")


main()
