// LeetCode #1198 bench: the ★ arm in C, over the same 20 matrices of
// 500 x 500 and 100 rounds as the Kāra bench; a matrix is 500 rows of 500
// values in one array.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define M 500
#define N 500

static int64_t smallest_common_element(const int64_t *mat) {
    static int64_t count[10001];
    memset(count, 0, sizeof count);
    for (int r = 0; r < M; r++) {
        for (int c = 0; c < N; c++) {
            count[mat[r * N + c]] += 1;
        }
    }
    for (int c = 0; c < N; c++) {
        if (count[mat[c]] == M) {
            return mat[c];
        }
    }
    return -1;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static void random_row(int64_t *seed, int64_t *row, int64_t n, int64_t high) {
    int64_t v = 0;
    for (int64_t len = 0; len < n; len++) {
        v += 1 + next_random(seed) % (2 * high / n);
        if (v > high - (n - len) + 1) {
            v = high - (n - len) + 1;
        }
        row[len] = v;
    }
}

int main(void) {
    int64_t highs[4] = {520, 1000, 5000, 10000};
    int64_t seed = 1198;
    int64_t *mats = malloc(20 * M * N * sizeof(int64_t));
    for (int k = 0; k < 20; k++) {
        for (int r = 0; r < M; r++) {
            random_row(&seed, mats + (k * M + r) * N, N, highs[k % 4]);
        }
    }
    int64_t check = 0;
    for (int round = 0; round < 100; round++) {
        for (int k = 0; k < 20; k++) {
            int64_t v = smallest_common_element(mats + k * M * N);
            check = (check * 131 + v + 2) % 1000000007;
        }
    }
    printf("100 rounds of 20 matrices of 500 x 500: checksum %lld\n", (long long)check);
    free(mats);
    return 0;
}
