/*
 * LeetCode 633 -- Sum of Square Numbers, bench mirror in C.
 *
 * The ★ arm of judge_square_sum.kara: two pointers from 0 and from the
 * integer square root of `c`, found by binary search. Same values, same
 * output line.
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t root(int64_t n) {
    int64_t lo = 0, hi = (n < 3037000499LL ? n : 3037000499LL) + 1;
    while (hi - lo > 1) {
        int64_t mid = (lo + hi) / 2;
        if (mid * mid <= n) lo = mid;
        else hi = mid;
    }
    return lo;
}

static int judge_square_sum(int64_t c) {
    int64_t a = 0, b = root(c);
    while (a <= b) {
        int64_t sum = a * a + b * b;
        if (sum == c) return 1;
        if (sum < c) a++;
        else b--;
    }
    return 0;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 633;
    const int64_t count = 10000;
    int64_t *values = malloc(count * sizeof(int64_t));
    for (int64_t i = 0; i < count; i++) {
        int64_t wide = next_random(&seed) * 32768;
        wide += next_random(&seed);
        values[i] = wide * 2 + next_random(&seed) % 2;
    }
    int64_t yes = 0, checksum = 0;
    for (int64_t i = 0; i < count; i++) {
        if (judge_square_sum(values[i])) {
            yes++;
            checksum = (checksum * 31 + values[i]) % 1000000007;
        }
    }
    printf("%lld values: %lld sums of two squares, checksum %lld\n", (long long)count,
           (long long)yes, (long long)checksum);
    free(values);
    return 0;
}
