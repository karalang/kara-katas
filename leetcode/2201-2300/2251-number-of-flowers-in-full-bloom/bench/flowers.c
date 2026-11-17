// LeetCode #2251: Number of Flowers in Full Bloom -- the benchmark's C
// mirror of flowers.kara: the starts and the ends sorted once, and each
// person the starts of at most t less the ends before t, by two binary
// searches.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 50000

static int64_t starts[N], ends[N], people[N], counts[N];

static int cmp_i64(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

// the first index whose value fails `values[i] <= x` (or `< x` if strict)
static int64_t partition(const int64_t *values, int64_t n, int64_t x, int strict) {
    int64_t lo = 0, hi = n;
    while (lo < hi) {
        int64_t mid = lo + (hi - lo) / 2;
        if (strict ? values[mid] < x : values[mid] <= x) lo = mid + 1; else hi = mid;
    }
    return lo;
}

static void full_bloom_flowers(int64_t f, int64_t p) {
    qsort(starts, f, sizeof(int64_t), cmp_i64);
    qsort(ends, f, sizeof(int64_t), cmp_i64);
    for (int64_t i = 0; i < p; i++)
        counts[i] = partition(starts, f, people[i], 0) - partition(ends, f, people[i], 1);
}

static int64_t seed = 2251;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide_random(void) {
    int64_t high = next_random();
    return high * 32768 + next_random();
}

int main(void) {
    int64_t check = 0;
    for (int t = 0; t < 20; t++) {
        for (int i = 0; i < N; i++) {
            int64_t a = wide_random() % 1000000000 + 1;
            int64_t b = wide_random() % 1000000000 + 1;
            starts[i] = a < b ? a : b;
            ends[i] = a < b ? b : a;
        }
        for (int i = 0; i < N; i++) people[i] = wide_random() % 1000000000 + 1;
        full_bloom_flowers(N, N);
        for (int i = 0; i < N; i++) check = (check * 31 + counts[i]) % 1000000007;
    }
    printf("20 cases of 5 * 10^4 flowers and people: checksum %lld\n", (long long)check);
    return 0;
}
