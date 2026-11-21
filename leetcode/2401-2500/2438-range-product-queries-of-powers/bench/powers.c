// LeetCode #2438: Range Product Queries of Powers -- the bench, the ★ arm:
// the exponents' prefix sums, and two to each range's sum by squaring
// modulo 10^9 + 7.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define MOD 1000000007LL

static int64_t power_of_two(int64_t exponent) {
    int64_t result = 1, base = 2, e = exponent;
    while (e > 0) {
        if (e % 2 == 1) result = result * base % MOD;
        base = base * base % MOD;
        e /= 2;
    }
    return result;
}

static int64_t *product_queries(int64_t n, int64_t **queries, int64_t q) {
    int64_t prefix[32];
    int64_t k = 0;
    prefix[0] = 0;
    for (int64_t bit = 0; bit < 31; bit++)
        if ((n >> bit) & 1) {
            prefix[k + 1] = prefix[k] + bit;
            k++;
        }
    int64_t *answers = malloc(q * sizeof(int64_t));
    for (int64_t i = 0; i < q; i++)
        answers[i] = power_of_two(prefix[queries[i][1] + 1] - prefix[queries[i][0]]);
    return answers;
}

static int64_t seed = 2438;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t count = 100, q = 10000;
    int64_t values[100];
    int64_t ***all = malloc(count * sizeof(int64_t **));
    for (int64_t c = 0; c < count; c++) {
        int64_t r = next_random();
        int64_t n = 1 + (r * 32768 + next_random()) % 1000000000;
        int64_t k = __builtin_popcountll((unsigned long long)n);
        all[c] = malloc(q * sizeof(int64_t *));
        for (int64_t i = 0; i < q; i++) {
            int64_t a = next_random() % k;
            int64_t b = next_random() % k;
            all[c][i] = malloc(2 * sizeof(int64_t));
            all[c][i][0] = a < b ? a : b;
            all[c][i][1] = a < b ? b : a;
        }
        values[c] = n;
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 10; p++)
        for (int64_t c = 0; c < count; c++) {
            int64_t *answers = product_queries(values[c], all[c], q);
            for (int64_t i = 0; i < q; i++) check = (check * 31 + answers[(i + p) % q] + p) % 1000000007;
            free(answers);
        }
    printf("10 passes over 100 values of 10^4 queries: checksum %lld\n", (long long)check);
    for (int64_t c = 0; c < count; c++) {
        for (int64_t i = 0; i < q; i++) free(all[c][i]);
        free(all[c]);
    }
    free(all);
    return 0;
}
