# LeetCode #1015: Smallest Integer Divisible by K -- remainder walk (mirror of repunit.kara)


def smallest_repunit_div_by_k(k):
    if k % 2 == 0 or k % 5 == 0:
        return -1
    r = 0
    for length in range(1, k + 1):
        r = (r * 10 + 1) % k
        if r == 0:
            return length
    return -1


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    examples = [1, 2, 3, 5, 7, 9, 11, 13, 17, 19, 27, 41, 81, 99, 101, 9091, 99989, 99991, 99999, 100000]
    for k in examples:
        print(f"k = {k} -> {smallest_repunit_div_by_k(k)}")
    none = 0
    total = 0
    check = 0
    longest = 0
    longest_k = 0
    for k in range(1, 10001):
        answer = smallest_repunit_div_by_k(k)
        if answer < 0:
            none += 1
        else:
            total += answer
            if answer > longest:
                longest = answer
                longest_k = k
        check = (check * 31 + answer + 1) % 1000000007
    print(f"k = 1..10000: {none} with no answer, the rest sum to {total}, longest {longest} at k = {longest_k}, checksum {check}")
    seed = [1015]
    none = 0
    total = 0
    check = 0
    for _ in range(1000):
        k = 1 + (next_random(seed) * 32768 + next_random(seed)) % 100000
        answer = smallest_repunit_div_by_k(k)
        if answer < 0:
            none += 1
        else:
            total += answer
        check = (check * 31 + answer + 1) % 1000000007
    print(f"1000 random k up to 100000: {none} with no answer, the rest sum to {total}, checksum {check}")


main()
