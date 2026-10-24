// Benchmark: LeetCode #960 Delete Columns to Make Sorted III -- the ★
// arm, longest chain, on 100 strings of 100 letters, LeetCode's largest.
// Mirrors min_deletion_size.kara, .rs, .py and go-seq/. The chain lengths
// are an array on the stack, so a call allocates nothing.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 100
#define M 100
#define COUNT 50

static int64_t min_deletion_size(char strs[][M + 1], int n, int m) {
    int64_t longest[M];
    int64_t best = 0;
    for (int j = 0; j < m; j++) {
        longest[j] = 1;
        for (int k = 0; k < j; k++) {
            int before = 1;
            for (int i = 0; i < n; i++) {
                if (strs[i][k] > strs[i][j]) {
                    before = 0;
                    break;
                }
            }
            if (before && longest[k] + 1 > longest[j]) longest[j] = longest[k] + 1;
        }
        if (longest[j] > best) best = longest[j];
    }
    return m - best;
}

static int64_t seed = 960;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int cmp_char(const void *a, const void *b) {
    return *(const char *)a - *(const char *)b;
}

static char cases[COUNT][N][M + 1];

int main(void) {
    int rounds = 40;
    for (int c = 0; c < COUNT; c++) {
        int64_t letters = 2 + c % 25;
        int swaps = c % 10;
        for (int s = 0; s < N; s++) {
            char *b = cases[c][s];
            for (int i = 0; i < M; i++) b[i] = (char)('a' + next_random() % letters);
            qsort(b, M, 1, cmp_char);
            for (int k = 0; k < swaps; k++) {
                int64_t p = next_random() % (M - 1);
                char t = b[p];
                b[p] = b[p + 1];
                b[p + 1] = t;
            }
            b[M] = '\0';
        }
    }
    int64_t total = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int i = 0; i < COUNT; i++) {
            int64_t d = min_deletion_size(cases[(r + i) % COUNT], N, M);
            total += d;
            check = (check * 31 + d + i) % 1000000007;
        }
    }
    printf("%d rounds over 50 cases of 100 strings of 100 letters: %lld columns deleted, checksum %lld\n",
           rounds, (long long)total, (long long)check);
    return 0;
}
