// LeetCode #1682: Longest Palindromic Subsequence II -- the bench's C
// mirror: the ★ arm on 200 random strings of 250 letters from the first 4
// of the alphabet, all drawn first, each answered 2 times. The table is
// one block of n * n * 26 entries, calloc'd for each answer.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define COUNT 200
#define N 250
#define ROUNDS 2

static int32_t longest_palindrome_subseq(const char *s, int64_t n) {
    if (n == 0) return 0;
    int32_t *best = calloc((size_t)(n * n * 26), sizeof *best);
#define AT(i, j, c) best[((i) * n + (j)) * 26 + (c)]
    for (int64_t i = n - 1; i >= 0; i--) {
        for (int64_t j = i + 1; j < n; j++) {
            for (int64_t c = 0; c < 26; c++) {
                if (s[i] - 'a' == c && s[j] - 'a' == c) {
                    int32_t inside = 0;
                    if (i + 1 < j - 1) {
                        for (int64_t d = 0; d < 26; d++) {
                            if (d != c && AT(i + 1, j - 1, d) > inside) inside = AT(i + 1, j - 1, d);
                        }
                    }
                    AT(i, j, c) = inside + 2;
                } else {
                    int32_t a = AT(i + 1, j, c), b = AT(i, j - 1, c);
                    AT(i, j, c) = a > b ? a : b;
                }
            }
        }
    }
    int32_t answer = 0;
    for (int64_t c = 0; c < 26; c++) {
        if (AT(0, n - 1, c) > answer) answer = AT(0, n - 1, c);
    }
#undef AT
    free(best);
    return answer;
}

// ---- the harness ----------------------------------------------------------

static int64_t seed = 1682;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    static const char alphabet[] = "abcd";
    static char strings[COUNT][N + 1];
    for (int c = 0; c < COUNT; c++) {
        for (int i = 0; i < N; i++) strings[c][i] = alphabet[next_random() % 4];
        strings[c][N] = '\0';
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int c = 0; c < COUNT; c++) {
            int64_t answer = longest_palindrome_subseq(strings[c], N);
            total += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    printf("%d strings of %d letters, %d rounds: answers sum to %lld, checksum %lld\n", COUNT, N, ROUNDS, (long long)total, (long long)check);
    return 0;
}
