# LeetCode #1550: Three Consecutive Odds -- bench: the ★ arm (the run of
# odd values) over 1000 arrays of 1 to 1000 values, each with its own
# chance of an odd value, built once, each asked 2000 times with one value
# raised by one before every ask, so no ask repeats the last. Python mirror
# of three_odds.kara.


def three_consecutive_odds(arr):
    run = 0
    for x in arr:
        if x % 2 == 1:
            run += 1
            if run == 3:
                return True
        else:
            run = 0
    return False


seed = 1550


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    arrays = []
    for _ in range(1000):
        length = (next_random() * 32768 + next_random()) % 1000 + 1
        odds = next_random() % 101
        arr = []
        for _ in range(length):
            odd = next_random() % 100 < odds
            half = next_random() % 500
            arr.append(2 * half + 1 if odd else 2 * half + 2)
        arrays.append(arr)
    yes = 0
    check = 0
    for p in range(2000):
        for g, arr in enumerate(arrays):
            arr[(p * 7 + g) % len(arr)] += 1
            if three_consecutive_odds(arr):
                yes += 1
                check = (check * 31 + p + g + 1) % 1000000007
    print(f"2000 passes over 1000 arrays of up to 1000 values: {yes} true, checksum {check}")


main()
