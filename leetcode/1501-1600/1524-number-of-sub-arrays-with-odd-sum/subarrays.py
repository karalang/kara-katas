# LeetCode #1524: Number of Sub-arrays With Odd Sum -- mirrors
# subarrays.kara, the ★ arm: each prefix pairs with every earlier prefix
# of the other parity.


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


def batch(count, most):
    check = 0
    for _ in range(count):
        n = (next_random() * 32768 + next_random()) % most + 1
        arr = [next_random() % 100 + 1 for _ in range(n)]
        check = mix(check, num_of_subarrays(arr))
    print(f"{count} arrays of 1 to {most} numbers: checksum {check}")


print(f"example 1, [1,3,5] -> {num_of_subarrays([1, 3, 5])}")
print(f"example 2, [2,4,6] -> {num_of_subarrays([2, 4, 6])}")
print(f"example 3, [1,2,3,4,5,6,7] -> {num_of_subarrays([1, 2, 3, 4, 5, 6, 7])}")
print(f"100000 ones -> {num_of_subarrays([1] * 100000)}")
batch(3000, 12)
batch(30, 100000)
