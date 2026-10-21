# Benchmark for #835: Image Overlap -- the ★ arm (shifts counted over pairs of ones).
#
# Mirrors largest_overlap.kara: every pair of a one in the first image and
# a one in the second votes for the shift that lays the first on the
# second, and the shift with the most votes is the answer.


def largest_overlap(img1, img2):
    n = len(img1)
    ones1 = []
    ones2 = []
    for r in range(n):
        for c in range(n):
            if img1[r][c] == 1:
                ones1.append((r, c))
            if img2[r][c] == 1:
                ones2.append((r, c))
    width = 2 * n - 1
    votes = [0] * (width * width)
    best = 0
    for r1, c1 in ones1:
        for r2, c2 in ones2:
            k = (r2 - r1 + n - 1) * width + (c2 - c1 + n - 1)
            votes[k] += 1
            if votes[k] > best:
                best = votes[k]
    return best


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    # 64 pairs of images drawn once, each of LeetCode's largest size, 30
    # by 30, the share of ones running from 2% to 98% over the pairs, the
    # two images of pair k at 2k and 2k + 1 in one list. Each round solves
    # the next pair.
    count = 64
    rounds = 4000
    n = 30
    seed = [835]
    images = []
    for g in range(count):
        percent = 2 + g * 96 // (count - 1)
        for _ in range(2):
            img = []
            for _ in range(n):
                row = []
                for _ in range(n):
                    row.append(1 if next_random(seed) % 100 < percent else 0)
                img.append(row)
            images.append(img)
    total = 0
    checksum = 0
    for round_ in range(rounds):
        k = round_ % count
        x = largest_overlap(images[2 * k], images[2 * k + 1])
        total += x
        checksum = (checksum * 131 + x) % 1000000007
    print(f"{rounds} rounds of {count} pairs: overlaps total {total}, checksum {checksum}")


main()
