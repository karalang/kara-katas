# LeetCode #1707: Maximum XOR With an Element From Array -- the bench's
# Python mirror: the ★ arm on 4 random problems of 100000 values and
# 100000 queries, all drawn first, each answered 3 times.


def maximize_xor(nums, queries):
    # the queries offline by limit, against a 30-bit trie of the values allowed
    values = sorted(nums)
    order = sorted(range(len(queries)), key=lambda i: queries[i][1])
    trie = [[0, 0]]
    nxt = 0
    answer = [-1] * len(queries)
    for i in order:
        x, m = queries[i]
        while nxt < len(values) and values[nxt] <= m:
            node = 0
            v = values[nxt]
            for bit in range(29, -1, -1):
                b = v >> bit & 1
                if trie[node][b] == 0:
                    trie.append([0, 0])
                    trie[node][b] = len(trie) - 1
                node = trie[node][b]
            nxt += 1
        if nxt == 0:
            continue
        node = 0
        best = 0
        for bit in range(29, -1, -1):
            want = (x >> bit & 1) ^ 1
            if trie[node][want] != 0:
                best |= 1 << bit
                node = trie[node][want]
            else:
                node = trie[node][want ^ 1]
        answer[i] = best
    return answer


def next_random(state):
    state[0] = (state[0] * 1103515245 + 12345) % 2147483648
    return state[0] // 65536


def value(seed):
    a = next_random(seed)
    return (a * 32768 + next_random(seed)) % 1000000000


def main():
    count, rounds, n = 4, 3, 100000
    seed = [1707]
    problems = []
    for _ in range(count):
        nums = [value(seed) for _ in range(n)]
        queries = []
        for _ in range(n):
            x = value(seed)
            queries.append((x, value(seed)))
        problems.append((nums, queries))
    total = 0
    check = 0
    for r in range(rounds):
        for nums, queries in problems:
            for a in maximize_xor(nums, queries):
                total += a
                check = (check * 31 + a + 1 + r) % 1000000007
    print(f"{count} problems of {n} values and {n} queries, {rounds} rounds: answers sum to {total}, checksum {check}")


main()
