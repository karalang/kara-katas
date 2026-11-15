// LeetCode #2163: Minimum Difference in Sums After Removal of Elements --
// the benchmark's C mirror of difference.kara: a binary heap by hand, its
// order a sign, 1 for largest first and -1 for smallest first.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t *a;
    int64_t len, sign;
} Heap;

static void heap_push(Heap *h, int64_t x) {
    int64_t i = h->len++;
    h->a[i] = x;
    while (i > 0) {
        int64_t p = (i - 1) / 2;
        if (h->a[i] * h->sign <= h->a[p] * h->sign) break;
        int64_t t = h->a[i]; h->a[i] = h->a[p]; h->a[p] = t;
        i = p;
    }
}

static int64_t heap_pop(Heap *h) {
    int64_t top = h->a[0];
    h->a[0] = h->a[--h->len];
    int64_t i = 0;
    for (;;) {
        int64_t best = i;
        for (int64_t c = 2 * i + 1; c <= 2 * i + 2; c++) {
            if (c < h->len && h->a[c] * h->sign > h->a[best] * h->sign) best = c;
        }
        if (best == i) break;
        int64_t t = h->a[i]; h->a[i] = h->a[best]; h->a[best] = t;
        i = best;
    }
    return top;
}

static int64_t minimum_difference(const int64_t *nums, int64_t len, int64_t *heap_space, int64_t *left) {
    int64_t n = len / 3;
    Heap kept = {heap_space, 0, 1};
    int64_t sum = 0, count = 0;
    for (int64_t i = 0; i < 2 * n; i++) {
        heap_push(&kept, nums[i]);
        sum += nums[i];
        if (kept.len > n) sum -= heap_pop(&kept);
        if (i >= n - 1) left[count++] = sum;
    }
    kept.len = 0;
    kept.sign = -1;
    sum = 0;
    int64_t best = INT64_MAX;
    for (int64_t i = 3 * n - 1; i >= n; i--) {
        heap_push(&kept, nums[i]);
        sum += nums[i];
        if (kept.len > n) sum -= heap_pop(&kept);
        if (i <= 2 * n && left[i - n] - sum < best) best = left[i - n] - sum;
    }
    return best;
}

static int64_t seed = 2163;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide_random(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

int main(void) {
    enum { LEN = 300000 };
    static int64_t lists[4][LEN], copy[LEN], heap_space[LEN], left[LEN];
    for (int k = 0; k < 4; k++)
        for (int i = 0; i < LEN; i++) lists[k][i] = wide_random() % 100000 + 1;
    int64_t check = 0;
    for (int r = 0; r < 5; r++) {
        for (int k = 0; k < 4; k++) {
            int64_t at = wide_random() % LEN;
            lists[k][at] = wide_random() % 100000 + 1;
            memcpy(copy, lists[k], sizeof copy);
            int64_t d = minimum_difference(copy, LEN, heap_space, left);
            check = (check * 31 + d + 1000000000000LL) % 1000000007;
        }
    }
    printf("20 solves: checksum %lld\n", (long long)check);
    return 0;
}
