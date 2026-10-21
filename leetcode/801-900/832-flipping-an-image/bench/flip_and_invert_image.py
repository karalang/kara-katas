# Benchmark for #832: Flipping an Image -- the ★ arm (two pointers in place).
#
# Mirrors flip_and_invert_image.kara: each row is flipped and inverted in
# one walk from both ends, the middle cell of an odd row only inverted.
# The image is changed in place.


def flip_and_invert_image(image):
    img = image
    n = len(img)
    for r in range(n):
        row = img[r]
        i = 0
        j = n - 1
        while i < j:
            left = row[i]
            row[i] = 1 - row[j]
            row[j] = 1 - left
            i += 1
            j -= 1
        if i == j:
            row[i] = 1 - row[i]
    return img


def main():
    count, rounds = 64, 4000000
    seed = 832

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    images = []
    for g in range(count):
        n = 17 + g % 4
        images.append([[next_random() % 2 for _ in range(n)] for _ in range(n)])
    total = 0
    checksum = 0
    for rnd in range(rounds):
        k = rnd % count
        images[k] = flip_and_invert_image(images[k])
        for x in images[k][rnd // count % len(images[k])]:
            total += x
            checksum = (checksum * 3 + x) % 1000000007
    print(f"{rounds} rounds of {count} images: {total} ones, checksum {checksum}")


main()
