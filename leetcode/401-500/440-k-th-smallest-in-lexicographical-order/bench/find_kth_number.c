// Benchmark for #440: mirror of find_kth_number.kara (counting down the
// denary tree) on 1,000,000 random queries with n up to 10^9.
#include <stdint.h>
#include <stdio.h>

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

// The numbers in [1, n] that start with prefix.
static int64_t count_under(int64_t prefix, int64_t n) {
    int64_t count = 0;
    int64_t first = prefix;
    int64_t last = prefix;
    while (first <= n) {
        count += (n < last ? n : last) - first + 1;
        first *= 10;
        last = last * 10 + 9;
    }
    return count;
}

static int64_t find_kth_number(int64_t n, int64_t k) {
    int64_t current = 1;
    int64_t left = k - 1;
    while (left > 0) {
        int64_t under = count_under(current, n);
        if (under <= left) {
            left -= under;
            current += 1;
        } else {
            left -= 1;
            current *= 10;
        }
    }
    return current;
}

int main(void) {
    const int64_t queries = 1000000;
    int64_t seed = 440;
    int64_t total = 0, checksum = 0;
    for (int64_t q = 0; q < queries; q++) {
        int64_t a = next_random(&seed);
        int64_t n = 1 + (a * 32768 + next_random(&seed)) % 1000000000;
        int64_t b = next_random(&seed);
        int64_t k = 1 + (b * 32768 + next_random(&seed)) % n;
        int64_t x = find_kth_number(n, k);
        total += x;
        checksum = (checksum * 31 + x) % 1000000007;
    }
    printf("%lld queries with n up to 10^9: total %lld, checksum %lld\n", (long long)queries, (long long)total,
           (long long)checksum);
    return 0;
}
