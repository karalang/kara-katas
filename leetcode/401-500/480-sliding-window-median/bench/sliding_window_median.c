// Benchmark for #480: C mirror of the ★ arm (two heaps, deletions put
// off); see sliding_window_median.kara. C has no heap or hash map, so
// both are written out: a binary min-heap (the low half stores negated
// values) and an open-addressing table of counts that never deletes.
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    long long *a;
    int len, cap;
} Heap;

static void heap_push(Heap *h, long long x) {
    if (h->len == h->cap) {
        h->cap = h->cap ? h->cap * 2 : 16;
        h->a = realloc(h->a, sizeof(long long) * h->cap);
    }
    int i = h->len++;
    while (i > 0) {
        int p = (i - 1) / 2;
        if (h->a[p] <= x) break;
        h->a[i] = h->a[p];
        i = p;
    }
    h->a[i] = x;
}

static long long heap_pop(Heap *h) {
    long long top = h->a[0];
    long long x = h->a[--h->len];
    int i = 0;
    for (;;) {
        int c = 2 * i + 1;
        if (c >= h->len) break;
        if (c + 1 < h->len && h->a[c + 1] < h->a[c]) c++;
        if (x <= h->a[c]) break;
        h->a[i] = h->a[c];
        i = c;
    }
    if (h->len > 0) h->a[i] = x;
    return top;
}

#define TABLE (1 << 22)
static long long keys[TABLE];
static long long counts[TABLE];
static char used[TABLE];

static long long *slot(long long key) {
    unsigned long long h = (unsigned long long)key * 0x9E3779B97F4A7C15ULL;
    unsigned i = (unsigned)(h >> 42) & (TABLE - 1);
    while (used[i] && keys[i] != key) i = (i + 1) & (TABLE - 1);
    if (!used[i]) {
        used[i] = 1;
        keys[i] = key;
        counts[i] = 0;
    }
    return &counts[i];
}

typedef struct {
    Heap low, high;
    long long low_size, high_size;
} Window;

static void prune(Window *w) {
    while (w->low.len > 0) {
        long long *left = slot(-w->low.a[0]);
        if (*left == 0) break;
        (*left)--;
        heap_pop(&w->low);
    }
    while (w->high.len > 0) {
        long long *left = slot(w->high.a[0]);
        if (*left == 0) break;
        (*left)--;
        heap_pop(&w->high);
    }
}

static void balance(Window *w) {
    if (w->low_size > w->high_size + 1) {
        heap_push(&w->high, -heap_pop(&w->low));
        w->low_size--;
        w->high_size++;
    } else if (w->low_size < w->high_size) {
        heap_push(&w->low, -heap_pop(&w->high));
        w->high_size--;
        w->low_size++;
    }
    prune(w);
}

static void add(Window *w, long long x) {
    if (w->low.len == 0 || x <= -w->low.a[0]) {
        heap_push(&w->low, -x);
        w->low_size++;
    } else {
        heap_push(&w->high, x);
        w->high_size++;
    }
    balance(w);
}

static void remove_one(Window *w, long long x) {
    int in_low = x <= -w->low.a[0];
    (*slot(x))++;
    if (in_low) w->low_size--; else w->high_size--;
    prune(w);
    balance(w);
}

static double median(Window *w, int k) {
    long long a = -w->low.a[0];
    if (k % 2 == 1) return (double)a;
    return (double)(a + w->high.a[0]) / 2.0;
}

static long long nums[1000000];
static long long seed = 480;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int n = 1000000;
    for (int i = 0; i < n; i++) {
        long long a = next_random();
        long long b = next_random();
        long long r = a * 32768 + b;
        nums[i] = r * 4 + next_random() % 4 - 2147483648LL;
    }
    long long windows = 0, checksum = 0;
    for (int k = 1000; k < 1002; k++) {
        Window w = {0};
        for (int i = 0; i < TABLE; i++) used[i] = 0;
        for (int i = 0; i < n; i++) {
            add(&w, nums[i]);
            if (i >= k) remove_one(&w, nums[i - k]);
            if (i >= k - 1) {
                double m = median(&w, k);
                windows++;
                checksum = (checksum * 31 + (long long)(m * 2.0) % 1000000007 + 1000000007) % 1000000007;
            }
        }
        free(w.low.a);
        free(w.high.a);
    }
    printf("%lld windows: checksum %lld\n", windows, checksum);
    return 0;
}
