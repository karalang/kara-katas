// LeetCode #1528: Shuffle String -- bench: the ★ arm over 100000 random
// strings of 1 to 100 letters with shuffled indices, built once and
// answered 30 times.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static char *restore_string(const char *s, const int64_t *indices, int64_t n) {
    char *out = malloc((size_t)n + 1);
    for (int64_t i = 0; i < n; i++) {
        out[indices[i]] = s[i];
    }
    out[n] = 0;
    return out;
}

static int64_t seed = 1528;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) {
    return (check * 31 + x + 1) % 1000000007;
}

int main(void) {
    enum { COUNT = 100000 };
    static char *strs[COUNT];
    static int64_t *idx[COUNT];
    static int64_t lens[COUNT];
    for (int c = 0; c < COUNT; c++) {
        int64_t n = next_random() % 100 + 1;
        lens[c] = n;
        strs[c] = malloc((size_t)n + 1);
        for (int64_t i = 0; i < n; i++) {
            strs[c][i] = (char)(97 + next_random() % 26);
        }
        strs[c][n] = 0;
        idx[c] = malloc((size_t)n * sizeof(int64_t));
        for (int64_t i = 0; i < n; i++) {
            idx[c][i] = i;
        }
        for (int64_t i = n - 1; i >= 1; i--) {
            int64_t j = next_random() % (i + 1);
            int64_t t = idx[c][i];
            idx[c][i] = idx[c][j];
            idx[c][j] = t;
        }
    }
    int64_t check = 0;
    for (int pass = 0; pass < 30; pass++) {
        for (int c = 0; c < COUNT; c++) {
            char *answer = restore_string(strs[c], idx[c], lens[c]);
            check = mix(check, (unsigned char)answer[pass % lens[c]]);
            free(answer);
        }
    }
    printf("30 passes over 100000 strings of up to 100 letters: checksum %lld\n", (long long)check);
    for (int c = 0; c < COUNT; c++) {
        free(strs[c]);
        free(idx[c]);
    }
    return 0;
}
