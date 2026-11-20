// LeetCode #1735: Count Ways to Make Array With Product -- the bench
// (ways.kara): the product over k's primes of C(n + e - 1, e), read off
// factorials and their inverses.

#include <stdio.h>
#include <stdlib.h>

#define MOD 1000000007L

static long power(long base, long exp) {
    long result = 1, b = base % MOD, e = exp;
    while (e > 0) {
        if (e % 2 == 1) result = result * b % MOD;
        b = b * b % MOD;
        e /= 2;
    }
    return result;
}

/* the answers, one per query, in a fresh allocation */
static int *ways_to_fill_array(const int (*queries)[2], long q) {
    long top = 0;
    for (long i = 0; i < q; i++)
        if (queries[i][0] > top) top = queries[i][0];
    top += 14;
    long *fact = malloc(sizeof(long) * (top + 1));
    long *inverse = malloc(sizeof(long) * (top + 1));
    fact[0] = 1;
    for (long i = 1; i <= top; i++) fact[i] = fact[i - 1] * i % MOD;
    inverse[top] = power(fact[top], MOD - 2);
    for (long i = top; i >= 1; i--) inverse[i - 1] = inverse[i] * i % MOD;
    int *answers = malloc(sizeof(int) * q);
    for (long i = 0; i < q; i++) {
        long n = queries[i][0], k = queries[i][1], ways = 1;
        for (long p = 2; p * p <= k; p++) {
            long e = 0;
            while (k % p == 0) {
                k /= p;
                e++;
            }
            long m = n + e - 1;
            ways = ways * (fact[m] * inverse[e] % MOD * inverse[m - e] % MOD) % MOD;
        }
        if (k > 1) ways = ways * n % MOD;
        answers[i] = (int)ways;
    }
    free(fact);
    free(inverse);
    return answers;
}

static long next_random(long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648L;
    return *seed / 65536;
}

int main(void) {
    int count = 10;
    long rounds = 60, q = 10000, seed = 1735;
    int (**problems)[2] = malloc(sizeof(*problems) * count);
    for (int p = 0; p < count; p++) {
        problems[p] = malloc(sizeof(int[2]) * q);
        for (long i = 0; i < q; i++) {
            problems[p][i][0] = (int)(next_random(&seed) % 10000 + 1);
            problems[p][i][1] = (int)(next_random(&seed) % 10000 + 1);
        }
    }
    long sum = 0, check = 0;
    for (long r = 0; r < rounds; r++) {
        for (int p = 0; p < count; p++) {
            int *answers = ways_to_fill_array((const int (*)[2])problems[p], q);
            sum += answers[0];
            check = (check * 31 + answers[0] + answers[q / 2] + answers[q - 1] + r) % 1000000007;
            free(answers);
        }
    }
    for (int p = 0; p < count; p++) free(problems[p]);
    free(problems);
    printf("%d lists of %ld queries, %ld rounds: first answers sum to %ld, checksum %ld\n", count, q, rounds, sum, check);
    return 0;
}
