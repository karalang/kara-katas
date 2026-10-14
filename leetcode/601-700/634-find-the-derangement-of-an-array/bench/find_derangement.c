/*
 * LeetCode 634 -- Find the Derangement of An Array, bench mirror in C.
 *
 * The ★ arm of find_derangement.kara: D(n) = (n - 1) * (D(n - 1) +
 * D(n - 2)) modulo 10^9 + 7, kept in two variables. Same values of n,
 * same output line.
 */
#include <stdint.h>
#include <stdio.h>

#define MOD 1000000007LL

static int64_t find_derangement(int64_t n) {
    int64_t before = 1, last = 0;
    for (int64_t i = 2; i < n + 1; i++) {
        int64_t next = (i - 1) * ((last + before) % MOD) % MOD;
        before = last;
        last = next;
    }
    return last;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 634;
    int64_t sizes[100];
    for (int i = 0; i < 100; i++) {
        int64_t wide = next_random(&seed) * 32768;
        wide += next_random(&seed);
        sizes[i] = 1 + wide % 1000000;
    }
    int64_t total = 0, checksum = 0;
    for (int i = 0; i < 100; i++) {
        int64_t d = find_derangement(sizes[i]);
        total = (total + d) % MOD;
        checksum = (checksum * 31 + d) % MOD;
    }
    printf("100 values of n: total %lld, checksum %lld\n", (long long)total, (long long)checksum);
    return 0;
}
