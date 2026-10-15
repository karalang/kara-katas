// LeetCode #686: Repeated String Match -- Knuth-Morris-Pratt. Bench.
//
// 100 pairs are built once: `a` of 1,000 to 10,000 letters over two
// letters, and `b` of 10,000 cut from the repetition of `a`, half of
// them with the last letter changed. Then 30 rounds answer every pair.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t repeated_string_match(const uint8_t *x, int64_t n, const uint8_t *y, int64_t m) {
    int64_t *fail = calloc((size_t)m, sizeof(int64_t));
    int64_t k = 0;
    for (int64_t i = 1; i < m; i++) {
        while (k > 0 && y[i] != y[k]) {
            k = fail[k - 1];
        }
        if (y[i] == y[k]) {
            k++;
        }
        fail[i] = k;
    }
    int64_t out = -1;
    int64_t j = 0;
    for (int64_t i = 0; i < n + m; i++) {
        uint8_t c = x[i % n];
        while (j > 0 && c != y[j]) {
            j = fail[j - 1];
        }
        if (c == y[j]) {
            j++;
        }
        if (j == m) {
            out = (i + 1 + n - 1) / n;
            break;
        }
    }
    free(fail);
    return out;
}

static int64_t seed = 686;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t count = 100, rounds = 30, m = 10000;
    uint8_t *firsts[100];
    int64_t lens[100];
    uint8_t *seconds[100];
    for (int64_t c = 0; c < count; c++) {
        int64_t n = 1000 + next_random() % 9001;
        uint8_t *a = malloc((size_t)n);
        for (int64_t i = 0; i < n; i++) {
            a[i] = (uint8_t)(97 + next_random() % 2);
        }
        int64_t start = next_random() % n;
        uint8_t *b = malloc((size_t)m);
        for (int64_t i = 0; i < m; i++) {
            b[i] = a[(start + i) % n];
        }
        if (c % 2 == 1) {
            b[m - 1] = (uint8_t)(196 - b[m - 1]);
        }
        firsts[c] = a;
        lens[c] = n;
        seconds[c] = b;
    }
    int64_t sum = 0, none = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t c = 0; c < count; c++) {
            int64_t k = repeated_string_match(firsts[c], lens[c], seconds[c], m);
            if (k == -1) {
                none++;
            }
            sum = (sum * 31 + k + r + 2) % 1000000007;
        }
    }
    printf("%lld pairs answered: %lld with no answer, checksum %lld\n", (long long)(count * rounds), (long long)none, (long long)sum);
    for (int64_t c = 0; c < count; c++) {
        free(firsts[c]);
        free(seconds[c]);
    }
    return 0;
}
