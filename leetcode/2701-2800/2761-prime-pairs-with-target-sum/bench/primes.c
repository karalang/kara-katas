// LeetCode #2761: Prime Pairs With Target Sum -- the bench (primes.kara in
// C): a sieve of Eratosthenes up to n, then each x up to n / 2 with x and
// n - x both prime, the pairs written into an array.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// writes the smaller of each pair into `firsts` and returns how many
static int64_t find_prime_pairs(int64_t n, int64_t *firsts) {
    bool *prime = malloc((size_t)n + 1);
    for (int64_t i = 0; i <= n; i++) prime[i] = true;
    prime[0] = false;
    if (n >= 1) prime[1] = false;
    for (int64_t p = 2; p * p <= n; p++)
        if (prime[p])
            for (int64_t m = p * p; m <= n; m += p) prime[m] = false;
    int64_t count = 0;
    for (int64_t x = 2; x <= n / 2; x++)
        if (prime[x] && prime[n - x]) firsts[count++] = x;
    free(prime);
    return count;
}

static int64_t seed = 2761;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int count = 20, rounds = 3;
    int64_t targets[20];
    for (int k = 0; k < count; k++) {
        int64_t hi = next_random();
        targets[k] = (hi * 32768 + next_random()) % 100000 + 900001;
    }
    int64_t *firsts = malloc(sizeof(int64_t) * 500001);
    int64_t pairs_seen = 0, check = 0;
    for (int r = 0; r < rounds; r++)
        for (int k = 0; k < count; k++) {
            int64_t m = find_prime_pairs(targets[k], firsts);
            pairs_seen += m;
            check = (check * 31 + m + r) % 1000000007;
            for (int64_t i = 0; i < m; i++) check = (check * 31 + firsts[i]) % 1000000007;
        }
    printf("%d n near 10^6, %d rounds: %lld pairs, checksum %lld\n", count, rounds, (long long)pairs_seen, (long long)check);
    free(firsts);
    return 0;
}
