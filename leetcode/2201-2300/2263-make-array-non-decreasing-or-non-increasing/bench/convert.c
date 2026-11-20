// LeetCode #2263: Make Array Non-decreasing or Non-increasing -- C mirror
// of the ★ arm (convert.kara): the slope trick on a binary max-heap in an
// array, forwards and over the reversed array, the smaller cost. Output
// is byte-identical to convert.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t *v;
    int len;
} Heap;

static void heap_push(Heap *h, int64_t x) {
    int i = h->len++;
    h->v[i] = x;
    while (i > 0) {
        int p = (i - 1) / 2;
        if (h->v[p] >= h->v[i]) break;
        int64_t t = h->v[p]; h->v[p] = h->v[i]; h->v[i] = t;
        i = p;
    }
}

static int64_t heap_pop(Heap *h) {
    int64_t top = h->v[0];
    h->v[0] = h->v[--h->len];
    int i = 0;
    for (;;) {
        int l = 2 * i + 1, r = l + 1, m = i;
        if (l < h->len && h->v[l] > h->v[m]) m = l;
        if (r < h->len && h->v[r] > h->v[m]) m = r;
        if (m == i) break;
        int64_t t = h->v[m]; h->v[m] = h->v[i]; h->v[i] = t;
        i = m;
    }
    return top;
}

static int64_t nondecreasing_cost(const int64_t *nums, int n, int step) {
    Heap h = { malloc(sizeof(int64_t) * 2 * n), 0 };
    int64_t cost = 0;
    for (int k = 0; k < n; k++) {
        int64_t x = nums[step > 0 ? k : n - 1 - k];
        heap_push(&h, x);
        if (h.v[0] > x) {
            cost += heap_pop(&h) - x;
            heap_push(&h, x);
        }
    }
    free(h.v);
    return cost;
}

static int64_t convert_array(const int64_t *nums, int n) {
    int64_t up = nondecreasing_cost(nums, n, 1);
    int64_t down = nondecreasing_cost(nums, n, -1);
    return up < down ? up : down;
}

// ---- bench harness ---------------------------------------------------------

static int64_t seed = 2263;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int64_t check = 0;
    int64_t nums[1000];
    for (int t = 0; t < 400; t++) {
        for (int i = 0; i < 1000; i++) nums[i] = next_random() % 1001;
        check = (check * 31 + convert_array(nums, 1000)) % 1000000007;
    }
    printf("400 arrays of 1000: checksum %lld\n", (long long)check);
    return 0;
}
