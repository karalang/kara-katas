# LeetCode #1629: Slowest Key -- the bench's Python mirror: the ★ arm on
# 1000 random problems of 1000 presses, all drawn first, each answered 100
# times.


def slowest_key(release_times, keys_pressed):
    previous = 0
    best = (0, "a")
    for time, key in zip(release_times, keys_pressed):
        best = max(best, (time - previous, key))
        previous = time
    return best[1]


seed = 1629


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


problems = []
for _ in range(1000):
    release_times = []
    keys = []
    time = 0
    for _ in range(1000):
        time += next_random() % 1000 + 1
        release_times.append(time)
        keys.append(chr(ord("a") + next_random() % 26))
    problems.append((release_times, "".join(keys)))
check = 0
for _ in range(100):
    for release_times, keys_pressed in problems:
        key = slowest_key(release_times, keys_pressed)
        check = (check * 31 + ord(key)) % 1000000007
print(f"1000 problems of 1000 presses, answered 100 times: checksum {check}")
