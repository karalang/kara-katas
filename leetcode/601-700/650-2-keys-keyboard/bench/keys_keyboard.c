// Benchmark for #650: the sum of the prime factors, as the Kara ★ arm.
#include <stdint.h>
#include <stdio.h>

static int64_t min_steps(int64_t n) {
    int64_t rest = n, steps = 0, p = 2;
    while (p * p <= rest) {
        while (rest % p == 0) {
            steps += p;
            rest /= p;
        }
        p += 1;
    }
    if (rest > 1) steps += rest;
    return steps;
}

int main(void) {
    int64_t limit = 1000000, total = 0, checksum = 0;
    for (int64_t n = 1; n <= limit; n++) {
        int64_t steps = min_steps(n);
        total += steps;
        checksum = (checksum * 31 + steps) % 1000000007;
    }
    printf("1 to %lld: total %lld, checksum %lld\n", (long long)limit,
           (long long)total, (long long)checksum);
    return 0;
}
