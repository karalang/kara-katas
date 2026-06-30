// LeetCode #48 bench mirror — C, the in-place layer four-way cyclic rotation (★).
//
// Mirrors bench/rotate_image.kara: rotate a fixed n=20 matrix 90° clockwise IN PLACE by cycling
// four cells at a time (one temporary, like the Rust mirror — the four-target parallel assignment
// is Kāra-only), TOTAL times with the state carrying forward; one cell punched per iteration
// (`m[k%n][(k*7)%n] = k%97`), folding a position-weighted per-cell signature into a rolling
// checksum. A fixed `int64_t[20][20]` stands in for Vec[Vec[i64]] — the rotation never allocates.
// Same workload + checksum as every other mirror.

#include <stdio.h>
#include <stdint.h>

#define N 20

static void rotate(int64_t m[N][N]) {
    for (int i = 0; i < N / 2; i++) {
        for (int j = i; j < N - 1 - i; j++) {
            int64_t tmp = m[i][j];
            m[i][j] = m[N - 1 - j][i];
            m[N - 1 - j][i] = m[N - 1 - i][N - 1 - j];
            m[N - 1 - i][N - 1 - j] = m[j][N - 1 - i];
            m[j][N - 1 - i] = tmp;
        }
    }
}

int main(void) {
    const int64_t total = 40000;
    const int64_t modulus = 1000000007;

    int64_t m[N][N];
    for (int a = 0; a < N; a++)
        for (int b = 0; b < N; b++)
            m[a][b] = (a * 7 + b * 13) % 97;

    int64_t acc = 0;
    for (int64_t k = 0; k < total; k++) {
        m[k % N][(k * 7) % N] = k % 97;
        rotate(m);

        int64_t sig = 0;
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                sig = (sig * 31 + m[i][j] * ((int64_t)i * N + j + 1)) % modulus;
            }
        }
        acc = (acc * 131 + sig) % modulus;
    }

    printf("%lld\n", (long long)acc);
    return 0;
}
