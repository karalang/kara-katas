# LeetCode #2353: Design a Food Rating System -- the bench, the ★ arm: lazy
# heaps, a dict from each food to its rating and its cuisine, and for each
# cuisine a heapq of (-rating, food) holding every key a food was ever
# given; a query pops the tops that are no longer true.

import heapq

seed = 2353


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


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


def four_letters(v):
    return chr(97 + v // 17576) + chr(97 + v // 676 % 26) + chr(97 + v // 26 % 26) + chr(97 + v % 26)


def main():
    n = 10000
    foods = [four_letters(i * 7919 % 456976) for i in range(n)]
    cuisines = [f"c{next_random() % 100}" for _ in range(n)]
    ratings = [1 + next_random() % 100000000 for _ in range(n)]
    calls = []
    for i in range(100000):
        f = next_random() % n
        if i % 3 == 2:
            calls.append((1, cuisines[f], 0))
        else:
            calls.append((0, foods[f], 1 + next_random() % 100000000))
    check = 0
    for p in range(100):
        table = FoodRatings(foods, cuisines, ratings)
        for kind, name, rating in calls:
            if kind == 0:
                table.change_rating(name, rating)
            else:
                for b in table.highest_rated(name).encode():
                    check = (check * 31 + b) % 1000000007
                check = (check * 31 + p) % 1000000007
    print(f"100 passes over 10^4 foods and 10^5 calls: checksum {check}")


main()
