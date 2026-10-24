// Benchmark: LeetCode #967 Numbers With Same Consecutive Differences --
// the ★ arm, level by level, for every n from 2 to 9 and every k from 0
// to 9. Mirrors nums_same_consec_diff.kara, .rs, .py and go-seq/. Each
// call mallocs its levels, as the other languages grow theirs.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// The numbers in *out, their count returned; at most 9 * 2^(n-1).
static int nums_same_consec_diff(int n, int k, int64_t **out) {
    int cap = 9 << (n - 1);
    int64_t *level = malloc(sizeof(int64_t) * cap), *next = malloc(sizeof(int64_t) * cap);
    int len = 0;
    for (int d = 1; d < 10; d++) level[len++] = d;
    for (int i = 1; i < n; i++) {
        int m = 0;
        for (int j = 0; j < len; j++) {
            int64_t x = level[j], last = x % 10;
            if (last + k <= 9) next[m++] = x * 10 + last + k;
            if (k > 0 && last - k >= 0) next[m++] = x * 10 + last - k;
        }
        int64_t *t = level;
        level = next;
        next = t;
        len = m;
    }
    free(next);
    *out = level;
    return len;
}

int main(void) {
    int rounds = 2000;
    int64_t found = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int n = 2; n < 10; n++) {
            for (int k = 0; k < 10; k++) {
                int64_t *v;
                int len = nums_same_consec_diff(n, k, &v);
                for (int i = 0; i < len; i++) {
                    found++;
                    check = (check * 31 + v[i]) % 1000000007;
                }
                free(v);
            }
        }
    }
    printf("%d rounds over n from 2 to 9 and k from 0 to 9: %lld numbers, checksum %lld\n", rounds,
           (long long)found, (long long)check);
    return 0;
}
