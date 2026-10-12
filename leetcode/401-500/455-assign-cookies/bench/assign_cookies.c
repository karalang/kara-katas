// Benchmark for #455: mirror of assign_cookies.kara (the ★ arm, both
// sorted, least greedy child first) on the same workload.
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int by_value(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a;
    int64_t y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int64_t find_content_children(const int64_t *g, int64_t n, const int64_t *s, int64_t m) {
    int64_t *greed = malloc(n * sizeof(int64_t));
    memcpy(greed, g, n * sizeof(int64_t));
    qsort(greed, n, sizeof(int64_t), by_value);
    int64_t *sizes = malloc(m * sizeof(int64_t));
    memcpy(sizes, s, m * sizeof(int64_t));
    qsort(sizes, m, sizeof(int64_t), by_value);
    int64_t child = 0;
    for (int64_t i = 0; i < m; i++) {
        if (child < n && sizes[i] >= greed[child]) {
            child += 1;
        }
    }
    free(greed);
    free(sizes);
    return child;
}

// ---- benchmark --------------------------------------------------------

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t random_value(int64_t *seed) {
    int64_t hi = next_random(seed);
    int64_t lo = next_random(seed);
    return 1 + (hi * 65536 + lo) % 1000000000;
}

int main(void) {
    const int64_t n = 1000000;
    const int64_t rounds = 10;
    int64_t seed = 455;
    int64_t *g = malloc(n * sizeof(int64_t));
    int64_t *s = malloc(n * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) {
        g[i] = random_value(&seed);
        s[i] = random_value(&seed);
    }
    int64_t total = 0;
    int64_t checksum = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t hi = next_random(&seed);
        int64_t lo = next_random(&seed);
        g[(hi * 65536 + lo) % n] = random_value(&seed);
        hi = next_random(&seed);
        lo = next_random(&seed);
        s[(hi * 65536 + lo) % n] = random_value(&seed);
        int64_t fed = find_content_children(g, n, s, n);
        total += fed;
        checksum = (checksum * 31 + fed) % 1000000007;
    }
    printf("%" PRId64 " rounds on %" PRId64 " children and %" PRId64 " cookies: %" PRId64 " content, checksum %" PRId64
           "\n",
           rounds, n, n, total, checksum);
    free(g);
    free(s);
    return 0;
}
