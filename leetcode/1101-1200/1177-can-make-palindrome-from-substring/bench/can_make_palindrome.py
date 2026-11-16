# LeetCode #1177: Can Make Palindrome from Substring -- the ★ arm's bench
# in Python: the parity masks of every prefix, each query's odd letters
# counted with int.bit_count on two masks XORed. The same string, the same
# queries and the same 200 calls.


def can_make_pali_queries(s, queries):
    masks = [0]
    for c in s.encode():
        masks.append(masks[-1] ^ (1 << (c - 97)))
    return [(masks[q[1] + 1] ^ masks[q[0]]).bit_count() // 2 <= q[2] for q in queries]


seed = 1177


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


s = "".join(chr(97 + next_random() % 26) for _ in range(100000))
queries = []
for _ in range(100000):
    a = next_random() % 100000
    b = next_random() % 100000
    queries.append([min(a, b), max(a, b), next_random() % 14])
calls = 200
check = 0
for _ in range(calls):
    for a in can_make_pali_queries(s, queries):
        check = (check * 3 + (2 if a else 1)) % 1000000007
print(f"{calls} calls: checksum {check}")
