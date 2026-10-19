// LeetCode 790 — Domino and Tromino Tiling: the bench, in C.
// Mirrors num_tilings.kara: two growing tables of counts, full and
// ragged ends, for 300,000 random n.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t num_tilings(int64_t n) {
    const int64_t modulus = 1000000007;
    int64_t size = n + 1 < 2 ? 2 : n + 1;
    int64_t *full = malloc(size * sizeof *full);
    int64_t *ragged = malloc(size * sizeof *ragged);
    full[0] = 1, full[1] = 1;
    ragged[0] = 0, ragged[1] = 1;
    for (int64_t i = 2; i <= n; i++) {
        full[i] = (full[i - 1] + full[i - 2] + 2 * ragged[i - 2]) % modulus;
        ragged[i] = (ragged[i - 1] + full[i - 1]) % modulus;
    }
    int64_t answer = full[n];
    free(full);
    free(ragged);
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 790, rounds = 300000, sum = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t n = 1 + next_random(&seed) % 1000;
        int64_t ways = num_tilings(n);
        sum = (sum + ways) % 1000000007;
        check = (check * 31 + ways) % 1000000007;
    }
    printf("%lld rounds of n up to 1000: answers sum to %lld, checksum %lld\n", (long long)rounds, (long long)sum,
           (long long)check);
    return 0;
}
