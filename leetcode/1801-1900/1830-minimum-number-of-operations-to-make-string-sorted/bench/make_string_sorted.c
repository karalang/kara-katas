// LeetCode #1830: Minimum Number of Operations to Make String Sorted -- the
// bench in C: the ★ arm over 500 calls on runs of 1500 to 2999 letters cut
// from one string of 4500 random letters, built once, each run's start and
// length drawn from the checksum so far. Each call makes its run a string of
// its own.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MOD 1000000007LL

static int64_t power(int64_t base, int64_t exp) {
    int64_t result = 1, b = base % MOD, e = exp;
    while (e > 0) {
        if (e % 2 == 1) result = result * b % MOD;
        b = b * b % MOD;
        e /= 2;
    }
    return result;
}

static int64_t make_string_sorted(const char *s, int64_t n) {
    int64_t *fact = malloc((size_t)(n + 1) * sizeof(int64_t)), *inverse = malloc((size_t)(n + 1) * sizeof(int64_t));
    fact[0] = 1;
    for (int64_t i = 1; i <= n; i++) fact[i] = fact[i - 1] * i % MOD;
    inverse[n] = power(fact[n], MOD - 2);
    for (int64_t i = n - 1; i >= 0; i--) inverse[i] = inverse[i + 1] * (i + 1) % MOD;
    int64_t count[26] = {0};
    int64_t operations = 0;
    for (int64_t i = n - 1; i >= 0; i--) {
        int64_t c = s[i] - 'a';
        count[c]++;
        int64_t smaller = 0;
        for (int64_t k = 0; k < c; k++) smaller += count[k];
        int64_t ways = fact[n - 1 - i] * smaller % MOD;
        for (int k = 0; k < 26; k++) ways = ways * inverse[count[k]] % MOD;
        operations = (operations + ways) % MOD;
    }
    free(fact);
    free(inverse);
    return operations;
}

static int64_t seed = 1830;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    char letters[4500];
    for (int i = 0; i < 4500; i++) letters[i] = (char)('a' + next_random() % 26);
    int64_t check = 0;
    for (int64_t call = 0; call < 500; call++) {
        int64_t start = (check + call) % 1500;
        int64_t len = 1500 + (check * 7 + call) % 1500;
        char *s = malloc((size_t)len + 1);
        memcpy(s, letters + start, (size_t)len);
        s[len] = 0;
        check = (check * 31 + make_string_sorted(s, len)) % 1000000007;
        free(s);
    }
    printf("500 calls: checksum %lld\n", (long long)check);
    return 0;
}
