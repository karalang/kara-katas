// LeetCode #2040: Kth Smallest Product of Two Sorted Arrays -- the ★ arm in
// C, the same algorithm and workload as product.kara: binary search on the
// answer, the products at most `x` counted by a hand-written partition
// point (the first index where the predicate fails).
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// first index of sorted `b` (length m) where `a * b[i] <= x` fails
static int64_t first_above(const int64_t *b, int64_t m, int64_t a, int64_t x) {
    int64_t lo = 0, hi = m;
    while (lo < hi) {
        int64_t mid = lo + (hi - lo) / 2;
        if (a * b[mid] <= x) lo = mid + 1; else hi = mid;
    }
    return lo;
}

// first index of sorted `b` where `a * b[i] > x` fails
static int64_t first_at_most(const int64_t *b, int64_t m, int64_t a, int64_t x) {
    int64_t lo = 0, hi = m;
    while (lo < hi) {
        int64_t mid = lo + (hi - lo) / 2;
        if (a * b[mid] > x) lo = mid + 1; else hi = mid;
    }
    return lo;
}

static int64_t count_at_most(const int64_t *a, int64_t n, const int64_t *b, int64_t m, int64_t x) {
    int64_t count = 0;
    for (int64_t i = 0; i < n; i++) {
        if (a[i] > 0) count += first_above(b, m, a[i], x);
        else if (a[i] < 0) count += m - first_at_most(b, m, a[i], x);
        else if (x >= 0) count += m;
    }
    return count;
}

static int64_t floor_half(int64_t v) { return v >= 0 ? v / 2 : -((-v + 1) / 2); }

static int64_t kth_smallest_product(const int64_t *a, int64_t n, const int64_t *b, int64_t m, int64_t k) {
    int64_t lo = -10000000000LL, hi = 10000000000LL;
    while (lo < hi) {
        int64_t mid = lo + floor_half(hi - lo);
        if (count_at_most(a, n, b, m, mid) >= k) hi = mid; else lo = mid + 1;
    }
    return lo;
}

static int64_t seed = 2040;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int cmp(const void *p, const void *q) {
    int64_t x = *(const int64_t *)p, y = *(const int64_t *)q;
    return (x > y) - (x < y);
}

static int64_t *sorted_values(int64_t n, int64_t top) {
    int64_t *v = malloc(sizeof(int64_t) * n);
    for (int64_t i = 0; i < n; i++) {
        int64_t hi = next_random();
        v[i] = (hi * 32768 + next_random()) % (2 * top + 1) - top;
    }
    qsort(v, n, sizeof(int64_t), cmp);
    return v;
}

int main(void) {
    const int64_t n = 50000;
    const int64_t tops[4] = {100000, 3, 1000, 100000};
    int64_t *as[4], *bs[4];
    for (int r = 0; r < 4; r++) {
        as[r] = sorted_values(n, tops[r]);
        bs[r] = sorted_values(n, tops[r]);
    }
    int64_t calls = 0, sum = 0, check = 0;
    for (int64_t round = 0; round < 3; round++) {
        for (int64_t r = 0; r < 4; r++) {
            int64_t k = (round * 4 + r + 1) * (n * n / 13) + 1;
            int64_t answer = kth_smallest_product(as[r], n, bs[r], n, k);
            calls++;
            sum += answer;
            int64_t m = answer % 1000000007;
            if (m < 0) m += 1000000007;
            check = (check * 31 + m) % 1000000007;
        }
    }
    printf("%lld calls: sum %lld, checksum %lld\n", (long long)calls, (long long)sum, (long long)check);
    for (int r = 0; r < 4; r++) { free(as[r]); free(bs[r]); }
    return 0;
}
