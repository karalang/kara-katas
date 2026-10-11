// Benchmark for #365 -- mirror of water_jug.kara.
#include <stdint.h>
#include <stdio.h>

static int64_t gcd(int64_t a, int64_t b) { return b == 0 ? a : gcd(b, a % b); }

static int can_measure_water(int64_t x, int64_t y, int64_t target) {
    return target <= x + y && target % gcd(x, y) == 0;
}

int main(void) {
    int64_t seed = 365, yes = 0, checksum = 0;
    for (int64_t i = 0; i < 5000000; i++) {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int64_t x = 1 + (seed / 65536) % 1000000;
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int64_t y = 1 + (seed / 65536) % 1000000;
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int64_t target = ((seed / 65536) % 1000) * (1 + i % 6);
        if (can_measure_water(x, y, target)) {
            yes++;
            checksum = (checksum * 31 + i) % 1000000007;
        }
    }
    printf("%lld measurable, checksum %lld\n", (long long)yes, (long long)checksum);
    return 0;
}
