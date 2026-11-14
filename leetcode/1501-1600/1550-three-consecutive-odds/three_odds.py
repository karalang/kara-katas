# LeetCode #1550: Three Consecutive Odds -- the Python mirror of
# three_odds.kara, the ★ arm: one pass keeping the length of the run of odd
# values. Prints byte-identical output.


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


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def show(answer):
    return "true" if answer else "false"


def batch(count, longest):
    check = 0
    yes = 0
    for _ in range(count):
        length = next_random() % longest + 1
        odds = next_random() % 101
        arr = []
        for _ in range(length):
            odd = next_random() % 100 < odds
            half = next_random() % 500
            arr.append(2 * half + 1 if odd else 2 * half + 2)
        answer = three_consecutive_odds(arr)
        if answer:
            yes += 1
        check = mix(check, 1 if answer else 0)
    print(f"{count} arrays of up to {longest} values: {yes} true, checksum {check}")


def main():
    global seed
    examples = [
        [2, 6, 4, 1],
        [1, 2, 34, 3, 4, 5, 7, 23, 12],
        [1, 3, 5],
        [1, 3],
        [1],
        [2, 1, 1, 2, 1, 1, 1],
        [1, 1, 2, 1, 1, 2, 1, 1],
        [999, 1000, 999, 999, 999],
    ]
    for arr in examples:
        print(f"[{', '.join(map(str, arr))}] -> {show(three_consecutive_odds(arr))}")
    print(f"1 to 1000 -> {show(three_consecutive_odds(list(range(1, 1001))))}")
    seed = 1550
    batch(3000, 12)
    batch(300, 100)
    batch(300, 1000)


main()
