// LeetCode #2386: Find the K-Sum of an Array -- the bench, the ★ arm in
// C: the largest sum less the (k-1)-th smallest nonempty sum of the
// sorted sizes, walked from the smallest by a heap of (sum, last place).

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t sum, last;
} Entry;

static int less(Entry a, Entry b) { return a.sum < b.sum || (a.sum == b.sum && a.last < b.last); }

static void heap_push(Entry *h, int64_t *n, Entry e) {
    int64_t i = (*n)++;
    h[i] = e;
    while (i > 0) {
        int64_t p = (i - 1) / 2;
        if (!less(h[i], h[p])) break;
        Entry t = h[i];
        h[i] = h[p];
        h[p] = t;
        i = p;
    }
}

static Entry heap_pop(Entry *h, int64_t *n) {
    Entry top = h[0];
    h[0] = h[--(*n)];
    int64_t i = 0;
    for (;;) {
        int64_t l = 2 * i + 1, r = l + 1, m = i;
        if (l < *n && less(h[l], h[m])) m = l;
        if (r < *n && less(h[r], h[m])) m = r;
        if (m == i) break;
        Entry t = h[i];
        h[i] = h[m];
        h[m] = t;
        i = m;
    }
    return top;
}

static int cmp(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int64_t k_sum(const int64_t *nums, int64_t n, int64_t k) {
    int64_t largest = 0;
    int64_t *sizes = malloc(sizeof(int64_t) * n);
    for (int64_t i = 0; i < n; i++) {
        if (nums[i] > 0) largest += nums[i];
        sizes[i] = nums[i] < 0 ? -nums[i] : nums[i];
    }
    qsort(sizes, n, sizeof(int64_t), cmp);
    Entry *heap = malloc(sizeof(Entry) * (2 * k + 2));
    int64_t count = 0;
    heap_push(heap, &count, (Entry){sizes[0], 0});
    int64_t lost = 0;
    for (int64_t step = 1; step < k; step++) {
        Entry e = heap_pop(heap, &count);
        lost = e.sum;
        if (e.last + 1 < n) {
            heap_push(heap, &count, (Entry){e.sum + sizes[e.last + 1], e.last + 1});
            heap_push(heap, &count, (Entry){e.sum - sizes[e.last] + sizes[e.last + 1], e.last + 1});
        }
    }
    free(heap);
    free(sizes);
    return largest - lost;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t wide(int64_t *seed) {
    int64_t high = next_random(seed);
    return high * 32768 + next_random(seed);
}

static int64_t arrays[10][100000];

int main(void) {
    // 10 arrays of 10^5 values from -10^9 to 10^9; pass p asks array a for
    // k = 2000 - (7 p + a) % 100
    int64_t seed = 2386;
    for (int a = 0; a < 10; a++) {
        for (int i = 0; i < 100000; i++) {
            arrays[a][i] = wide(&seed) % 2000000001 - 1000000000;
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 60; p++) {
        for (int64_t a = 0; a < 10; a++) {
            int64_t answer = k_sum(arrays[a], 100000, 2000 - (7 * p + a) % 100);
            check = (check * 31 + answer % 1000000007 + 1000000007 + p) % 1000000007;
        }
    }
    printf("60 passes over 10 arrays of 10^5 values: checksum %lld\n", (long long)check);
    return 0;
}
