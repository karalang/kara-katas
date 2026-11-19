// LeetCode #1625: Lexicographically Smallest String After Applying
// Operations -- the bench in C, mirroring smallest.kara: every rotation by
// a multiple of gcd(b, n) with every count of additions, each string made
// (a fresh buffer, as the others build a fresh string) and the least kept.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t gcd(int64_t x, int64_t y) { return y == 0 ? x : gcd(y, x % y); }

// the answer into `best`, which holds n + 1 bytes
static void find_lex_smallest_string(const char *s, int64_t n, int32_t a, int32_t b, char *best) {
    int64_t *digits = malloc(sizeof(int64_t) * (size_t)n);
    for (int64_t i = 0; i < n; i++) digits[i] = s[i] - '0';
    int64_t step = gcd(b, n);
    int64_t even_counts = b % 2 == 1 ? 10 : 1;
    memcpy(best, s, (size_t)n + 1);
    for (int64_t start = 0; start < n; start += step) {
        for (int64_t odd = 0; odd < 10; odd++) {
            for (int64_t even = 0; even < even_counts; even++) {
                char *t = malloc((size_t)n + 1);
                for (int64_t i = 0; i < n; i++) {
                    int64_t count = i % 2 == 1 ? odd : even;
                    t[i] = (char)('0' + (digits[(i + start) % n] + count * a) % 10);
                }
                t[n] = '\0';
                if (strcmp(t, best) < 0) memcpy(best, t, (size_t)n + 1);
                free(t);
            }
        }
    }
    free(digits);
}

static int64_t seed = 1625;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    enum { CASES = 200, N = 100 };
    static char strings[CASES][N + 1];
    int32_t as[CASES], bs[CASES];
    for (int k = 0; k < CASES; k++) {
        for (int i = 0; i < N; i++) strings[k][i] = (char)('0' + next_random() % 10);
        strings[k][N] = '\0';
        as[k] = (int32_t)(next_random() % 9 + 1);
        bs[k] = (int32_t)(next_random() % 99 + 1);
    }
    int64_t check = 0, zeros = 0;
    char best[N + 1];
    for (int k = 0; k < CASES; k++) {
        find_lex_smallest_string(strings[k], N, as[k], bs[k], best);
        for (int i = 0; i < N; i++) {
            if (best[i] == '0') zeros++;
            check = (check * 31 + (best[i] - '0') + 1) % 1000000007;
        }
    }
    printf("200 cases of 100 digits: %lld zeros in the answers, checksum %lld\n", (long long)zeros, (long long)check);
    return 0;
}
