# LeetCode #2231: Largest Number After Digit Swaps by Parity -- the mirror
# of parity.kara: each parity's digits sorted from largest down into that
# parity's places.


def largest_integer(num):
    digits = [ord(c) - 48 for c in str(num)]
    odd = sorted(d for d in digits if d % 2 == 1)
    even = sorted(d for d in digits if d % 2 == 0)
    largest = 0
    for d in digits:
        nxt = odd.pop() if d % 2 == 1 else even.pop()
        largest = largest * 10 + nxt
    return largest


seed = 2231


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    high = next_random()
    return high * 32768 + next_random()


def main():
    for num in [1234, 65875, 1, 1000000000, 247, 10, 86420, 123456789]:
        print(f"{num} -> {largest_integer(num)}")
    check = 0
    for c in range(3000):
        num = wide_random() % [10000, 10000000, 1000000000][c % 3] + 1
        check = (check * 31 + largest_integer(num)) % 1000000007
    print(f"3000 nums: checksum {check}")
    total = 0
    for num in range(1, 100001):
        total += largest_integer(num) - num
    print(f"1 to 10^5: the swaps add {total} in all")


main()
