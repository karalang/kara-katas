# LeetCode #575: Distribute Candies -- a set of the types.
#
# Python mirror of distribute_candies.kara (the starred arm): the
# smaller of the number of types and n / 2.


def distribute_candies(candy_type):
    kinds = set()
    for c in candy_type:
        kinds.add(c)
    return min(len(kinds), len(candy_type) // 2)


# ---- test harness -----------------------------------------------------------

seed = 575


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(candy_type):
    print(f"{candy_type}: {distribute_candies(candy_type)}")


def main():
    show([1, 1, 2, 2, 3, 3])
    show([1, 1, 2, 3])
    show([6, 6, 6, 6])
    show([5, 5])
    show([5, -5])
    show([4, 3, 2, 1, 0, -1])
    show([-100000, 100000, -100000, 100000])
    show([7, 7, 7, 7, 7, 8])
    show([1, 1, 1, 2, 2, 3])
    show([1, 1, 2, 3, 4, 4])
    total = 0
    checksum = 0
    for _ in range(300):
        n = 2 * (1 + step() % 20)
        types = 1 + step() % 30
        pool = [(step() * 32768 + step()) % 200001 - 100000 for _ in range(types)]
        candy_type = [pool[step() % types] for _ in range(n)]
        got = distribute_candies(candy_type)
        total += got
        checksum = (checksum * 31 + got) % 1000000007
    print(f"300 random cases: {total} types eaten, checksum {checksum}")
    all_ = [i * 20 - 100000 for i in range(10000)]
    print(f"10000 candies, all different: {distribute_candies(all_)}")
    many = [i % 4999 for i in range(10000)]
    print(f"10000 candies, 4999 types: {distribute_candies(many)}")
    two = [-100000 if i % 3 == 0 else 100000 for i in range(10000)]
    print(f"10000 candies, 2 types: {distribute_candies(two)}")


main()
