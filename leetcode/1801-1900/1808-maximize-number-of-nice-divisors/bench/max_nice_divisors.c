// LeetCode #1808: Maximize Number of Nice Divisors -- the bench in C: the ★
// arm over 2 * 10^6 calls, each count of prime factors drawn from the
// checksum so far.
#include <stdint.h>
#include <stdio.h>

#define MOD 1000000007LL

static int64_t power(int64_t base, int64_t exp) {
    int64_t result = 1;
    int64_t b = base % MOD;
    int64_t e = exp;
    while (e > 0) {
        if (e % 2 == 1) result = result * b % MOD;
        b = b * b % MOD;
        e /= 2;
    }
    return result;
}

static int32_t max_nice_divisors(int32_t prime_factors) {
    int64_t n = prime_factors;
    if (n <= 3) return prime_factors;
    int64_t answer;
    switch (n % 3) {
    case 0: answer = power(3, n / 3); break;
    case 1: answer = power(3, n / 3 - 1) * 4 % MOD; break;
    default: answer = power(3, n / 3) * 2 % MOD; break;
    }
    return (int32_t)answer;
}

int main(void) {
    int64_t check = 0;
    for (int64_t call = 0; call < 2000000; call++) {
        int64_t n = 1 + (check * 7919 + call) % 1000000000;
        check = (check * 31 + max_nice_divisors((int32_t)n)) % 1000000007;
    }
    printf("2000000 calls: checksum %lld\n", (long long)check);
    return 0;
}
