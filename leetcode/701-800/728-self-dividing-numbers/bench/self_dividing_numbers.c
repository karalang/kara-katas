// LeetCode #728: Self Dividing Numbers -- each digit, by remainders.
// Benchmark mirror of the Kara star arm: peel each number's digits off
// with % 10 and / 10, stopping at a 0 or a digit that does not divide
// it, and collect the numbers that pass into a fresh array.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int self_dividing(int64_t n) {
    for (int64_t rest = n; rest > 0; rest /= 10) {
        int64_t d = rest % 10;
        if (d == 0 || n % d != 0) return 0;
    }
    return 1;
}

static int64_t *self_dividing_numbers(int64_t left, int64_t right, int64_t *len) {
    int64_t *out = malloc((right - left + 1) * sizeof(int64_t));
    int64_t k = 0;
    for (int64_t n = left; n <= right; n++)
        if (self_dividing(n)) out[k++] = n;
    *len = k;
    return out;
}

int main(void) {
    int64_t seed = 728, count = 0, sum = 0;
    for (int r = 0; r < 40000; r++) {
        int64_t a = 1 + next_random(&seed) % 10000;
        int64_t b = 1 + next_random(&seed) % 10000;
        int64_t left = a < b ? a : b, right = a < b ? b : a, len;
        int64_t *found = self_dividing_numbers(left, right, &len);
        count += len;
        for (int64_t i = 0; i < len; i++) sum += found[i];
        free(found);
    }
    printf("40000 random ranges: %lld numbers, sum %lld\n", (long long)count, (long long)sum);
    return 0;
}
