# Benchmark mirror — LeetCode 309, Best Time to Buy and Sell Stock with Cooldown.
# Same three-state DP, same LCG series, same per-pass perturbation and masked
# sink as cooldown.kara. See ../README.md § Benchmarks.
#
# The sink masks rather than taking a modulus: Python's `%` FLOORS while
# C/Rust/Go/kara truncate toward zero, so a modulo sink over a signed running
# total prints a different number here than in every other mirror (measured on
# #303). Masking is two's-complement in all five languages.


def main():
    n = 200000
    passes = 1900

    prices = [0] * n
    state = 20309
    for i in range(n):
        state = (state * 1103515245 + 12345) % 2147483648
        prices[i] = state % 2001 - 1000

    checksum = 0
    for p in range(passes):
        slot = p % n
        prices[slot] = prices[slot] + (checksum & 1)

        hold = -prices[0]
        sold = 0
        rest = 0
        for i in range(1, n):
            prev_hold, prev_sold, prev_rest = hold, sold, rest
            hold = prev_hold
            if prev_rest - prices[i] > hold:
                hold = prev_rest - prices[i]
            sold = prev_hold + prices[i]
            rest = prev_rest
            if prev_sold > rest:
                rest = prev_sold
        best = rest
        if sold > best:
            best = sold
        checksum = (checksum + best) & 0x3FFFFFFF
    print(f"checksum {checksum}")


main()
