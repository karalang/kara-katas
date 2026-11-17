# LeetCode #2231: Largest Number After Digit Swaps by Parity -- the
# benchmark's Python mirror of parity.kara: each parity's digits sorted
# from largest down into that parity's places.


def largest_integer(num):
    digits = [ord(c) - 48 for c in str(num)]
    odd = []
    even = []
    for d in digits:
        if d % 2 == 1:
            odd.append(d)
        else:
            even.append(d)
    odd.sort()
    even.sort()
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
    nums = [wide_random() % 1000000000 + 1 for _ in range(100000)]
    check = 0
    for _ in range(20):
        # punch: one num drawn again before each pass over all of them
        at = wide_random() % 100000
        nums[at] = wide_random() % 1000000000 + 1
        for num in nums:
            check = (check * 31 + largest_integer(num)) % 1000000007
    print(f"20 passes over 10^5 nums: checksum {check}")


main()
