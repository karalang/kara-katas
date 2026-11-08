// LeetCode #1525: Number of Good Ways to Split a String -- bench: the ★
// arm over 200 random strings of 1 to 100000 letters, built once and
// answered 10 times. Each answer takes its own copy of the string, as the
// other languages' do (`malloc` and `free`).

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t num_splits(const char *src, int64_t n) {
    char *b = malloc((size_t)n);
    memcpy(b, src, (size_t)n);
    int64_t *left = malloc((size_t)n * sizeof(int64_t));
    int64_t *right = malloc((size_t)n * sizeof(int64_t));
    bool seen[26] = {false};
    int64_t distinct = 0;
    for (int64_t i = 0; i < n; i++) {
        int c = b[i] - 97;
        if (!seen[c]) {
            seen[c] = true;
            distinct++;
        }
        left[i] = distinct;
    }
    memset(seen, 0, sizeof seen);
    distinct = 0;
    for (int64_t i = n - 1; i >= 0; i--) {
        int c = b[i] - 97;
        if (!seen[c]) {
            seen[c] = true;
            distinct++;
        }
        right[i] = distinct;
    }
    int64_t good = 0;
    for (int64_t i = 1; i < n; i++) {
        if (left[i - 1] == right[i]) {
            good++;
        }
    }
    free(left);
    free(right);
    free(b);
    return good;
}

static int64_t seed = 1525;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) {
    return (check * 31 + x + 1) % 1000000007;
}

int main(void) {
    enum { COUNT = 200 };
    static char *strings[COUNT];
    static int64_t lens[COUNT];
    for (int c = 0; c < COUNT; c++) {
        int64_t hi = next_random();
        int64_t n = (hi * 32768 + next_random()) % 100000 + 1;
        int64_t letters = next_random() % 26 + 1;
        strings[c] = malloc((size_t)n);
        lens[c] = n;
        for (int64_t i = 0; i < n; i++) {
            strings[c][i] = (char)(97 + next_random() % letters);
        }
    }
    int64_t check = 0, total = 0;
    for (int pass = 0; pass < 10; pass++) {
        for (int c = 0; c < COUNT; c++) {
            int64_t good = num_splits(strings[c], lens[c]);
            total += good;
            check = mix(check, good);
        }
    }
    printf("10 passes over 200 strings of up to 100000 letters: %lld good splits, checksum %lld\n",
           (long long)total, (long long)check);
    for (int c = 0; c < COUNT; c++) {
        free(strings[c]);
    }
    return 0;
}
