// Benchmark workload for LeetCode #342 — C mirror of power_of_four.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define LEN 500000
#define PUNCHES 100
#define MODULUS 1073741789LL
#define I32_MIN (-2147483648LL)

static int is_power_of_four(int32_t n) {
    return n > 0 && (n & (n - 1)) == 0 && (n & 0x55555555) != 0;
}

static int64_t next(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int32_t two_to(int64_t k) {
    int32_t p = 1;
    for (int64_t i = 0; i < k; i++) {
        p *= 2;
    }
    return p;
}

static int32_t value(int64_t *seed) {
    int64_t kind = next(seed) % 3;
    if (kind == 0) {
        return two_to(2 * (next(seed) % 16));
    }
    if (kind == 1) {
        int64_t r = next(seed) % 3;
        if (r == 0) {
            return two_to(2 * (next(seed) % 15) + 1);
        }
        int32_t p = two_to(2 * (next(seed) % 16));
        if (r == 1) {
            return p + 1;
        }
        return p - 1;
    }
    /* Two draws, in order: C leaves the order of `next(seed) * 32768 +
       next(seed)` unspecified, so name them. */
    int64_t x = next(seed);
    int64_t y = next(seed);
    int64_t hi = x * 32768 + y;
    return (int32_t)(hi * 4 + next(seed) % 4 + I32_MIN);
}

int main(void) {
    int64_t seed = 342;
    int32_t *a = malloc(sizeof(int32_t) * LEN);
    for (int64_t i = 0; i < LEN; i++) {
        a[i] = value(&seed);
    }
    int64_t sink = 0;
    for (int64_t p = 0; p < PUNCHES; p++) {
        int64_t x = next(&seed);
        int64_t y = next(&seed);
        int64_t pos = (x * 32768 + y) % LEN;
        a[pos] = value(&seed);
        int64_t count = 0;
        int64_t sum = 0;
        for (int64_t i = 0; i < LEN; i++) {
            if (is_power_of_four(a[i])) {
                count += 1;
                sum += a[i];
            }
        }
        sink = (sink * 31 + count + sum % MODULUS) % MODULUS;
    }
    printf("sink %lld\n", (long long)sink);
    free(a);
    return 0;
}
