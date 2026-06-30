"""LeetCode #48 bench mirror — Python, the in-place layer four-way cyclic rotation (★).

Mirrors bench/rotate_image.kara exactly: rotate a fixed n=20 matrix 90° clockwise IN PLACE by
cycling four cells at a time, TOTAL times, with the state carrying forward; one cell punched per
iteration (`m[k%n][(k*7)%n] = k%97`), folding a position-weighted per-cell signature into a rolling
checksum. Prints the same sink as every other mirror.
"""


def rotate(m: list[list[int]]) -> None:
    n = len(m)
    for i in range(n // 2):
        for j in range(i, n - 1 - i):
            (m[i][j], m[j][n - 1 - i], m[n - 1 - i][n - 1 - j], m[n - 1 - j][i]) = (
                m[n - 1 - j][i], m[i][j], m[j][n - 1 - i], m[n - 1 - i][n - 1 - j])


def main() -> None:
    total = 40000
    modulus = 1000000007
    n = 20

    m = [[(a * 7 + b * 13) % 97 for b in range(n)] for a in range(n)]

    acc = 0
    for k in range(total):
        m[k % n][(k * 7) % n] = k % 97
        rotate(m)

        sig = 0
        for i in range(n):
            row = m[i]
            for j in range(n):
                sig = (sig * 31 + row[j] * (i * n + j + 1)) % modulus
        acc = (acc * 131 + sig) % modulus

    print(acc)


if __name__ == "__main__":
    main()
