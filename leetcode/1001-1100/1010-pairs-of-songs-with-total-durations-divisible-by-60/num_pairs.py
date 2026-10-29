# LeetCode #1010: Pairs of Songs With Total Durations Divisible by 60 --
# remainder counts in one pass. Mirrors num_pairs.kara line for line.


def num_pairs(time):
    seen = [0] * 60
    pairs = 0
    for t in time:
        r = t % 60
        pairs += seen[(60 - r) % 60]
        seen[r] += 1
    return pairs


seed = 1010


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(nums):
    return "[" + ",".join(str(x) for x in nums) + "]"


def main():
    examples = [
        [30, 20, 150, 100, 40],
        [60, 60, 60],
        [1],
        [30, 30],
        [59, 1, 61, 119, 2],
        [120, 180, 240, 300, 360],
        [10, 50, 110, 70, 20, 40, 30, 90],
        [500, 40, 100, 20, 499, 1],
    ]
    for time in examples:
        print(f"time = {show(time)} -> {num_pairs(time)}")
    sixties, thirties, cycle, sevens = [], [], [], []
    for i in range(60000):
        sixties.append(60)
        thirties.append(30 if i % 2 == 0 else 90)
        cycle.append(1 + i % 500)
        sevens.append(7)
    large = [
        ("60000 songs of 60", sixties),
        ("60000 songs of 30 and 90", thirties),
        ("60000 songs cycling 1..500", cycle),
        ("60000 songs of 7", sevens),
    ]
    for name, time in large:
        print(f"{name} -> {num_pairs(time)}")
    for count, most in [(3000, 10), (300, 1000), (5, 60000)]:
        songs = 0
        total = 0
        check = 0
        for _ in range(count):
            size = 1 + next_random() % most
            time = [1 + next_random() % 500 for _ in range(size)]
            pairs = num_pairs(time)
            songs += size
            total += pairs
            check = (check * 31 + pairs) % 1000000007
        print(f"{count} random playlists of {songs} songs: {total} pairs, checksum {check}")


main()
