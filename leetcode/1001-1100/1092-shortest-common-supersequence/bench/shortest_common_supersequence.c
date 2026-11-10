// Benchmark: LeetCode #1092 Shortest Common Supersequence -- C mirror of the
// ★ arm: the longest common subsequence's table, a row pointer per row,
// walked back from the end. The table and the answer are allocated per
// call as the Kāra arm's are. Same workload and sink as
// shortest_common_supersequence.kara.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define PAIRS 50
#define LEN 1000

// The answer is written into a fresh buffer of `*len` letters.
static char *shortest_common_supersequence(const char *x, int64_t n, const char *y, int64_t m,
                                           int64_t *len) {
    int64_t **lcs = malloc((n + 1) * sizeof(int64_t *));
    for (int64_t i = 0; i <= n; i++) {
        lcs[i] = calloc(m + 1, sizeof(int64_t));
    }
    for (int64_t i = 1; i <= n; i++) {
        for (int64_t j = 1; j <= m; j++) {
            if (x[i - 1] == y[j - 1]) {
                lcs[i][j] = lcs[i - 1][j - 1] + 1;
            } else {
                int64_t up = lcs[i - 1][j], left = lcs[i][j - 1];
                lcs[i][j] = up > left ? up : left;
            }
        }
    }
    char *out = malloc(n + m);
    int64_t k = 0, i = n, j = m;
    while (i > 0 && j > 0) {
        if (x[i - 1] == y[j - 1]) {
            out[k++] = x[i - 1];
            i--;
            j--;
        } else if (lcs[i - 1][j] >= lcs[i][j - 1]) {
            out[k++] = x[i - 1];
            i--;
        } else {
            out[k++] = y[j - 1];
            j--;
        }
    }
    while (i > 0) {
        out[k++] = x[--i];
    }
    while (j > 0) {
        out[k++] = y[--j];
    }
    for (int64_t lo = 0, hi = k - 1; lo < hi; lo++, hi--) {
        char t = out[lo];
        out[lo] = out[hi];
        out[hi] = t;
    }
    for (int64_t r = 0; r <= n; r++) {
        free(lcs[r]);
    }
    free(lcs);
    *len = k;
    return out;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 1092;
    static char a[PAIRS][LEN], b[PAIRS][LEN];
    for (int k = 0; k < PAIRS; k++) {
        int64_t letters = 2 + k % 25;
        for (int i = 0; i < LEN; i++) {
            a[k][i] = (char)(97 + next_random(&seed) % letters);
        }
        for (int i = 0; i < LEN; i++) {
            b[k][i] = (char)(97 + next_random(&seed) % letters);
        }
    }
    int64_t total = 0, check = 0;
    for (int round = 0; round < 4; round++) {
        for (int k = 0; k < PAIRS; k++) {
            int64_t len;
            char *s = shortest_common_supersequence(a[k], LEN, b[k], LEN, &len);
            total += len;
            check = (check * 31 + len) % 1000000007;
            check = (check * 31 + s[len / 3]) % 1000000007;
            check = (check * 31 + s[2 * len / 3]) % 1000000007;
            free(s);
        }
    }
    printf("4 rounds over 50 pairs of 1000 letters: lengths sum to %lld, checksum %lld\n",
           (long long)total, (long long)check);
    return 0;
}
