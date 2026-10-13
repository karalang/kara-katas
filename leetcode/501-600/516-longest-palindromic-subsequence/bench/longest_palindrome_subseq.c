// Benchmark for #516: C mirror of the ★ arm (a table over substrings);
// see longest_palindrome_subseq.kara. The table is a fresh array of
// rows for every call, as the ★ arm's `vec![vec![0; n]; n]`.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t longest_palindrome_subseq(const char *b, int64_t n) {
    int64_t **best = malloc(n * sizeof(int64_t *));
    for (int64_t i = 0; i < n; i++) best[i] = calloc(n, sizeof(int64_t));
    for (int64_t i = n - 1; i >= 0; i--) {
        best[i][i] = 1;
        for (int64_t j = i + 1; j < n; j++) {
            if (b[i] == b[j]) {
                best[i][j] = best[i + 1][j - 1] + 2;
            } else {
                int64_t x = best[i + 1][j], y = best[i][j - 1];
                best[i][j] = x > y ? x : y;
            }
        }
    }
    int64_t answer = best[0][n - 1];
    for (int64_t i = 0; i < n; i++) free(best[i]);
    free(best);
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    // 120 random strings of 1,000 letters (the problem's most), from the
    // first 4 or all 26 in turn, solved once each.
    int64_t seed = 516, strings = 120, total = 0, checksum = 0;
    char s[1000];
    for (int64_t t = 0; t < strings; t++) {
        int64_t letters = t % 2 == 0 ? 4 : 26;
        for (int i = 0; i < 1000; i++) s[i] = 'a' + next_random(&seed) % letters;
        int64_t v = longest_palindrome_subseq(s, 1000);
        total += v;
        checksum = (checksum * 31 + v) % 1000000007;
    }
    printf("%lld strings of 1000 letters: %lld in all, checksum %lld\n", (long long)strings,
           (long long)total, (long long)checksum);
    return 0;
}
