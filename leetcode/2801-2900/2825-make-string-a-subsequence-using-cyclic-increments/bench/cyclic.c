// LeetCode #2825: Make String a Subsequence Using Cyclic Increments --
// the bench's C mirror of the ★ arm: two pointers over the bytes.

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

static bool can_make_subsequence(const char *a, long n, const char *b, long m) {
    long j = 0;
    for (long i = 0; i < n; i++) {
        if (j == m) break;
        char c = a[i], next = c == 'z' ? 'a' : c + 1;
        if (c == b[j] || next == b[j]) j++;
    }
    return j == m;
}

static long long seed = 2825;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}
static long long wide(void) {
    long long a = next_random();
    return a * 32768 + next_random();
}

static char *letters(long n, long from, long width) {
    char *s = malloc(n);
    for (long i = 0; i < n; i++) s[i] = (char)((from + next_random() % width) % 26 + 97);
    return s;
}

int main(void) {
    enum { COUNT = 100, ROUNDS = 50, N = 100000 };
    char *s1[COUNT], *s2[COUNT];
    long m[COUNT];
    for (int c = 0; c < COUNT; c++) {
        s1[c] = letters(N, 23, 6);
        m[c] = wide() % 50000 + 1;
        s2[c] = letters(m[c], 23, 6);
    }
    long long yes = 0, check = 0;
    for (int r = 0; r < ROUNDS; r++)
        for (int c = 0; c < COUNT; c++) {
            bool a = can_make_subsequence(s1[c], N, s2[c], m[c]);
            if (a) yes++;
            check = (check * 31 + (a ? 1 : 0) + r) % 1000000007;
        }
    printf("%d pairs of 100000, %d rounds: %lld true, checksum %lld\n", COUNT, ROUNDS, yes, check);
    for (int c = 0; c < COUNT; c++) {
        free(s1[c]);
        free(s2[c]);
    }
    return 0;
}
