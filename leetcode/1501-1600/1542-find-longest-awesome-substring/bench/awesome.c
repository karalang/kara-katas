// LeetCode #1542: Find Longest Awesome Substring -- bench: the ★ arm (prefix
// parity masks, first places in an array) over 100 strings of 1 to 100000
// digits, each over its own first 1 to 10, built once, each asked 4 times.
// C mirror of awesome.kara.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t longest_awesome(const char *s, int64_t n) {
    int64_t *first = malloc(1024 * sizeof(int64_t));
    for (int m = 0; m < 1024; m++) first[m] = n + 1;
    first[0] = 0;
    int64_t mask = 0, best = 0;
    for (int64_t i = 0; i < n; i++) {
        mask ^= (int64_t)1 << (s[i] - '0');
        int64_t end = i + 1;
        if (end - first[mask] > best) best = end - first[mask];
        for (int d = 0; d < 10; d++) {
            int64_t len = end - first[mask ^ (1 << d)];
            if (len > best) best = len;
        }
        if (first[mask] > n) first[mask] = end;
    }
    free(first);
    return best;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

int main(void) {
    int64_t seed = 1542;
    char *strings[100];
    int64_t lens[100];
    for (int k = 0; k < 100; k++) {
        int64_t a = next_random(&seed);
        int64_t n = (a * 32768 + next_random(&seed)) % 100000 + 1;
        int64_t digits = next_random(&seed) % 10 + 1;
        char *s = malloc(n);
        for (int64_t i = 0; i < n; i++) {
            s[i] = (char)('0' + next_random(&seed) % digits);
        }
        strings[k] = s;
        lens[k] = n;
    }
    int64_t check = 0;
    for (int p = 0; p < 4; p++) {
        for (int k = 0; k < 100; k++) {
            check = mix(check, longest_awesome(strings[k], lens[k]));
        }
    }
    for (int k = 0; k < 100; k++) free(strings[k]);
    printf("4 passes over 100 strings of up to 100000 digits: checksum %lld\n", (long long)check);
    return 0;
}
