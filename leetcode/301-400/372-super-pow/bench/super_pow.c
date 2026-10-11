// Benchmark for #372 -- mirror of super_pow.kara.
#include <stdint.h>
#include <stdio.h>

#define MODULUS 1337

static int64_t pow_mod(int64_t base, int64_t exp) {
    int64_t out = 1;
    for (int64_t i = 0; i < exp; i++) out = out * base % MODULUS;
    return out;
}

static int64_t super_pow(int64_t a, const int64_t *b, int n) {
    int64_t base = a % MODULUS, out = 1;
    for (int i = 0; i < n; i++) out = pow_mod(out, 10) * pow_mod(base, b[i]) % MODULUS;
    return out;
}

int main(void) {
    int64_t seed = 372, checksum = 0;
    static int64_t b[2000];
    for (int r = 0; r < 500; r++) {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int64_t high = seed / 65536;
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int64_t a = 1 + (high * 65536 + seed / 32768) % 2147483647;
        for (int k = 0; k < 2000; k++) {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            int64_t d = (seed / 65536) % 10;
            b[k] = (k == 0 && d == 0) ? 1 : d;
        }
        checksum = (checksum * 1337 + super_pow(a, b, 2000)) % 1000000007;
    }
    printf("checksum %lld\n", (long long)checksum);
    return 0;
}
