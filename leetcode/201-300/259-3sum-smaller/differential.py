"""LeetCode 259 - differential harness. Python oracle.

Mirrors differential.kara exactly: same LCG, same in-band target draw, the same
three counters and the same digest.
"""


def count_two_pointer(nums, target):
    s = sorted(nums)
    n = len(s)
    count = 0
    for i in range(max(0, n - 2)):
        lo, hi = i + 1, n - 1
        while lo < hi:
            if s[i] + s[lo] + s[hi] < target:
                count += hi - lo
                lo += 1
            else:
                hi -= 1
    return count


def count_brute(nums, target):
    n = len(nums)
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if nums[i] + nums[j] + nums[k] < target:
                    count += 1
    return count


def count_bsearch(nums, target):
    s = sorted(nums)
    n = len(s)
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            need = target - s[i] - s[j]
            lo, hi = j + 1, n
            while lo < hi:
                mid = lo + (hi - lo) // 2
                if s[mid] < need:
                    lo = mid + 1
                else:
                    hi = mid
            count += lo - j - 1
    return count


def main():
    cases = 4000
    seed = 259259
    mismatches = total_triples = saturated_lo = saturated_hi = digest = 0

    for _ in range(cases):
        seed = (seed * 1103515245 + 12345) & 2147483647
        n = (seed // 65536) % 13

        nums = []
        for _ in range(n):
            seed = (seed * 1103515245 + 12345) & 2147483647
            nums.append((seed // 65536) % 21 - 10)

        target = 1
        if n >= 3:
            srt = sorted(nums)
            min_sum = srt[0] + srt[1] + srt[2]
            max_sum = srt[n - 1] + srt[n - 2] + srt[n - 3]
            seed = (seed * 1103515245 + 12345) & 2147483647
            span = max_sum - min_sum + 2
            target = min_sum + (seed // 65536) % span

        a = count_two_pointer(nums, target)
        b = count_brute(nums, target)
        d = count_bsearch(nums, target)

        if a != b or a != d:
            mismatches += 1
        total_triples += b
        if b == 0:
            saturated_lo += 1
        if n >= 3 and b == n * (n - 1) * (n - 2) // 6:
            saturated_hi += 1
        digest = (digest * 131 + b) % 1000000007

    print(f"cases {cases}")
    print(f"triples counted {total_triples}")
    print(f"answer==0 {saturated_lo}")
    print(f"answer==C(n,3) {saturated_hi}")
    print(f"digest {digest}")
    print(f"mismatches {mismatches}")


if __name__ == "__main__":
    main()
