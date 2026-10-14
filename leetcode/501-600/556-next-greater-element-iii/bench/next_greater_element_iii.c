// Benchmark for #556: C mirror of the ★ arm (the next permutation of the
// digits); see next_greater_element_iii.kara. The digits go in a fresh
// malloc'd buffer that grows as it fills, as a Vec does.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t next_greater_element(int64_t n) {
    size_t cap = 4, len = 0;
    int64_t *d = malloc(cap * sizeof(int64_t));
    for (int64_t x = n; x > 0; x /= 10) {
        if (len == cap) d = realloc(d, (cap *= 2) * sizeof(int64_t));
        d[len++] = x % 10;
    }
    for (size_t a = 0, b = len - 1; a < b; a++, b--) {
        int64_t t = d[a]; d[a] = d[b]; d[b] = t;
    }
    int64_t i = (int64_t)len - 2;
    while (i >= 0 && d[i] >= d[i + 1]) i--;
    if (i < 0) {
        free(d);
        return -1;
    }
    size_t j = len - 1;
    while (d[j] <= d[i]) j--;
    int64_t t = d[i]; d[i] = d[j]; d[j] = t;
    for (size_t a = (size_t)i + 1, b = len - 1; a < b; a++, b--) {
        int64_t u = d[a]; d[a] = d[b]; d[b] = u;
    }
    int64_t out = 0;
    for (size_t k = 0; k < len; k++) out = out * 10 + d[k];
    free(d);
    return out > 2147483647 ? -1 : out;
}

int main(void) {
    const int count = 500000;
    int64_t seed = 556;
    int64_t *numbers = malloc(count * sizeof(int64_t));
    for (int t = 0; t < count; t++) {
        int64_t top = t % 3 == 0 ? 1000 : t % 3 == 1 ? 10000000 : 2147483647;
        int64_t a = next_random(&seed);
        int64_t b = next_random(&seed);
        numbers[t] = 1 + (a * 65536 + b) % top;
    }
    long found = 0;
    int64_t checksum = 0;
    for (int round = 0; round < 20; round++) {
        for (int g = 0; g < count; g++) {
            int64_t got = next_greater_element(numbers[(round * 7 + g) % count]);
            if (got > 0) found++;
            checksum = (checksum * 31 + got + 1) % 1000000007;
        }
    }
    printf("%d numbers, 20 rounds each: %ld have a next, checksum %lld\n", count, found, (long long)checksum);
    free(numbers);
    return 0;
}
