"""LeetCode 229 — Majority Element II (Python mirror / oracle).

Two-candidate Boyer-Moore vote (at most two elements exceed n/3), then a
verification counting pass. Result sorted ascending. Mirrors the Kara version.
"""


def majority_elements(nums):
    n = len(nums)
    result = []
    if n == 0:
        return result

    cand1 = cand2 = 0
    count1 = count2 = 0
    for x in nums:
        if count1 > 0 and x == cand1:
            count1 += 1
        elif count2 > 0 and x == cand2:
            count2 += 1
        elif count1 == 0:
            cand1 = x
            count1 = 1
        elif count2 == 0:
            cand2 = x
            count2 = 1
        else:
            count1 -= 1
            count2 -= 1

    real1 = real2 = 0
    for x in nums:
        if count1 > 0 and x == cand1:
            real1 += 1
        elif count2 > 0 and x == cand2:
            real2 += 1

    threshold = n // 3
    if count1 > 0 and real1 > threshold:
        result.append(cand1)
    if count2 > 0 and real2 > threshold:
        result.append(cand2)
    if len(result) == 2 and result[0] > result[1]:
        result[0], result[1] = result[1], result[0]
    return result


def report(nums):
    res = majority_elements(nums)
    print(" ".join(str(x) for x in res) if res else "(none)")


def main():
    report([3, 2, 3])
    report([1])
    report([1, 2])
    report([1, 1, 1, 3, 3, 2, 2, 2])
    report([2, 2, 1, 3])
    report([1, 2, 3, 4])
    report([5, 5, 5, 5])
    report([-1, -1, -1, 2, 2, 2, 3, 3, 3])


main()
