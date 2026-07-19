"""LeetCode #137: Single Number II — every element appears 3x except one.

Two canonical approaches, both mirrored:
  A) ones/twos bitmask FSM: ones^=x & ~twos; twos^=x & ~ones (32-bit).
  B) per-bit count mod 3 reconstruction.
"""

MASK32 = 0xFFFFFFFF


def single_ones_twos(nums):
    ones = 0
    twos = 0
    for x in nums:
        x &= MASK32
        ones = (ones ^ x) & ~twos & MASK32
        twos = (twos ^ x) & ~ones & MASK32
    # sign-extend from 32-bit
    if ones >= 0x80000000:
        ones -= 0x100000000
    return ones


def single_bitcount(nums):
    res = 0
    for b in range(32):
        cnt = 0
        for x in nums:
            if (x >> b) & 1:
                cnt += 1
        if cnt % 3:
            res |= (1 << b)
    if res >= 0x80000000:
        res -= 0x100000000
    return res


def main():
    MOD = 1000000007
    cases = [
        [2, 2, 3, 2],
        [0, 1, 0, 1, 0, 1, 99],
        [-2, -2, 1, 1, -3, 1, -3, -3, -2, 30],
        [5],
        [7, 7, 7, 13],
    ]
    sink_a = 0
    sink_b = 0
    for nums in cases:
        a = single_ones_twos(nums)
        b = single_bitcount(nums)
        assert a == b, (nums, a, b)
        print(f"n={len(nums)}: {a}")
        sink_a = (sink_a * 1000003 + (a + 1000)) % MOD
        sink_b = (sink_b * 1000003 + (b + 1000)) % MOD
    assert sink_a == sink_b
    print(f"sink: {sink_a}")


if __name__ == "__main__":
    main()
