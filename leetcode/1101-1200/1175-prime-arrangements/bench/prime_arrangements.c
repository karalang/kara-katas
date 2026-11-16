// LeetCode #1175: Prime Arrangements -- the ★ arm's bench in C: a sieve of
// Eratosthenes over a calloc'd array counts the primes up to n (freed
// after each call, as the other languages' vectors are), and the answer is
// p! * (n - p)! modulo 10^9 + 7. The same million calls.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define MOD 1000000007LL

static int64_t factorial(int64_t k) {
    int64_t f = 1;
    for (int64_t i = 2; i <= k; i++) f = f * i % MOD;
    return f;
}

static int64_t num_prime_arrangements(int64_t n) {
    unsigned char *composite = calloc((size_t)n + 1, 1);
    int64_t primes = 0;
    for (int64_t i = 2; i <= n; i++) {
        if (!composite[i]) {
            primes++;
            for (int64_t j = i * i; j <= n; j += i) composite[j] = 1;
        }
    }
    free(composite);
    return factorial(primes) * factorial(n - primes) % MOD;
}

static int64_t seed = 1175;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int calls = 1000000;
    int64_t check = 0;
    for (int c = 0; c < calls; c++) {
        int64_t n = 1 + next_random() % 100;
        check = (check * 131 + num_prime_arrangements(n)) % 1000000007;
    }
    printf("%d calls: checksum %lld\n", calls, (long long)check);
    return 0;
}
