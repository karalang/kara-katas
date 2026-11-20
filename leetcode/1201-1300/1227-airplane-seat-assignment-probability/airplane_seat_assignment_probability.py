# LeetCode #1227: Airplane Seat Assignment Probability -- Python mirror of
# the ★ arm, the closed form: 1 for one passenger, 1/2 for more.


def nth_person_gets_nth_seat(n):
    return 1.0 if n == 1 else 0.5


# ---- test harness ---------------------------------------------------------

def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    for n in [1, 2, 3, 4, 100000]:
        print(f"n={n}: {nth_person_gets_nth_seat(n):.5f}")
    seed = [1227]
    total = 0.0
    for _ in range(300):
        n = next_random(seed) % 3000 + 1
        total += nth_person_gets_nth_seat(n)
    print(f"300 random n from 1 to 3000: total {total:.5f}")


main()
