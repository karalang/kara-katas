# Benchmark for #482: Python mirror of the ★ arm (back to front); see
# license_key_formatting.kara.


def license_key_formatting(s, k):
    backwards = []
    in_group = 0
    for c in reversed(s):
        if c == "-":
            continue
        if in_group == k:
            backwards.append("-")
            in_group = 0
        backwards.append(c.upper())
        in_group += 1
    backwards.reverse()
    return "".join(backwards)


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    alphabet = "abcxyzABCXYZ0189"
    seed = [482]
    chars = []
    for _ in range(100000):
        if next_random(seed) % 4 == 0:
            chars.append("-")
        else:
            chars.append(alphabet[next_random(seed) % len(alphabet)])
    s = "".join(chars)
    total = 0
    checksum = 0
    for k in range(1, 501):
        key = license_key_formatting(s, k)
        total += len(key)
        checksum = (checksum * 31 + len(key) * 7 + ord(key[len(key) // 2]) + ord(key[k])) % 1000000007
    print(f"k = 1 to 500 on 100000 characters: keys add up to {total} characters, checksum {checksum}")


main()
