# LeetCode #905: Sort Array By Parity -- Python mirror of the two pointers
# from both ends in sort_array_by_parity.kara, with the same test harness.


def sort_array_by_parity(nums):
    out = nums
    i = 0
    j = len(out) - 1
    while i < j:
        if out[i] % 2 == 0:
            i += 1
        elif out[j] % 2 == 1:
            j -= 1
        else:
            out[i], out[j] = out[j], out[i]
            i += 1
            j -= 1
    return out


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def fits(nums, out):
    if len(out) != len(nums):
        return False
    k = 0
    while k < len(out) and out[k] % 2 == 0:
        k += 1
    while k < len(out) and out[k] % 2 == 1:
        k += 1
    if k != len(out):
        return False
    return sorted(nums) == sorted(out)


def listed(xs):
    return ",".join(str(x) for x in xs)


def show(nums):
    out = sort_array_by_parity(list(nums))
    evens = sorted(x for x in out if x % 2 == 0)
    odds = sorted(x for x in out if x % 2 == 1)
    verdict = "fits" if fits(nums, out) else "DOES NOT FIT"
    print(f"nums = [{listed(nums)}] -> evens [{listed(evens)}] then odds [{listed(odds)}], {verdict}")


def random_nums(length, even):
    out = []
    for _ in range(length):
        half = next_random() % 2501
        x = 2 * half if next_random() % 100 < even else min(2 * half + 1, 4999)
        out.append(x)
    return out


def summary(out):
    lead = 0
    while lead < len(out) and out[lead] % 2 == 0:
        lead += 1
    check = lead
    for k in range(len(out)):
        side = 1 if k < lead else 2
        check = (check + side * (out[k] + 1) * (out[k] + 7)) % 1000000007
    return lead, check


def b(x):
    return "true" if x else "false"


def main():
    global seed
    show([3, 1, 2, 4])
    show([0])
    show([1])
    show([2, 4, 6])
    show([1, 3, 5])
    show([1, 2])
    show([2, 1])
    show([1, 2, 3, 4, 5, 6, 7, 8])
    show([5000, 4999, 0, 1, 2, 3, 3, 2])
    seed = 905
    fit = 0
    lead = 0
    check = 0
    for c in range(300):
        length = 1 + next_random() % 5000
        nums = random_nums(length, (c * 37) % 101)
        out = sort_array_by_parity(list(nums))
        if fits(nums, out):
            fit += 1
        l, s = summary(out)
        lead += l
        check = (check * 1000003 + s) % 1000000007
    print(f"300 cases: {fit} fit, {lead} evens first in all, checksum {check}")
    big = random_nums(5000, 50)
    out = sort_array_by_parity(list(big))
    l, s = summary(out)
    print(f"5000 numbers: fits {b(fits(big, out))}, evens first {l}, checksum {s}")
    odd = [2 * k % 5000 + 1 for k in range(4999)] + [5000]
    out2 = sort_array_by_parity(list(odd))
    l2, s2 = summary(out2)
    print(f"4999 odd numbers then 5000: fits {b(fits(odd, out2))}, evens first {l2}, checksum {s2}")


main()
