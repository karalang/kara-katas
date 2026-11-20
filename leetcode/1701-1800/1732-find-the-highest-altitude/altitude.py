# LeetCode #1732: Find the Highest Altitude -- the Python mirror of the ★
# arm, altitude.kara: every altitude listed, the start's 0 included, and
# the largest taken.


def largest_altitude(gain):
    altitudes = [0]
    for g in gain:
        altitudes.append(altitudes[-1] + g)
    return max(altitudes)


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def batch(count, most, top, seed):
    total = 0
    check = 0
    for _ in range(count):
        n = next_random(seed) % most + 1
        gain = [next_random(seed) % (2 * top + 1) - top for _ in range(n)]
        answer = largest_altitude(gain)
        total += answer
        check = (check * 31 + answer + n) % 1000000007
    print(f"{count} trips of up to {most} gains up to {top}: highest points sum to {total}, checksum {check}")


def main():
    print(largest_altitude([-5, 1, 5, 0, -7]))
    print(largest_altitude([-4, -3, -2, -1, 4, 3, 2]))
    print(largest_altitude([-100]))
    print(largest_altitude([100] * 100))
    seed = [1732]
    batch(3000, 8, 3, seed)
    batch(3000, 100, 100, seed)


main()
