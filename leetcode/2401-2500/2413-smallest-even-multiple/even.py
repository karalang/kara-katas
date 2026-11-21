# LeetCode #2413: Smallest Even Multiple -- the mirror of the ★ arm: n when
# n is even, and 2 n when it is odd.


def smallest_even_multiple(n):
    return n if n % 2 == 0 else 2 * n


def main():
    print(f"{smallest_even_multiple(5)} {smallest_even_multiple(6)}")
    print(f"{smallest_even_multiple(1)} {smallest_even_multiple(2)} {smallest_even_multiple(149)} {smallest_even_multiple(150)}")
    print(" ".join(str(smallest_even_multiple(n)) for n in range(1, 21)))
    check = 0
    total = 0
    for n in range(1, 151):
        a = smallest_even_multiple(n)
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"1 to 150: checksum {check}, total {total}")


if __name__ == "__main__":
    main()
