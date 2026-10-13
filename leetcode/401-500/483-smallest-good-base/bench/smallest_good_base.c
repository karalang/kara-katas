// Benchmark for #483: C mirror of the ★ arm (the most 1s first, a float
// root); see smallest_good_base.kara. The number goes in and out as
// text, as in the problem's signature: strtoll in, snprintf out.
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

static int is_ones(long long n, long long k, long long m) {
    long long sum = 1, term = 1;
    for (long long i = 1; i < m; i++) {
        if (term > (n - sum) / k) {
            return 0;
        }
        term *= k;
        sum += term;
    }
    return sum == n;
}

static void smallest_good_base(const char *n, char *out, size_t size) {
    long long value = strtoll(n, NULL, 10);
    for (long long m = 63; m >= 3; m--) {
        long long root = (long long)pow((double)value, 1.0 / (double)(m - 1));
        for (long long k = root; k < root + 2; k++) {
            if (k >= 2 && is_ones(value, k, m)) {
                snprintf(out, size, "%lld", k);
                return;
            }
        }
    }
    snprintf(out, size, "%lld", value - 1);
}

int main(void) {
    long long count = 50000, total = 0, checksum = 0;
    char in[32], out[32];
    for (long long i = 0; i < count; i++) {
        long long n = 1000000000000000000LL - 7 * i;
        if (i % 3 == 2) {
            long long k = 2 + i / 3, m = 3 + (i / 3) % 6, term = 1;
            n = 1;
            for (long long j = 1; j < m; j++) {
                if (term > (1000000000000000000LL - n) / k) {
                    break;
                }
                term *= k;
                n += term;
            }
        }
        snprintf(in, sizeof in, "%lld", n);
        smallest_good_base(in, out, sizeof out);
        long long base = strtoll(out, NULL, 10);
        total += base % 1000;
        checksum = (checksum * 31 + base % 1000000007) % 1000000007;
    }
    printf("%lld values: bases add up to %lld (mod 1000 each), checksum %lld\n", count, total, checksum);
    return 0;
}
