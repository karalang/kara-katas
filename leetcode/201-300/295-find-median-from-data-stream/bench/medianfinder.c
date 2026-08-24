/* LeetCode 295 benchmark lane — C mirror of medianfinder.kara.
 *
 * Same algorithm: two binary heaps meeting at the median, one max-heap over the
 * lower half and one min-heap over the upper half, with a `max` flag flipping
 * the comparison rather than negating values (matching the Kara version, which
 * avoids negation because -INT64_MIN overflows and Kara traps that). */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef struct { int64_t *data; int64_t len, cap; int max; } Heap;

static void heap_init(Heap *h, int max, int64_t cap) {
    h->data = malloc((size_t)cap * sizeof(int64_t));
    h->len = 0; h->cap = cap; h->max = max;
}

static inline int outranks(const Heap *h, int64_t a, int64_t b) {
    return h->max ? (a > b) : (a < b);
}

static void heap_push(Heap *h, int64_t v) {
    if (h->len == h->cap) { h->cap *= 2; h->data = realloc(h->data, (size_t)h->cap * sizeof(int64_t)); }
    h->data[h->len++] = v;
    int64_t i = h->len - 1;
    while (i > 0) {
        int64_t parent = (i - 1) / 2;
        if (!outranks(h, h->data[i], h->data[parent])) break;
        int64_t t = h->data[i]; h->data[i] = h->data[parent]; h->data[parent] = t;
        i = parent;
    }
}

static int64_t heap_pop(Heap *h) {
    int64_t top = h->data[0];
    int64_t last = h->data[--h->len];
    if (h->len > 0) {
        h->data[0] = last;
        int64_t i = 0, n = h->len;
        for (;;) {
            int64_t l = 2 * i + 1, r = l + 1, best = i;
            if (l < n && outranks(h, h->data[l], h->data[best])) best = l;
            if (r < n && outranks(h, h->data[r], h->data[best])) best = r;
            if (best == i) break;
            int64_t t = h->data[i]; h->data[i] = h->data[best]; h->data[best] = t;
            i = best;
        }
    }
    return top;
}

int main(void) {
    const int64_t n = 2000000;
    Heap lo, hi;
    heap_init(&lo, 1, 1024);
    heap_init(&hi, 0, 1024);

    int64_t state = 12345, checksum = 0;
    for (int64_t i = 0; i < n; i++) {
        state = (state * 1103515245 + 12345) & 0x7fffffff;
        int64_t v = state % 1000003 - 500000;

        heap_push(&lo, v);
        heap_push(&hi, heap_pop(&lo));
        if (hi.len > lo.len) heap_push(&lo, heap_pop(&hi));

        int64_t twice = (lo.len > hi.len) ? 2 * lo.data[0] : lo.data[0] + hi.data[0];
        checksum = (checksum * 31 + twice) % 1000000007;
    }

    printf("adds %lld checksum %lld\n", (long long)n, (long long)checksum);
    free(lo.data); free(hi.data);
    return 0;
}
