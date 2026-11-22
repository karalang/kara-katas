# LeetCode #2766: Relocate Marbles -- the ★ arm in Python (marbles.kara):
# the occupied positions in a set; each move takes its from position out
# and puts its to position in, and the set is sorted at the end.


def relocate_marbles(nums, move_from, move_to):
    occupied = set(nums)
    for a, b in zip(move_from, move_to):
        occupied.discard(a)
        occupied.add(b)
    return sorted(occupied)


seed = 2766


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    return next_random() * 32768 + next_random()


def case(n, moves, top):
    # n marbles at positions from 1 to top, then moves each from a place
    # that holds marbles at the time to any place from 1 to top
    nums = [wide() % top + 1 for _ in range(n)]
    places = []
    where = {}
    for x in nums:
        if x not in where:
            where[x] = len(places)
            places.append(x)
    move_from = []
    move_to = []
    for _ in range(moves):
        a = places[wide() % len(places)]
        b = wide() % top + 1
        move_from.append(a)
        move_to.append(b)
        if a != b:
            k = where.pop(a)
            last = places.pop()
            if last != a:
                places[k] = last
                where[last] = k
            if b not in where:
                where[b] = len(places)
                places.append(b)
    return nums, move_from, move_to


def fold(places, acc):
    acc[0] += len(places)
    for p in places:
        acc[1] = (acc[1] * 31 + p) % 1000000007


def main():
    print(relocate_marbles([1, 6, 7, 8], [1, 7, 2], [2, 9, 5]))
    print(relocate_marbles([1, 1, 3, 3], [1, 3], [2, 2]))
    print(relocate_marbles([4, 4], [4, 4], [4, 9]))
    print(relocate_marbles([1000000000, 1], [1, 1000000000], [1000000000, 5]))
    acc = [0, 0]
    for _ in range(3000):
        n = next_random() % 10 + 1
        moves = next_random() % 10 + 1
        top = next_random() % 15 + 1
        fold(relocate_marbles(*case(n, moves, top)), acc)
    print(f"3000 small cases: {acc[0]} places, checksum {acc[1]}")
    acc = [0, 0]
    for _ in range(5):
        fold(relocate_marbles(*case(100000, 100000, 1000000000)), acc)
    print(f"5 cases of 100000 marbles and moves: {acc[0]} places, checksum {acc[1]}")


main()
