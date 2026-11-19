// LeetCode #1642: Furthest Building You Can Reach -- the bench's C mirror:
// the ★ arm on 50 random rows of 100000 buildings up to 10^4 high, each
// with up to 10^9 bricks and up to 5000 ladders, all drawn first, with a
// binary min-heap written out.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

enum { ROWS = 50, N = 100000 };

typedef struct {
    int32_t *items;
    size_t len, cap;
} Heap;

static void heap_push(Heap *h, int32_t x) {
    if (h->len == h->cap) {
        h->cap = h->cap ? 2 * h->cap : 64;
        h->items = realloc(h->items, sizeof(int32_t) * h->cap);
    }
    size_t i = h->len++;
    while (i > 0) {
        size_t p = (i - 1) / 2;
        if (h->items[p] <= x) break;
        h->items[i] = h->items[p];
        i = p;
    }
    h->items[i] = x;
}

static int32_t heap_pop(Heap *h) {
    int32_t top = h->items[0], last = h->items[--h->len];
    size_t i = 0;
    for (;;) {
        size_t l = 2 * i + 1, r = l + 1, m = i;
        int32_t best = last;
        if (l < h->len && h->items[l] < best) m = l, best = h->items[l];
        if (r < h->len && h->items[r] < best) m = r;
        if (m == i) break;
        h->items[i] = h->items[m];
        i = m;
    }
    if (h->len > 0) h->items[i] = last;
    return top;
}

static int64_t furthest_building(const int32_t *heights, size_t n, int32_t bricks, int32_t ladders) {
    Heap laddered = {NULL, 0, 0};
    int64_t answer = (int64_t)n - 1;
    for (size_t i = 1; i < n; i++) {
        int32_t climb = heights[i] - heights[i - 1];
        if (climb <= 0) continue;
        heap_push(&laddered, climb);
        if ((int64_t)laddered.len > ladders) {
            bricks -= heap_pop(&laddered);
            if (bricks < 0) {
                answer = (int64_t)i - 1;
                break;
            }
        }
    }
    free(laddered.items);
    return answer;
}

static int64_t seed = 1642;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    static int32_t heights[ROWS][N];
    int32_t bricks[ROWS], ladders[ROWS];
    for (int r = 0; r < ROWS; r++) {
        for (int i = 0; i < N; i++) heights[r][i] = (int32_t)(next_random() % 10000 + 1);
        bricks[r] = (int32_t)((next_random() * 32768 + next_random()) % 1000000001);
        ladders[r] = (int32_t)(next_random() % 5001);
    }
    int64_t check = 0, total = 0;
    for (int r = 0; r < ROWS; r++) {
        int64_t furthest = furthest_building(heights[r], N, bricks[r], ladders[r]);
        total += furthest;
        check = (check * 31 + furthest + 1) % 1000000007;
    }
    printf("50 rows of 100000 buildings: indices sum to %lld, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
