// Benchmark for #392: mirror of is_subsequence.kara (two pointers).
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int is_subsequence(const char *s, int64_t sn, const char *t, int64_t tn) {
    int64_t i = 0;
    for (int64_t k = 0; k < tn; k++) {
        if (i < sn && s[i] == t[k]) {
            i++;
        }
    }
    return i == sn;
}

static int64_t seed = 392;

static int64_t step(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t big(void) {
    int64_t hi = step();
    return hi * 32768 + step();
}

int main(void) {
    char *pool = malloc(1000000);
    for (int i = 0; i < 1000000; i++) {
        pool[i] = (char)(step() % 26 + 97);
    }
    int yes = 0;
    int64_t checksum = 0;
    for (int k = 0; k < 20000; k++) {
        int64_t a = big() % (1000000 - 100);
        int64_t len = step() % 10001;
        int64_t b = big() % (1000000 - len);
        int r = is_subsequence(pool + a, 100, pool + b, len);
        if (r) {
            yes++;
        }
        checksum = (checksum * 3 + (r ? 1 : 2)) % 1000000007;
    }
    printf("20000 pairs: %d subsequences, checksum %lld\n", yes, (long long)checksum);
    free(pool);
    return 0;
}
