// LeetCode #1536: Minimum Swaps to Arrange a Binary Grid -- bench: the ★
// arm over 50 random 200 x 200 grids, built once and answered 50 times.
// C mirror of swaps.kara.

#include <stdint.h>
#include <stdio.h>

#define N 200

static int64_t grids[50][N][N];

static int64_t min_swaps(int64_t g[N][N], int n) {
    int64_t zeros[N];
    for (int r = 0; r < n; r++) {
        int count = 0;
        while (count < n && g[r][n - 1 - count] == 0) {
            count += 1;
        }
        zeros[r] = count;
    }
    int64_t swaps = 0;
    for (int i = 0; i < n; i++) {
        int64_t need = n - 1 - i;
        int j = i;
        while (j < n && zeros[j] < need) {
            j += 1;
        }
        if (j == n) {
            return -1;
        }
        while (j > i) {
            int64_t t = zeros[j];
            zeros[j] = zeros[j - 1];
            zeros[j - 1] = t;
            j -= 1;
            swaps += 1;
        }
    }
    return swaps;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

static void grid(int64_t g[N][N], int64_t n, int64_t *seed) {
    int64_t zeros[N];
    for (int64_t i = 0; i < n; i++) {
        zeros[i] = i;
    }
    if (next_random(seed) % 2 == 0) {
        for (int64_t i = n - 1; i >= 1; i--) {
            int64_t j = next_random(seed) % (i + 1);
            int64_t t = zeros[i];
            zeros[i] = zeros[j];
            zeros[j] = t;
        }
        for (int64_t i = 0; i < n; i++) {
            int64_t z = zeros[i] + next_random(seed) % 2;
            zeros[i] = z < n ? z : n;
        }
    } else {
        for (int64_t i = 0; i < n; i++) {
            zeros[i] = next_random(seed) % (n + 1);
        }
    }
    for (int64_t i = 0; i < n; i++) {
        for (int64_t c = 0; c < n; c++) {
            g[i][c] = 0;
        }
        if (zeros[i] < n) {
            g[i][n - 1 - zeros[i]] = 1;
            for (int64_t c = 0; c < n - 1 - zeros[i]; c++) {
                g[i][c] = next_random(seed) % 2;
            }
        }
    }
}

int main(void) {
    int64_t seed = 1536;
    for (int p = 0; p < 50; p++) {
        grid(grids[p], N, &seed);
    }
    int64_t check = 0;
    for (int pass = 0; pass < 50; pass++) {
        for (int p = 0; p < 50; p++) {
            check = mix(check, min_swaps(grids[p], N) + 1);
        }
    }
    printf("50 passes over 50 grids of 200 rows: checksum %lld\n", (long long)check);
    return 0;
}
