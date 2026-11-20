# LeetCode #1744: Can You Eat Your Favorite Candy on Your Favorite Day?
# -- the bench (eat.kara in Python): prefix sums, then two comparisons a
# query.


def can_eat(candies_count, queries):
    before = [0]
    for c in candies_count:
        before.append(before[-1] + c)
    answers = []
    for t, day, cap in queries:
        answers.append(day + 1 <= before[t + 1] and (day + 1) * cap > before[t])
    return answers


seed = 1744


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    return next_random() * 32768 + next_random()


count, rounds, n = 10, 30, 100000
problems = []
for _ in range(count):
    candies = [next_random() % 20 + 1 for _ in range(n)]
    total = sum(candies)
    queries = []
    for _ in range(n):
        t = wide() % n
        day = wide() % total
        cap = next_random() % 30 + 1
        queries.append([t, day, cap])
    problems.append((candies, queries))
yes = 0
check = 0
for r in range(rounds):
    for candies, queries in problems:
        here = 0
        for i, a in enumerate(can_eat(candies, queries)):
            if a:
                here += 1
                check = (check + i * 7 + r) % 1000000007
        yes += here
print(f"{count} problems of {n} types and {n} queries, {rounds} rounds: {yes} yes, checksum {check}")
