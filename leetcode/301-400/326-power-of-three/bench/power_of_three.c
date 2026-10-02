// Benchmark workload for LeetCode #326 — C mirror of power_of_three.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define LEN 300000
#define PUNCHES 40
#define MODULUS 1073741789LL
#define I32_MIN (-2147483648LL)

static int is_power_of_three(int64_t n) {
    if (n <= 0) {
        return 0;
    }
    int64_t m = n;
    while (m % 3 == 0) {
        m /= 3;
    }
    return m == 1;
}

static int64_t next(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t power(int64_t k) {
    int64_t p = 1;
    for (int64_t i = 0; i < k; i++) {
        p *= 3;
    }
    return p;
}

static int64_t value(int64_t *seed) {
    int64_t kind = next(seed) % 3;
    if (kind == 0) {
        return power(next(seed) % 20);
    }
    if (kind == 1) {
        int64_t p = power(next(seed) % 20);
        if (next(seed) % 2 == 0) {
            return p + 1;
        }
        return p - 1;
    }
    /* Two draws, in order: C leaves the order of `next(seed) * 32768 +
       next(seed)` unspecified, so name them. */
    int64_t a = next(seed);
    int64_t b = next(seed);
    int64_t hi = a * 32768 + b;
    return hi * 4 + next(seed) % 4 + I32_MIN;
}

int main(void) {
    int64_t seed = 326;
    int64_t *a = malloc(sizeof(int64_t) * LEN);
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
            if (is_power_of_three(a[i])) {
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
