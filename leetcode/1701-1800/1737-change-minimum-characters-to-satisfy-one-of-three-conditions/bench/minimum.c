// LeetCode #1737: Change Minimum Characters to Satisfy One of Three
// Conditions -- the bench (minimum.kara): letter counts, and every
// boundary tried.

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static long min_long(long x, long y) { return x < y ? x : y; }

static long min_characters(const char *a, const char *b) {
    long count_a[26] = {0}, count_b[26] = {0};
    long m = (long)strlen(a), n = (long)strlen(b);
    for (long i = 0; i < m; i++) count_a[a[i] - 'a']++;
    for (long i = 0; i < n; i++) count_b[b[i] - 'a']++;
    long best = m + n;
    for (int c = 0; c < 26; c++) best = min_long(best, m + n - count_a[c] - count_b[c]);
    long below_a = 0, below_b = 0;
    for (int c = 1; c < 26; c++) {
        below_a += count_a[c - 1];
        below_b += count_b[c - 1];
        best = min_long(best, m - below_a + below_b);
        best = min_long(best, n - below_b + below_a);
    }
    return best;
}

static long next_random(long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648L;
    return *seed / 65536;
}

int main(void) {
    int count = 20;
    long rounds = 200, n = 100000, seed = 1737;
    char **as = malloc(sizeof(char *) * count), **bs = malloc(sizeof(char *) * count);
    for (int p = 0; p < count; p++) {
        as[p] = malloc(n + 1);
        for (long i = 0; i < n; i++) as[p][i] = (char)(97 + next_random(&seed) % 26);
        as[p][n] = '\0';
        bs[p] = malloc(n + 1);
        for (long i = 0; i < n; i++) bs[p][i] = (char)(97 + next_random(&seed) % 26);
        bs[p][n] = '\0';
    }
    long sum = 0, check = 0;
    for (long r = 0; r < rounds; r++) {
        for (int p = 0; p < count; p++) {
            long answer = min_characters(as[p], bs[p]);
            sum += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    for (int p = 0; p < count; p++) {
        free(as[p]);
        free(bs[p]);
    }
    free(as);
    free(bs);
    printf("%d pairs of %ld letters, %ld rounds: changes sum to %ld, checksum %ld\n", count, n, rounds, sum, check);
    return 0;
}
