// Benchmark for #829: Consecutive Numbers Sum -- the ★ arm (each length).
//
// Mirrors consecutive_numbers_sum.kara: n has a run of k consecutive
// numbers exactly when n - k * (k - 1) / 2 is a positive multiple of k,
// and k runs while 1 + 2 + ... + k fits.

#include <stdint.h>
#include <stdio.h>

static int64_t consecutive_numbers_sum(int64_t n) {
    int64_t count = 0;
    for (int64_t k = 1; k * (k + 1) / 2 <= n; k++)
        if ((n - k * (k - 1) / 2) % k == 0) count++;
    return count;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    const int64_t count = 64, rounds = 16000;
    int64_t seed = 829;
    int64_t numbers[64];
    for (int64_t i = 0; i < count; i++) {
        int64_t a = next_random(&seed);
        int64_t r = a * 32768 + next_random(&seed);
        numbers[i] = 500000000 + r % 500000001;
    }
    int64_t total = 0, checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        int64_t r = consecutive_numbers_sum(numbers[round % count]);
        total += r;
        checksum = (checksum * 131 + r) % 1000000007;
    }
    printf("%lld rounds of %lld numbers: total %lld, checksum %lld\n", (long long)rounds,
           (long long)count, (long long)total, (long long)checksum);
    return 0;
}
