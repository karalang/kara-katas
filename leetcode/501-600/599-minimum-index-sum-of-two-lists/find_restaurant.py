# LeetCode #599: Minimum Index Sum of Two Lists -- index the first list.
#
# Mirrors star.kara: every string of list1 in a dict with its index, then
# a walk of list2 keeping the strings with the smallest index sum.


def find_restaurant(list1, list2):
    index = {}
    for i, s in enumerate(list1):
        index[s] = i
    best = len(list1) + len(list2)
    answer = []
    for j, s in enumerate(list2):
        i = index.get(s)
        if i is not None:
            total = i + j
            if total < best:
                best = total
                answer.clear()
            if total == best:
                answer.append(s)
    return answer


# ---- test harness ---------------------------------------------------------

def step(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def text(names):
    return "[" + ", ".join(names) + "]"


def spell(k):
    letters = []
    while True:
        letters.append(chr(97 + k % 26))
        k //= 26
        if k == 0:
            break
    return "".join(reversed(letters))


def sorted_answer(list1, list2):
    return sorted(find_restaurant(list1, list2))


def show(list1, list2):
    print(f"{text(list1)} {text(list2)} -> {text(sorted_answer(list1, list2))}")


def pick(pool, size, seed):
    order = list(range(len(pool)))
    out = []
    for k in range(size):
        j = k + step(seed) % (len(pool) - k)
        order[k], order[j] = order[j], order[k]
        out.append(pool[order[k]])
    return out


def main():
    show(["Shogun", "Tapioca Express", "Burger King", "KFC"], ["Piatti", "The Grill at Torrey Pines", "Hungry Hunter Steakhouse", "Shogun"])
    show(["Shogun", "Tapioca Express", "Burger King", "KFC"], ["KFC", "Shogun", "Burger King"])
    show(["happy", "sad", "good"], ["sad", "happy", "good"])
    show(["A"], ["A"])
    show(["a", "b", "c", "d"], ["d", "c", "b", "a"])
    show(["x", "y", "z"], ["p", "q", "z"])
    show(["KFC", "kfc", "Kfc"], ["kFC", "Kfc"])
    show(["m", "n", "o", "p"], ["p", "o", "x", "y", "m"])
    seed = [599]
    left = [f"left place {spell(k)}" for k in range(1000)] + ["both"]
    right = [f"right place {spell(k)}" for k in range(1000)] + ["both"]
    left.pop(0)
    right.pop(0)
    print(f"1000 and 1000 sharing the last -> {text(sorted_answer(left, right))}")
    forward = [f"place {spell(k)}" for k in range(1000)]
    backward = [f"place {spell(999 - k)}" for k in range(1000)]
    print(f"1000 and the same reversed -> {len(sorted_answer(forward, backward))} names tie")
    pool = ["Shogun", "KFC", "Piatti", "Burger King", "Tapioca Express", "sad", "happy", "good", "The Grill", "Noodle Bar", "Taqueria", "Dim Sum", "Pho", "Deli", "Bistro", "Ramen"]
    total = 0
    checksum = 0
    for _ in range(300):
        n = 1 + step(seed) % 12
        m = 1 + step(seed) % 12
        list1 = pick(pool, n, seed)
        list2 = pick(pool, m, seed)
        shared = any(s in list1 for s in list2)
        if not shared:
            at = step(seed) % m
            list2[at] = list1[step(seed) % n]
        got = sorted_answer(list1, list2)
        total += len(got)
        for s in got:
            for c in s:
                checksum = (checksum * 31 + ord(c)) % 1000000007
    print(f"300 random cases: {total} names in all, checksum {checksum}")


main()
