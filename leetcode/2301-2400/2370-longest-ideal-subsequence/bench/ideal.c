// LeetCode #2370: Longest Ideal Subsequence -- the bench, the ★ arm in C:
// best[c] is the longest ideal subsequence so far ending in letter c, and
// a new letter extends the best one within k letters of it.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t longest_ideal_string(const char *s, int64_t n, int64_t k) {
    int64_t best[26] = {0};
    for (int64_t i = 0; i < n; i++) {
        int64_t c = s[i] - 'a';
        int64_t lo = c - k > 0 ? c - k : 0;
        int64_t hi = c + k < 25 ? c + k : 25;
        int64_t most = 0;
        for (int64_t d = lo; d <= hi; d++) {
            if (best[d] > most) {
                most = best[d];
            }
        }
        best[c] = most + 1;
    }
    int64_t top = 0;
    for (int d = 0; d < 26; d++) {
        if (best[d] > top) {
            top = best[d];
        }
    }
    return top;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    // string a: 10^5 random letters from the whole alphabet, answered with
    // k of a and of 2 a + 5
    const int64_t n = 100000;
    int64_t seed = 2370;
    char *strings[10];
    for (int a = 0; a < 10; a++) {
        strings[a] = malloc(n + 1);
        for (int64_t i = 0; i < n; i++) {
            strings[a][i] = (char)(97 + next_random(&seed) % 26);
        }
        strings[a][n] = 0;
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 10; p++) {
        for (int64_t a = 0; a < 10; a++) {
            int64_t ks[2] = {a, 2 * a + 5};
            for (int j = 0; j < 2; j++) {
                check = (check * 31 + longest_ideal_string(strings[a], n, ks[j]) + p) % 1000000007;
            }
        }
    }
    printf("10 passes over 10 strings of 10^5 letters: checksum %lld\n", (long long)check);
    for (int a = 0; a < 10; a++) {
        free(strings[a]);
    }
    return 0;
}
