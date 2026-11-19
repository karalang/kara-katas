# LeetCode #1629: Slowest Key -- the Python mirror of the ★ arm: the
# largest (duration, key) pair over the times zipped with the keys.


def slowest_key(release_times, keys_pressed):
    previous = 0
    best = (0, "a")
    for time, key in zip(release_times, keys_pressed):
        best = max(best, (time - previous, key))
        previous = time
    return best[1]


# ---- the harness: the same as every arm's ---------------------------------

seed = 1629


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def batch(count, most, letters, longest):
    check = 0
    answers = ""
    for _ in range(count):
        n = next_random() % (most - 1) + 2
        release_times = []
        keys_pressed = ""
        time = 0
        for _ in range(n):
            time += next_random() % longest + 1
            release_times.append(time)
            keys_pressed += chr(ord("a") + next_random() % letters)
        key = slowest_key(release_times, keys_pressed)
        if len(answers) < 40:
            answers += key
        check = (check * 31 + ord(key)) % 1000000007
    print(f"{count} problems of up to {most} presses: {answers}..., checksum {check}")


print(slowest_key([9, 29, 49, 50], "cbcd"))
print(slowest_key([12, 23, 36, 46, 62], "spuda"))
print(slowest_key([5, 10], "ab"))
print(slowest_key([4, 8, 9], "zab"))
batch(3000, 6, 3, 4)
batch(300, 1000, 26, 100)
batch(10, 1000, 26, 30000)
