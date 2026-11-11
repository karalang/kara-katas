# LeetCode #2115: Find All Possible Recipes from Given Supplies -- the
# benchmark, the same algorithm as recipes.kara: Kahn's order over names,
# a dict from each ingredient to the recipes needing it and a deque
# starting with the supplies.

from collections import deque


def find_all_recipes(recipes, ingredients, supplies):
    needed_by = {}
    lacking = []
    for i in range(len(recipes)):
        lacking.append(len(ingredients[i]))
        for item in ingredients[i]:
            needed_by.setdefault(item, []).append(i)
    queue = deque(supplies)
    made = []
    while queue:
        item = queue.popleft()
        users = needed_by.get(item)
        if users is not None:
            for i in users:
                lacking[i] -= 1
                if lacking[i] == 0:
                    made.append(recipes[i])
                    queue.append(recipes[i])
    return made


seed = 2115


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    recipes = [f"r{i}" for i in range(100)]
    supplies = [f"s{i}" for i in range(56)]
    kitchens = []
    for _ in range(40):
        ingredients = []
        for i in range(100):
            need = []
            for _ in range(next_random() % 8 + 1):
                pick = next_random() % (60 + i)
                item = f"s{pick}" if pick < 60 else f"r{pick - 60}"
                if item not in need:
                    need.append(item)
            if not need:
                need.append("s0")
            ingredients.append(need)
        kitchens.append(ingredients)
    total = 0
    check = 0
    for rnd in range(10):
        for k in range(40):
            i = (rnd * 37 + k) % 100
            kitchens[k][i][0] = f"s{(rnd + k) % 50}"
            got = find_all_recipes(recipes, kitchens[k], supplies)
            total += len(got)
            check = (check * 31 + len(got)) % 1000000007
    print(f"400 solves: {total} recipes made, checksum {check}")


main()
