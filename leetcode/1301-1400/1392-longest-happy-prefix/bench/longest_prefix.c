// LeetCode #1392 bench, C mirror of the ★ arm: the string copied into a
// fresh buffer each round, as the others build a fresh string, and the
// answer a copy of the prefix.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char *longest_prefix(const char *s, int64_t n, int64_t *out_len) {
    int64_t *border = calloc((size_t)n, sizeof(int64_t));
    int64_t k = 0;
    for (int64_t i = 1; i < n; i++) {
        while (k > 0 && s[i] != s[k]) k = border[k - 1];
        if (s[i] == s[k]) k += 1;
        border[i] = k;
    }
    int64_t len = border[n - 1];
    free(border);
    char *out = malloc((size_t)len + 1);
    memcpy(out, s, (size_t)len);
    out[len] = 0;
    *out_len = len;
    return out;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    enum { N = 100000 };
    const char *block = "abacaba";
    static char letters[N];
    for (int64_t i = 0; i < N; i++) letters[i] = block[i % 7];
    int64_t seed = 1392, check = 0;
    for (int round = 0; round < 2000; round++) {
        seed = (seed + check) % 2147483648LL;
        int64_t at = next_random(&seed) % N;
        char was = letters[at];
        letters[at] = (char)(97 + next_random(&seed) % 3);
        char *s = malloc(N + 1);
        memcpy(s, letters, N);
        s[N] = 0;
        int64_t len;
        char *got = longest_prefix(s, N, &len);
        free(s);
        free(got);
        letters[at] = was;
        check = (check * 131 + len * 7 + at) % 1000000007;
    }
    printf("2000 rounds over 10^5 letters: checksum %lld\n", (long long)check);
    return 0;
}
