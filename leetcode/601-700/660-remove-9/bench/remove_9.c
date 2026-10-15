// Benchmark for #660: base 9, read as base 10, as the Kara ★ arm.
#include <stdint.h>
#include <stdio.h>

static int64_t new_integer(int64_t n) {
    int64_t rest = n, place = 1, out = 0;
    while (rest > 0) {
        out += rest % 9 * place;
        rest /= 9;
        place *= 10;
    }
    return out;
}

int main(void) {
    int64_t count = 50000000, checksum = 0;
    for (int64_t i = 0; i < count; i++) {
        int64_t n = 1 + i * 16;
        checksum = (checksum * 31 + new_integer(n)) % 1000000007;
    }
    printf("%lld values of n: checksum %lld\n", (long long)count, (long long)checksum);
    return 0;
}
