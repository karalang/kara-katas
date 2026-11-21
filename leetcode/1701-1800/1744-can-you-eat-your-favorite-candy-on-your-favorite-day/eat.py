# LeetCode #1744: Can You Eat Your Favorite Candy on Your Favorite Day?
# -- mirrors eat.kara (the ★ arm).


def can_eat(candies_count, queries):
    before = [0]
    for c in candies_count:
        before.append(before[-1] + c)
    return [day + 1 <= before[t + 1] and (day + 1) * cap > before[t] for t, day, cap in queries]


seed = 1744


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    return next_random() * 32768 + next_random()


def batch(count, most, pile, asked):
    yes = 0
    check = 0
    for _ in range(count):
        n = (next_random() * 32768 + next_random()) % most + 1
        candies = [wide() % pile + 1 for _ in range(n)]
        total = sum(candies)
        queries = []
        for _ in range(asked):
            t = next_random() % n
            day = wide() % (total + total // 4 + 1)
            cap = 1000000000 if next_random() % 10 == 0 else wide() % (3 * pile) + 1
            queries.append([t, day, cap])
        for a in can_eat(candies, queries):
            bit = 1 if a else 0
            yes += bit
            check = (check * 2 + bit) % 1000000007
    print(f"{count} problems of up to {most} types of up to {pile} candies, {asked} queries each: {yes} yes, checksum {check}")


def show(answers):
    return "[" + ", ".join("true" if a else "false" for a in answers) + "]"


print(show(can_eat([7, 4, 5, 3, 8], [[0, 2, 2], [4, 2, 4], [2, 13, 1000000000]])))
print(show(can_eat([5, 2, 6, 4, 1], [[3, 1, 2], [4, 10, 3], [3, 10, 100], [4, 100, 30], [1, 3, 1]])))
print(show(can_eat([1], [[0, 0, 1], [0, 1, 1]])))
print(show(can_eat([100000, 100000, 100000], [[2, 0, 1], [2, 1, 100000], [2, 0, 200001], [0, 99999, 1], [0, 100000, 1000000000]])))
batch(3000, 6, 5, 6)
batch(100, 1000, 100000, 1000)
batch(2, 100000, 100000, 100000)
