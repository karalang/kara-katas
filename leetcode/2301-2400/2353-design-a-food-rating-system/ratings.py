# LeetCode #2353: Design a Food Rating System -- the Python mirror of the
# ★ arm: for each cuisine a heap of (-rating, food) holding every rating a
# food was ever given; a change only pushes, and a query pops the tops
# whose rating is no longer the food's.

import heapq


class FoodRatings:
    def __init__(self, foods, cuisines, ratings):
        self.rating = {}
        self.cuisine_of = {}
        self.heaps = {}
        for food, cuisine, rating in zip(foods, cuisines, ratings):
            self.rating[food] = rating
            self.cuisine_of[food] = cuisine
            heapq.heappush(self.heaps.setdefault(cuisine, []), (-rating, food))

    def change_rating(self, food, new_rating):
        self.rating[food] = new_rating
        heapq.heappush(self.heaps[self.cuisine_of[food]], (-new_rating, food))

    def highest_rated(self, cuisine):
        heap = self.heaps[cuisine]
        while True:
            negated, food = heap[0]
            if self.rating[food] == -negated:
                return food
            heapq.heappop(heap)


def run(foods, cuisines, ratings, calls):
    table = FoodRatings(foods, cuisines, ratings)
    answers = []
    for kind, name, rating in calls:
        if kind == 0:
            table.change_rating(name, rating)
        else:
            answers.append(table.highest_rated(name))
    return answers


SEED = [2353]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def tally(answers, check):
    for a in answers:
        for c in a:
            check = (check * 31 + ord(c)) % 1000000007
        check = (check * 31 + 1) % 1000000007
    return check


def three_letters(v):
    return chr(97 + v // 676) + chr(97 + v // 26 % 26) + chr(97 + v % 26)


def main():
    # LeetCode's example; three foods tied, the least name first; one food
    # raised past another and lowered back
    print(" ".join(run(
        ["kimchi", "miso", "sushi", "moussaka", "ramen", "bulgogi"],
        ["korean", "japanese", "japanese", "greek", "japanese", "korean"],
        [9, 12, 8, 15, 14, 7],
        [(1, "korean", 0), (1, "japanese", 0), (0, "sushi", 16), (1, "japanese", 0),
         (0, "ramen", 16), (1, "japanese", 0)])))
    print(" ".join(run(["b", "ab", "a"], ["x", "x", "x"], [5, 5, 5],
                       [(1, "x", 0), (0, "a", 4), (1, "x", 0), (0, "ab", 4), (1, "x", 0)])))
    print(" ".join(run(["pie", "tart"], ["sweet", "sweet"], [100000000, 1],
                       [(1, "sweet", 0), (0, "tart", 100000000), (1, "sweet", 0),
                        (0, "pie", 1), (1, "sweet", 0), (0, "pie", 100000000), (1, "sweet", 0)])))
    # 500 foods over 20 cuisines, then 2 * 10^4 calls, two changes to every
    # query
    foods = [three_letters(i * 7919 % 1000) for i in range(500)]
    cuisines = ["c" + chr(97 + i % 20) for i in range(500)]
    ratings = [i * 37 % 100 + 1 for i in range(500)]
    calls = []
    for i in range(20000):
        if i % 3 == 2:
            calls.append((1, "c" + chr(97 + i % 20), 0))
        else:
            calls.append((0, foods[i * 13 % 500], i * 7 % 100 + 1))
    answers = run(foods, cuisines, ratings, calls)
    print(f"2 * 10^4 calls: checksum {tally(answers, 0)}, letters {sum(len(a) for a in answers)}")
    # 2000 random scripts: 1 to 8 foods of 1 to 3 letters from a to c over
    # cuisines x, y and z, rated 1 to 4, then 1 to 40 calls, three changes
    # to every two queries
    check = 0
    letters = 0
    firsts = 0
    for _ in range(2000):
        n = 1 + next_random() % 8
        foods = []
        while len(foods) < n:
            length = 1 + next_random() % 3
            name = "".join(chr(97 + next_random() % 3) for _ in range(length))
            if name not in foods:
                foods.append(name)
        cuisines = [chr(120 + next_random() % 3) for _ in range(n)]
        ratings = [1 + next_random() % 4 for _ in range(n)]
        calls = []
        for _ in range(1 + next_random() % 40):
            if next_random() % 5 < 3:
                food = foods[next_random() % n]
                calls.append((0, food, 1 + next_random() % 4))
            else:
                calls.append((1, cuisines[next_random() % n], 0))
        answers = run(foods, cuisines, ratings, calls)
        check = tally(answers, check)
        letters += sum(len(a) for a in answers)
        firsts += sum(1 for a in answers if a == foods[0])
    print(f"2000 scripts: checksum {check}, letters {letters}, the first food {firsts}")


main()
