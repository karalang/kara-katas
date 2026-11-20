// LeetCode #2400: Number of Ways to Reach a Position After Exactly k
// Steps -- the bench, the ★ arm in C: C(k, (k + d) / 2) from factorials
// modulo 10^9 + 7 and Fermat's inverse.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define MOD 1000000007LL

static int64_t seed = 2400;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t power(int64_t base, int64_t exponent) {
    int64_t result = 1, b = base % MOD;
    for (int64_t e = exponent; e > 0; e /= 2) {
        if (e % 2 == 1) result = result * b % MOD;
        b = b * b % MOD;
    }
    return result;
}

static int64_t number_of_ways(int64_t start_pos, int64_t end_pos, int64_t k) {
    int64_t d = end_pos > start_pos ? end_pos - start_pos : start_pos - end_pos;
    if (d > k || (k - d) % 2 == 1) return 0;
    int64_t toward = (k + d) / 2;
    int64_t *factorial = malloc((k + 1) * sizeof *factorial);
    factorial[0] = 1;
    for (int64_t i = 1; i <= k; i++) factorial[i] = factorial[i - 1] * i % MOD;
    int64_t w = factorial[k] * power(factorial[toward], MOD - 2) % MOD * power(factorial[k - toward], MOD - 2) % MOD;
    free(factorial);
    return w;
}

int main(void) {
    int64_t check = 0, zeros = 0;
    for (int q = 0; q < 300000; q++) {
        int64_t k = 1 + next_random() % 1000;
        int64_t start = 1 + next_random() % 1000;
        int64_t end = start - k + 2 * (next_random() % (k + 1));
        if (end < 1) end = 1;
        if (end > 1000) end = 1000;
        int64_t w = number_of_ways(start, end, k);
        if (w == 0) zeros++;
        check = (check * 31 + w) % MOD;
    }
    printf("300000 queries of k up to 1000: checksum %lld, %lld zeros\n", (long long)check, (long long)zeros);
    return 0;
}
