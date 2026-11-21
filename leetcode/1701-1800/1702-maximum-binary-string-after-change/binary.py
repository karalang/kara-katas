# LeetCode #1702: Maximum Binary String After Change -- the Python mirror
# of the ★ arm (binary.kara): one 0 is left, at the first 0 plus the
# count of zeros, less one.


def maximum_binary_string(binary):
    first = binary.find("0")
    if first < 0:
        return binary
    zeros = binary.count("0")
    n = len(binary)
    return "1" * (first + zeros - 1) + "0" + "1" * (n - first - zeros)


def next_random(state):
    state[0] = (state[0] * 1103515245 + 12345) % 2147483648
    return state[0] // 65536


def batch(count, most, seed):
    zeros = 0
    check = 0
    for _ in range(count):
        n = (next_random(seed) * 32768 + next_random(seed)) % most + 1
        lean = next_random(seed) % 11
        binary = "".join("1" if next_random(seed) % 10 < lean else "0" for _ in range(n))
        answer = maximum_binary_string(binary)
        for b in answer.encode():
            if b == ord("0"):
                zeros += 1
            check = (check * 31 + b) % 1000000007
    print(f"{count} strings of up to {most} digits: {zeros} zeros left, checksum {check}")


def main():
    # LeetCode's two examples, then a lone 1, four zeros, and no zero
    for s in ["000110", "01", "1", "0000", "1111"]:
        print(maximum_binary_string(s))
    seed = [1702]
    batch(3000, 12, seed)
    batch(300, 1000, seed)
    batch(10, 100000, seed)


main()
