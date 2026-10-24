// Benchmark: LeetCode #944 Delete Columns to Make Sorted -- the ★ arm,
// column by column, on grids of 100 rows of 1000 letters, LeetCode's
// largest. Mirrors min_deletion_size.kara, .rs, .py and go-seq/.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 100
#define M 1000
#define COUNT 20

static int64_t min_deletion_size(char strs[N][M + 1], int64_t n, int64_t m) {
    int64_t deleted = 0;
    for (int64_t c = 0; c < m; c++) {
        int64_t r = 1;
        while (r < n && strs[r - 1][c] <= strs[r][c]) {
            r++;
        }
        if (r < n) {
            deleted++;
        }
    }
    return deleted;
}

static int64_t seed = 944;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int cmp_char(const void *a, const void *b) {
    return *(const char *)a - *(const char *)b;
}

static char grids[COUNT][N][M + 1];

int main(void) {
    const int64_t rounds = 150, count = COUNT, n = N, m = M;
    static char columns[M][N];
    for (int64_t g = 0; g < count; g++) {
        for (int64_t c = 0; c < m; c++) {
            for (int64_t r = 0; r < n; r++) {
                columns[c][r] = (char)(next_random() % 26 + 97);
            }
            qsort(columns[c], (size_t)n, 1, cmp_char);
            if (next_random() % 2 == 0) {
                int64_t a = next_random() % n;
                int64_t b = next_random() % n;
                char t = columns[c][a];
                columns[c][a] = columns[c][b];
                columns[c][b] = t;
            }
        }
        for (int64_t r = 0; r < n; r++) {
            for (int64_t c = 0; c < m; c++) {
                grids[g][r][c] = columns[c][r];
            }
            grids[g][r][m] = 0;
        }
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t i = 0; i < count; i++) {
            int64_t d = min_deletion_size(grids[(r + i) % count], n, m);
            total += d;
            check = (check * 1000003 + d * (i + 1)) % 1000000007;
        }
    }
    printf("%lld rounds over %lld grids of %lld rows of %lld letters: %lld deleted, checksum %lld\n",
           (long long)rounds, (long long)count, (long long)n, (long long)m, (long long)total,
           (long long)check);
    return 0;
}
