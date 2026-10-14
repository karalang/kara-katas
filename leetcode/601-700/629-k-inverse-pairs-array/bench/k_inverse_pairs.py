# LeetCode #629: K Inverse Pairs Array -- Python mirror of the Kāra
# bench.
#
# The ★ arm's rolling DP with a window sum over the same inputs.


def k_inverse_pairs(n, k):
    modulus = 1000000007
    row = [0] * (k + 1)
    row[0] = 1
    for i in range(2, n + 1):
        nxt = [0] * (k + 1)
        window = 0
        for j in range(k + 1):
            window = (window + row[j]) % modulus
            if j >= i:
                window = (window - row[j - i] + modulus) % modulus
            nxt[j] = window
        row = nxt
    return row[k]


def main():
    rounds = 100
    checksum = 0
    for r in range(rounds):
        n = 500 + (r * 37) % 501
        k = 500 + (r * 91) % 501
        c = k_inverse_pairs(n, k)
        checksum = (checksum * 31 + c) % 1000000007
    print(f"{rounds} rounds: checksum {checksum}")


main()
