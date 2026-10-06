// Benchmark for #357 -- same workload and algorithm as unique_digits.kara.
#include <stdint.h>
#include <stdio.h>

static int64_t extend(int64_t len, int64_t n, int64_t base, int64_t used) {
    if (len == n) return 1;
    int64_t count = 1;
    for (int64_t d = 0; d < base; d++) {
        if (len == 0 && d == 0) continue;
        if ((used & ((int64_t)1 << d)) == 0)
            count += extend(len + 1, n, base, used | ((int64_t)1 << d));
    }
    return count;
}

int main(void) {
    int64_t checksum = 0;
    for (int64_t base = 2; base <= 11; base++) {
        int64_t count = extend(0, base, base, 0);
        checksum = (checksum * 31 + count) % 1000000007;
    }
    printf("bases 2 to 11: checksum %lld\n", (long long)checksum);
    return 0;
}
