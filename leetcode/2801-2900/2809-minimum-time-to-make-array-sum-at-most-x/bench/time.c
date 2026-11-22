// LeetCode #2809: Minimum Time to Make Array Sum At Most x -- the bench in
// C: the ★ arm over 20 cases of 1000 pairs, nums1 up to 1000 and nums2 up
// to 2, x from 3 * 10^5 to 5 * 10^5, all drawn first, then each answered
// 20 times; the pairs sorted by qsort on (nums2, nums1), as the tuples
// sort elsewhere.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define COUNT 20
#define N 1000

static int64_t seed = 2809;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}
static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

typedef struct {
    int64_t b, a;
} Pair;

static int by_pair(const void *p, const void *q) {
    const Pair *x = p, *y = q;
    if (x->b != y->b) return x->b < y->b ? -1 : 1;
    if (x->a != y->a) return x->a < y->a ? -1 : 1;
    return 0;
}

static int64_t minimum_time(const int64_t *nums1, const int64_t *nums2, int64_t n, int64_t x) {
    Pair pairs[N];
    int64_t best[N + 1];
    for (int64_t i = 0; i < n; i++) {
        pairs[i].b = nums2[i];
        pairs[i].a = nums1[i];
    }
    qsort(pairs, n, sizeof(Pair), by_pair);
    for (int64_t j = 0; j <= n; j++) best[j] = 0;
    for (int64_t i = 0; i < n; i++) {
        for (int64_t j = i + 1; j >= 1; j--) {
            int64_t take = best[j - 1] + pairs[i].a + j * pairs[i].b;
            if (take > best[j]) best[j] = take;
        }
    }
    int64_t sum1 = 0, sum2 = 0;
    for (int64_t i = 0; i < n; i++) {
        sum1 += nums1[i];
        sum2 += nums2[i];
    }
    for (int64_t t = 0; t <= n; t++)
        if (sum1 + t * sum2 - best[t] <= x) return t;
    return -1;
}

static int64_t nums1_[COUNT][N], nums2_[COUNT][N], xs[COUNT];

int main(void) {
    int rounds = 20;
    for (int c = 0; c < COUNT; c++) {
        for (int i = 0; i < N; i++) nums1_[c][i] = next_random() % 1001;
        for (int i = 0; i < N; i++) nums2_[c][i] = next_random() % 3;
        xs[c] = 300000 + wide() % 200000;
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int c = 0; c < COUNT; c++) {
            int64_t a = minimum_time(nums1_[c], nums2_[c], N, xs[c]);
            total += a;
            check = (check * 31 + a + 1 + r) % 1000000007;
        }
    }
    printf("%d cases of 1000 pairs, %d rounds: times sum to %lld, checksum %lld\n", COUNT, rounds, (long long)total, (long long)check);
    return 0;
}
