// LeetCode #1354 bench -- C: the moves undone from the target, largest
// value first, in a binary max-heap with a running total, many undos of
// one value as one remainder.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t *heap;
static int64_t len;

static void push(int64_t v) {
    int64_t i = len++;
    heap[i] = v;
    while (i > 0) {
        int64_t p = (i - 1) / 2;
        if (heap[p] >= heap[i]) break;
        int64_t t = heap[p];
        heap[p] = heap[i];
        heap[i] = t;
        i = p;
    }
}

static int64_t pop(void) {
    int64_t top = heap[0];
    heap[0] = heap[--len];
    int64_t i = 0;
    for (;;) {
        int64_t l = 2 * i + 1, r = l + 1, m = i;
        if (l < len && heap[l] > heap[m]) m = l;
        if (r < len && heap[r] > heap[m]) m = r;
        if (m == i) break;
        int64_t t = heap[m];
        heap[m] = heap[i];
        heap[i] = t;
        i = m;
    }
    return top;
}

static int is_possible(const int32_t *target, int64_t n) {
    if (n == 1) return target[0] == 1;
    int64_t total = 0;
    len = 0;
    for (int64_t i = 0; i < n; i++) {
        total += target[i];
        push(target[i]);
    }
    for (;;) {
        int64_t x = pop();
        int64_t rest = total - x;
        if (x == 1 || rest == 1) return 1;
        if (x <= rest || x % rest == 0) return 0;
        int64_t before = x % rest;
        push(before);
        total = rest + before;
    }
}

static int64_t seed = 1354;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static void reached(int32_t *out, int64_t n, int64_t moves, int64_t top) {
    int64_t *arr = malloc(n * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) arr[i] = 1;
    int64_t total = n;
    for (int64_t m = 0; m < moves; m++) {
        if (total > top) break;
        int64_t i = next_random() % n;
        int64_t was = arr[i];
        arr[i] = total;
        total = 2 * total - was;
    }
    for (int64_t i = 0; i < n; i++) out[i] = (int32_t)arr[i];
    free(arr);
}

int main(void) {
    // 20 targets of 5 * 10^4 values, each reached from the ones by moves
    // until a value would pass 10^9, built once; then 2000 rounds, each
    // changing one place of one target, drawn from the checksum so far,
    // answering, and putting the place back; one round in four leaves the
    // value as it was
    enum { N = 50000, T = 20 };
    int32_t *targets = malloc((size_t)T * N * sizeof(int32_t));
    heap = malloc(N * sizeof(int64_t));
    for (int k = 0; k < T; k++) reached(targets + (int64_t)k * N, N, 100, 1000000000);
    int64_t check = 0;
    for (int64_t r = 0; r < 2000; r++) {
        int64_t k = check % 20;
        int64_t at = (check / 20) % N;
        int32_t *t = targets + k * N;
        int32_t was = t[at];
        if (r % 4 != 0) t[at] = was + 1 + (int32_t)((check / 7) % 3);
        int64_t got = is_possible(t, N) ? 1 : 0;
        t[at] = was;
        check = (check * 31 + got * 1000 + r) % 1000000007;
    }
    printf("2000 rounds over 20 targets of 5 * 10^4 values: checksum %lld\n", (long long)check);
    free(targets);
    free(heap);
    return 0;
}
