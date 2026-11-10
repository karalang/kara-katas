// LeetCode #2109: Adding Spaces to a String -- the benchmark, the same
// algorithm as spaces.kara: one walk over the letters with an index into
// the spaces.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 300000

// Writes the spaced string into a fresh buffer the caller frees, as the
// other languages build a new string each call.
static char *add_spaces(const char *s, int64_t n, const int64_t *spaces, int64_t k, int64_t *len) {
    char *out = malloc((size_t)(n + k + 1));
    int64_t o = 0, next = 0;
    for (int64_t i = 0; i < n; i++) {
        if (next < k && spaces[next] == i) {
            out[o++] = ' ';
            next++;
        }
        out[o++] = s[i];
    }
    out[o] = 0;
    *len = o;
    return out;
}

static int64_t seed = 2109;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const char *letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    static char strs[20][N + 1];
    static int64_t spaces[20][N];
    int64_t counts[20];
    for (int r = 0; r < 20; r++) {
        counts[r] = 0;
        for (int64_t i = 0; i < N; i++) {
            strs[r][i] = letters[next_random() % 52];
            if (next_random() % 3 == 0) spaces[r][counts[r]++] = i;
        }
        strs[r][N] = 0;
    }
    int64_t total = 0, check = 0;
    for (int r = 0; r < 20; r++) {
        for (int q = 0; q < 5; q++) {
            int64_t len;
            char *got = add_spaces(strs[r], N, spaces[r], counts[r], &len);
            total += len;
            for (int64_t j = 0; j < len; j += 997) check = (check * 31 + (unsigned char)got[j]) % 1000000007;
            free(got);
        }
    }
    printf("100 strings: %lld characters, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
