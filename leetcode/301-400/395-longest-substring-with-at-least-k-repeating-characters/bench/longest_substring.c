// Benchmark for #395: mirror of longest_substring.kara (divide and conquer).
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t longest(const unsigned char *b, int64_t lo, int64_t hi, int64_t k) {
    if (hi - lo < k) {
        return 0;
    }
    int64_t count[26] = {0};
    for (int64_t i = lo; i < hi; i++) {
        count[b[i] - 97]++;
    }
    int64_t best = 0, start = lo;
    int split = 0;
    for (int64_t i = lo; i < hi; i++) {
        if (count[b[i] - 97] < k) {
            split = 1;
            int64_t r = longest(b, start, i, k);
            if (r > best) best = r;
            start = i + 1;
        }
    }
    if (!split) {
        return hi - lo;
    }
    int64_t r = longest(b, start, hi, k);
    return r > best ? r : best;
}

static int64_t seed = 395;

static int64_t step(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    unsigned char *pool = malloc(1000000);
    for (int i = 0; i < 1000000; i++) {
        int64_t x = step() % 26;
        int64_t y = step() % 26;
        pool[i] = (unsigned char)((x < y ? x : y) + 97);
    }
    int64_t total = 0, checksum = 0;
    for (int n = 0; n < 10000; n++) {
        int64_t hi = step();
        int64_t a = (hi * 32768 + step()) % (1000000 - 10000);
        int64_t k = 1 + step() % 30;
        int64_t r = longest(pool + a, 0, 10000, k);
        total += r;
        checksum = (checksum * 31 + r) % 1000000007;
    }
    printf("10000 windows: total %lld, checksum %lld\n", (long long)total, (long long)checksum);
    free(pool);
    return 0;
}
