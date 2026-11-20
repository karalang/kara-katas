// LeetCode #1754: Largest Merge Of Two Strings -- the bench (merge.kara in
// C): the larger rest goes first.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

enum { COUNT = 200, ROUNDS = 20, N = 3000 };

// whether a[0..m) is larger than b[0..n) in byte order, a prefix being
// the smaller
static int larger(const char *a, int64_t m, const char *b, int64_t n) {
    int64_t common = m < n ? m : n;
    int c = memcmp(a, b, common);
    if (c != 0) return c > 0;
    return m > n;
}

static void largest_merge(const char *w1, const char *w2, int64_t n, char *merge) {
    int64_t i = 0, j = 0, at = 0;
    while (i < n || j < n) {
        if (larger(w1 + i, n - i, w2 + j, n - j)) merge[at++] = w1[i++];
        else merge[at++] = w2[j++];
    }
}

static int64_t seed = 1754;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static char words[COUNT][2][N];
    for (int c = 0; c < COUNT; c++)
        for (int w = 0; w < 2; w++)
            for (int i = 0; i < N; i++) words[c][w][i] = next_random() % 300 == 0 ? 'b' : 'a';
    static char merge[2 * N];
    int64_t check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int c = 0; c < COUNT; c++) {
            largest_merge(words[c][0], words[c][1], N, merge);
            check = (check * 31 + r) % 1000000007;
            for (int64_t k = 0; k < 2 * N; k++) check = (check * 31 + (unsigned char)merge[k]) % 1000000007;
        }
    }
    printf("%d pairs of %d letters, %d rounds: checksum %lld\n", COUNT, N, ROUNDS, (long long)check);
    return 0;
}
