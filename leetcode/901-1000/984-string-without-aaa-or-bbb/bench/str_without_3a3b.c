// Benchmark: LeetCode #984 String Without AAA or BBB -- the ★ arm, greedy,
// reading the tail, on every pair of counts up to LeetCode's 100.
// Mirrors str_without_3a3b.kara, .rs, .py and go-seq/.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// The answer in a fresh buffer of a + b letters, which the caller frees.
static char *str_without_3a3b(int64_t a, int64_t b) {
    char *s = malloc((size_t)(a + b + 1));
    int64_t n = 0;
    int64_t left_a = a, left_b = b;
    while (left_a > 0 || left_b > 0) {
        int write_a;
        if (n >= 2 && s[n - 1] == 'a' && s[n - 2] == 'a') {
            write_a = 0;
        } else if (n >= 2 && s[n - 1] == 'b' && s[n - 2] == 'b') {
            write_a = 1;
        } else {
            write_a = left_a >= left_b;
        }
        if (write_a) {
            s[n++] = 'a';
            left_a--;
        } else {
            s[n++] = 'b';
            left_b--;
        }
    }
    s[n] = 0;
    return s;
}

int main(void) {
    int64_t rounds = 100;
    int64_t pa[10201], pb[10201];
    int64_t n = 0;
    for (int64_t a = 0; a < 101; a++) {
        for (int64_t b = 0; b < 101; b++) {
            if (a + b > 0 && a <= 2 * b + 2 && b <= 2 * a + 2) {
                pa[n] = a;
                pb[n] = b;
                n++;
            }
        }
    }
    int64_t letters = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t i = 0; i < n; i++) {
            int64_t j = (r + i) % n;
            char *s = str_without_3a3b(pa[j], pb[j]);
            int64_t len = pa[j] + pb[j];
            int64_t middle = s[len / 2] == 'a' ? 1 : 2;
            letters += len;
            check = (check * 31 + len * 3 + middle) % 1000000007;
            free(s);
        }
    }
    printf("%lld rounds over %lld pairs up to 100: %lld letters, checksum %lld\n",
           (long long)rounds, (long long)n, (long long)letters, (long long)check);
    return 0;
}
