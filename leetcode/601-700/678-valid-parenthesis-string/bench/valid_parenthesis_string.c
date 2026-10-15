// Benchmark for #678: the range of open counts, the ★ arm.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int check_valid_string(const char *s, int64_t n) {
    int64_t low = 0, high = 0;
    for (int64_t i = 0; i < n; i++) {
        char c = s[i];
        if (c == '(') {
            low += 1;
            high += 1;
        } else if (c == ')') {
            low -= 1;
            high -= 1;
        } else {
            low -= 1;
            high += 1;
        }
        if (high < 0) return 0;
        if (low < 0) low = 0;
    }
    return low == 0;
}

static int64_t seed = 678;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static char *random_string(int64_t c, int64_t *len) {
    char *s = malloc(201);
    int64_t n = 0;
    if (c % 3 == 0) {
        int64_t m = 1 + next_random() % 100;
        for (int64_t i = 0; i < m; i++) {
            int64_t d = next_random() % 3;
            s[n++] = d == 0 ? '(' : d == 1 ? ')' : '*';
        }
        *len = n;
        return s;
    }
    char b[201];
    int64_t bn = 0, open = 0, left = 1 + next_random() % 50;
    while (left > 0 || open > 0) {
        if (left > 0 && (open == 0 || next_random() % 2 == 0)) {
            b[bn++] = '(';
            open += 1;
            left -= 1;
        } else {
            b[bn++] = ')';
            open -= 1;
        }
    }
    int64_t stars = next_random() % 4;
    int64_t changes = next_random() % 3;
    for (int64_t i = 0; i < bn; i++) {
        int64_t r = next_random() % 10;
        if (r < stars) {
            s[n++] = '*';
        } else if (r == 9 && next_random() % 3 < changes) {
            s[n++] = b[i] == '(' ? ')' : '(';
        } else {
            s[n++] = b[i];
        }
    }
    *len = n;
    return s;
}

int main(void) {
    const int64_t count = 20000, rounds = 100;
    char **strings = malloc(sizeof(char *) * count);
    int64_t *lens = malloc(sizeof(int64_t) * count);
    for (int64_t c = 0; c < count; c++) strings[c] = random_string(c, &lens[c]);
    int64_t sum = 0, valid = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t i = 0; i < count; i++) {
            int64_t k = (i * 7919 + r * 104729) % count;
            int64_t n = lens[k];
            if (check_valid_string(strings[k], n)) {
                valid += 1;
                sum = (sum * 31 + n) % 1000000007;
            } else {
                sum = (sum * 31 + 1000 + n) % 1000000007;
            }
        }
    }
    printf("%lld rounds of %lld strings: %lld valid, checksum %lld\n", (long long)rounds,
           (long long)count, (long long)valid, (long long)sum);
    for (int64_t c = 0; c < count; c++) free(strings[c]);
    free(strings);
    free(lens);
    return 0;
}
