# LeetCode #2115: Find All Possible Recipes from Given Supplies -- the
# Python mirror of recipes.kara (the ★ arm): Kahn's order, each recipe
# counting the ingredients it lacks, a queue starting with the supplies.
# O(n + total ingredients).

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
        for i in needed_by.get(item, []):
            lacking[i] -= 1
            if lacking[i] == 0:
                made.append(recipes[i])
                queue.append(recipes[i])
    return made


# ---- test harness ----------------------------------------------------------

def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def show(v):
    return "[" + ", ".join(v) + "]"


def made(recipes, ingredients, supplies):
    return sorted(find_all_recipes(recipes, ingredients, supplies))


def main():
    examples = [
        (["bread"], [["yeast", "flour"]], ["yeast", "flour", "corn"]),
        (["bread", "sandwich"], [["yeast", "flour"], ["bread", "meat"]], ["yeast", "flour", "meat"]),
        (["bread", "sandwich", "burger"], [["yeast", "flour"], ["bread", "meat"], ["sandwich", "meat", "bread"]], ["yeast", "flour", "meat"]),
        (["egg", "hen"], [["hen"], ["egg", "grain"]], ["grain"]),
        (["soup", "stew"], [["salt", "water"], ["soup", "meat"]], ["water", "meat"]),
        (["c", "b", "a"], [["b"], ["a"], ["x"]], ["x"]),
    ]
    for recipes, ingredients, supplies in examples:
        print(f"{show(recipes)} from {show(supplies)} -> {show(made(recipes, ingredients, supplies))}")
    seed = [2115]
    total = 0
    check = 0
    for _ in range(2000):
        n = next_random(seed) % 8 + 1
        recipes = [f"r{i}" for i in range(n)]
        have = next_random(seed) % 6 + 1
        supplies = [f"s{i}" for i in range(have)]
        ingredients = []
        for i in range(n):
            need = []
            for _ in range(next_random(seed) % 4 + 1):
                pick = next_random(seed) % (8 + n)
                item = f"s{pick}" if pick < 8 else f"r{pick - 8}"
                if item != f"r{i}" and item not in need:
                    need.append(item)
            if not need:
                need.append("s0")
            ingredients.append(need)
        got = made(recipes, ingredients, supplies)
        total += len(got)
        for r in got:
            check = (check * 31 + ord(r[1])) % 1000000007
        check = (check * 37 + len(got)) % 1000000007
    print(f"2000 kitchens: {total} recipes made, checksum {check}")
    recipes = [f"r{99 - i}" for i in range(100)]
    supplies = [f"s{i}" for i in range(100)]
    chain = []
    for i in range(100):
        k = 99 - i
        need = [f"s{(k + j) % 100}" for j in range(99)]
        if k > 0:
            need.append(f"r{k - 1}")
        chain.append(need)
    print(f"chain of 100 -> {len(made(recipes, chain, supplies))} made")
    short = [f"s{i}" for i in range(1, 100)]
    print(f"chain of 100, s0 missing -> {len(made(recipes, chain, short))} made")


main()
