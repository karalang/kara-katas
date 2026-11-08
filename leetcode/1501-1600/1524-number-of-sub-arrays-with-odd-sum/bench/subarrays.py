# LeetCode #1524: Number of Sub-arrays With Odd Sum -- bench: the ★ arm
# over 100 random arrays of 1 to 100000 numbers from 1 to 100, built once
# and answered 20 times.


def num_of_subarrays(arr):
    modulus = 1000000007
    odd, even, total, answer = 0, 1, 0, 0
    for x in arr:
        total += x
        if total % 2 == 1:
            answer = (answer + even) % modulus
            odd += 1
        else:
            answer = (answer + odd) % modulus
            even += 1
    return answer


seed = 1524


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def main():
    arrays = []
    for _ in range(100):
        n = (next_random() * 32768 + next_random()) % 100000 + 1
        arrays.append([next_random() % 100 + 1 for _ in range(n)])
    check = 0
    for _ in range(20):
        for arr in arrays:
            check = mix(check, num_of_subarrays(arr))
    print(f"20 passes over 100 arrays of up to 100000 numbers: checksum {check}")


main()
