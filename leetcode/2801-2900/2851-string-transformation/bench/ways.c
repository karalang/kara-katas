// LeetCode #2851: String Transformation -- the bench: the ★ arm over 10
// pairs of 5 * 10^5 letters, LeetCode's most, each s a block of up to 8
// letters repeated, half of them with one letter changed, t a rotation
// of s two times in three and otherwise s with one letter changed, k up
// to about 10^15, all drawn first, then each answered 5 times. The
// strings are byte arrays; s + s and the prefix function are allocated
// afresh on each call, as the other languages' vectors are.
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

static int64_t number_of_ways(const unsigned char *s, const unsigned char *t, int64_t n, int64_t k) {
    unsigned char *text = malloc(2 * n);
    memcpy(text, s, n);
    memcpy(text + n, s, n);
    int64_t *fail = calloc(n, sizeof(int64_t));
    int64_t j = 0;
    for (int64_t i = 1; i < n; i++) {
        while (j > 0 && t[i] != t[j]) j = fail[j - 1];
        if (t[i] == t[j]) j++;
        fail[i] = j;
    }
    int64_t at_zero = 0, elsewhere = 0;
    j = 0;
    for (int64_t i = 0; i < 2 * n - 1; i++) {
        while (j > 0 && text[i] != t[j]) j = fail[j - 1];
        if (text[i] == t[j]) j++;
        if (j == n) {
            if (i + 1 == n) at_zero++;
            else elsewhere++;
            j = fail[j - 1];
        }
    }
    free(text);
    free(fail);
    int64_t all = power(n - 1, k);
    int64_t sign = k % 2 == 0 ? 1 : MOD - 1;
    int64_t inverse = power(n, MOD - 2);
    int64_t zero_ways = (all + (n - 1) * sign) % MOD * inverse % MOD;
    int64_t other_ways = (all - sign + MOD) % MOD * inverse % MOD;
    return (at_zero * zero_ways + elsewhere * other_ways) % MOD;
}

static int64_t seed = 2851;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}
static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

int main(void) {
    const int64_t count = 10, rounds = 5, n = 500000;
    unsigned char *ss[10], *ts[10];
    int64_t ks[10];
    for (int64_t c = 0; c < count; c++) {
        int64_t block = next_random() % 8 + 1;
        int64_t letters = next_random() % 3 + 1;
        unsigned char unit[8];
        for (int64_t i = 0; i < block; i++) unit[i] = 'a' + next_random() % letters;
        unsigned char *s = malloc(n);
        for (int64_t i = 0; i < n; i++) s[i] = unit[i % block];
        if (next_random() % 2 == 0) {
            int64_t at = wide() % n;
            s[at] = 'a' + next_random() % 3;
        }
        unsigned char *t = malloc(n);
        if (next_random() % 3 < 2) {
            int64_t r = wide() % n;
            memcpy(t, s + n - r, r);
            memcpy(t + r, s, n - r);
        } else {
            memcpy(t, s, n);
            int64_t at = wide() % n;
            t[at] = 'a' + (t[at] - 'a' + 1) % 3;
        }
        ks[c] = wide() * 900000 + 1;
        ss[c] = s;
        ts[c] = t;
    }
    int64_t check = 0;
    for (int64_t r = 0; r < rounds; r++)
        for (int64_t c = 0; c < count; c++)
            check = (check * 31 + number_of_ways(ss[c], ts[c], n, ks[c]) + r) % MOD;
    printf("%lld pairs of %lld, %lld rounds: checksum %lld\n", (long long)count, (long long)n, (long long)rounds, (long long)check);
    for (int64_t c = 0; c < count; c++) {
        free(ss[c]);
        free(ts[c]);
    }
    return 0;
}
