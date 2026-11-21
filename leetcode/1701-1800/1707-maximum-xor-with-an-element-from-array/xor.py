# LeetCode #1707: Maximum XOR With an Element From Array -- the Python
# mirror of the ★ arm (xor.kara): the queries answered offline, by limit,
# against a binary trie of 30 bits.


def maximize_xor(nums, queries):
    values = sorted(nums)
    order = sorted(range(len(queries)), key=lambda i: queries[i][1])
    # children of each node, 0 for none: the root is node 0
    trie = [[0, 0]]
    nxt = 0
    answer = [-1] * len(queries)
    for i in order:
        x, m = queries[i]
        while nxt < len(values) and values[nxt] <= m:
            node = 0
            for bit in range(29, -1, -1):
                b = values[nxt] >> bit & 1
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


def value(top, seed):
    a = next_random(seed)
    return (a * 32768 + next_random(seed)) % top


def batch(count, most, top, seed):
    total = 0
    check = 0
    for _ in range(count):
        n = (next_random(seed) * 32768 + next_random(seed)) % most + 1
        q = (next_random(seed) * 32768 + next_random(seed)) % most + 1
        nums = [value(top, seed) for _ in range(n)]
        queries = []
        for _ in range(q):
            x = value(top, seed)
            queries.append([x, value(top, seed)])
        for a in maximize_xor(nums, queries):
            total += a
            check = (check * 31 + a + 1) % 1000000007
    print(f"{count} problems of up to {most} values below {top}: answers sum to {total}, checksum {check}")


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    # LeetCode's two examples, then no value small enough, and the largest
    print(show(maximize_xor([0, 1, 2, 3, 4], [[3, 1], [1, 3], [5, 6]])))
    print(show(maximize_xor([5, 2, 4, 6, 6, 3], [[12, 4], [8, 1], [6, 3]])))
    print(show(maximize_xor([7, 8], [[1, 6], [0, 0]])))
    print(show(maximize_xor([1000000000, 0], [[536870911, 1000000000]])))
    seed = [1707]
    batch(3000, 8, 16, seed)
    batch(300, 1000, 1000000000, seed)
    batch(3, 100000, 1000000000, seed)


main()
