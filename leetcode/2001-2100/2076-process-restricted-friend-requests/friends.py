# LeetCode #2076: Process Restricted Friend Requests -- Python mirror of
# the ★ arm (friends.kara): a union-find of the groups, found with path
# halving; a request between two groups refused if a restriction has one
# person in each.


def find(parent, x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def friend_requests(n, restrictions, requests):
    parent = list(range(n))
    answers = []
    for u, v in requests:
        a = find(parent, u)
        b = find(parent, v)
        allowed = True
        if a != b:
            for x0, y0 in restrictions:
                x = find(parent, x0)
                y = find(parent, y0)
                if (x == a and y == b) or (x == b and y == a):
                    allowed = False
                    break
            if allowed:
                parent[a] = b
        answers.append(allowed)
    return answers


seed = 2076


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_pairs(n, count):
    pairs = []
    for _ in range(count):
        a = next_random() % n
        b = (a + 1 + next_random() % (n - 1)) % n
        pairs.append([a, b])
    return pairs


def show_pairs(pairs):
    return "[" + ",".join(f"[{p[0]},{p[1]}]" for p in pairs) + "]"


def show_answers(answers):
    return "[" + ",".join("true" if a else "false" for a in answers) + "]"


def fold(answers, check):
    yes = 0
    for a in answers:
        bit = 1 if a else 0
        yes += bit
        check = (check * 3 + bit + 1) % 1000000007
    return yes, check


examples = [
    (3, [[0, 1]], [[0, 2], [2, 1]]),
    (3, [[0, 1]], [[1, 2], [0, 2]]),
    (5, [[0, 1], [1, 2], [2, 3]], [[0, 4], [1, 2], [3, 1], [3, 4]]),
    (2, [], [[0, 1], [1, 0]]),
    (2, [[1, 0]], [[0, 1], [0, 1]]),
    (4, [[0, 3]], [[0, 1], [2, 3], [1, 2], [0, 2], [1, 3]]),
    (6, [[0, 5], [1, 4]], [[0, 1], [4, 5], [2, 3], [1, 2], [3, 4], [0, 3], [2, 5]]),
]
for n, restrictions, requests in examples:
    answers = friend_requests(n, restrictions, requests)
    print(f"n = {n}, {show_pairs(restrictions)}, {show_pairs(requests)} -> {show_answers(answers)}")
total = 0
check = 0
for _ in range(300):
    n = next_random() % 59 + 2
    restrictions = random_pairs(n, next_random() % 41)
    requests = random_pairs(n, next_random() % 80 + 1)
    yes, check = fold(friend_requests(n, restrictions, requests), check)
    total += yes
print(f"300 problems: {total} accepted, checksum {check}")
restrictions = random_pairs(1000, 1000)
requests = random_pairs(1000, 1000)
yes, c = fold(friend_requests(1000, restrictions, requests), 0)
print(f"1000 people: {yes} accepted, checksum {c}")
