# LeetCode #2766: Relocate Marbles -- the bench (marbles.kara in Python):
# the occupied positions in a set, each move taking its from position out
# and putting its to position in, sorted at the end.


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
    nums = [wide() % top + 1 for _ in range(n)]
    places = []
    slot = [-1] * (top + 1)
    for x in nums:
        if slot[x] < 0:
            slot[x] = len(places)
            places.append(x)
    move_from = []
    move_to = []
    for _ in range(moves):
        a = places[wide() % len(places)]
        b = wide() % top + 1
        move_from.append(a)
        move_to.append(b)
        if a != b:
            k = slot[a]
            slot[a] = -1
            last = places.pop()
            if last != a:
                places[k] = last
                slot[last] = k
            if slot[b] < 0:
                slot[b] = len(places)
                places.append(b)
    return nums, move_from, move_to


def main():
    count, rounds = 20, 5
    cases = [case(100000, 100000, 1000000) for _ in range(count)]
    total = check = 0
    for r in range(rounds):
        for nums, move_from, move_to in cases:
            places = relocate_marbles(nums, move_from, move_to)
            total += len(places)
            check = (check * 31 + len(places) + r) % 1000000007
            for p in places:
                check = (check * 31 + p) % 1000000007
    print(f"{count} cases of 100000 marbles and moves, {rounds} rounds: {total} places, checksum {check}")


main()
