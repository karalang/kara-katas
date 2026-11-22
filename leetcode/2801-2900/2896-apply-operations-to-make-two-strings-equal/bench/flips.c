// LeetCode #2896: Apply Operations to Make Two Strings Equal -- the bench, as
// flips.kara: 5000 pairs of 500 characters, each answered 20 times by
// the pairing arm,
// its work arrays allocated per call as the other languages do.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t min_operations(const char *s1, const char *s2, int64_t n, int64_t x) {
    int64_t *places = malloc(n * sizeof *places);
    int64_t m = 0;
    for (int64_t i = 0; i < n; i++)
        if (s1[i] != s2[i]) places[m++] = i;
    if (m % 2 == 1) {
        free(places);
        return -1;
    }
    int64_t *doubled = malloc((m + 1) * sizeof *doubled);
    doubled[0] = 0;
    for (int64_t i = 1; i <= m; i++) {
        doubled[i] = doubled[i - 1] + x;
        if (i >= 2) {
            int64_t pair = doubled[i - 2] + 2 * (places[i - 1] - places[i - 2]);
            if (pair < doubled[i]) doubled[i] = pair;
        }
    }
    int64_t cost = doubled[m] / 2;
    free(places);
    free(doubled);
    return cost;
}

static int64_t seed = 2896;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    const int64_t count = 5000, rounds = 20, n = 500;
    char *s1 = malloc(count * n), *s2 = malloc(count * n);
    int64_t *xs = malloc(count * sizeof *xs);
    for (int64_t c = 0; c < count; c++) {
        xs[c] = next_random() % 500 + 1;
        char *a = s1 + c * n, *b = s2 + c * n;
        for (int64_t i = 0; i < n; i++) a[i] = next_random() % 2 == 0 ? '0' : '1';
        if (c % 2 == 0) {
            for (int64_t i = 0; i < n; i++) b[i] = next_random() % 2 == 0 ? '0' : '1';
        } else {
            for (int64_t i = 0; i < n; i++) b[i] = a[i];
            int64_t flips = next_random() % 20;
            for (int64_t k = 0; k < flips; k++) {
                int64_t at = next_random() % n;
                b[at] = b[at] == '0' ? '1' : '0';
            }
        }
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t c = 0; c < count; c++) {
            int64_t cost = min_operations(s1 + c * n, s2 + c * n, n, xs[c]);
            total += cost;
            check = (check * 31 + cost + 1 + r) % 1000000007;
        }
    }
    printf("%lld pairs of %lld, %lld rounds: costs total %lld, checksum %lld\n", (long long)count, (long long)n,
           (long long)rounds, (long long)total, (long long)check);
    free(s1);
    free(s2);
    free(xs);
    return 0;
}
