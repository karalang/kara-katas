// LeetCode #1312 bench, C: the ★ arm (the interval costs kept in one row)
// on the same 20 strings and 50 passes. Each call copies the string, as the
// others build a fresh one, and takes a fresh row.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t min_insertions(const char *s, int64_t n) {
    int64_t *row = calloc((size_t)n, sizeof(int64_t));
    for (int64_t i = n - 1; i >= 0; i--) {
        int64_t inside = 0;
        for (int64_t j = i + 1; j < n; j++) {
            int64_t keep = row[j];
            if (s[i] == s[j]) {
                row[j] = inside;
            } else {
                row[j] = 1 + (keep < row[j - 1] ? keep : row[j - 1]);
            }
            inside = keep;
        }
    }
    int64_t r = row[n - 1];
    free(row);
    return r;
}

static int64_t seed = 1312;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const char *letters = "abcdefghijklmnopqrstuvwxyz";
    enum { N = 500 };
    static char strings[20][N];
    for (int g = 0; g < 20; g++) {
        int64_t k = g % 3 == 0 ? 2 : g % 3 == 1 ? 4 : 26;
        for (int i = 0; i < N; i++) strings[g][i] = letters[next_random() % k];
    }
    int64_t check = 0;
    for (int64_t pass = 0; pass < 50; pass++) {
        for (int g = 0; g < 20; g++) {
            int64_t k = g % 3 == 0 ? 2 : g % 3 == 1 ? 4 : 26;
            strings[g][check % N] = letters[(check / 7) % k];
            char *s = malloc(N + 1);
            memcpy(s, strings[g], N);
            s[N] = '\0';
            int64_t got = min_insertions(s, N);
            free(s);
            check = (check * 31 + got + pass) % 1000000007;
        }
    }
    printf("50 passes over 20 strings of 500: checksum %lld\n", (long long)check);
    return 0;
}
