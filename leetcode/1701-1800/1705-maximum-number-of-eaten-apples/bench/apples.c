// LeetCode #1705: Maximum Number of Eaten Apples -- the bench's C mirror:
// the ★ arm on 50 random trees of 20000 days, all drawn first, each
// answered 10 times.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define COUNT 50
#define ROUNDS 10
#define N 20000

typedef struct {
    int64_t rot;
    int32_t left;
} Crop;

static int less(Crop a, Crop b) {
    return a.rot < b.rot || (a.rot == b.rot && a.left < b.left);
}

// a binary min-heap of crops, by (rotting day, apples left)
typedef struct {
    Crop *items;
    int64_t len, cap;
} Heap;

static void heap_push(Heap *h, Crop c) {
    if (h->len == h->cap) {
        h->cap = h->cap ? h->cap * 2 : 16;
        h->items = realloc(h->items, (size_t)h->cap * sizeof *h->items);
    }
    int64_t i = h->len++;
    h->items[i] = c;
    while (i > 0) {
        int64_t parent = (i - 1) / 2;
        if (!less(h->items[i], h->items[parent])) {
            break;
        }
        Crop t = h->items[i];
        h->items[i] = h->items[parent];
        h->items[parent] = t;
        i = parent;
    }
}

static Crop heap_pop(Heap *h) {
    Crop top = h->items[0];
    h->items[0] = h->items[--h->len];
    int64_t i = 0;
    for (;;) {
        int64_t l = 2 * i + 1, r = l + 1, m = i;
        if (l < h->len && less(h->items[l], h->items[m])) {
            m = l;
        }
        if (r < h->len && less(h->items[r], h->items[m])) {
            m = r;
        }
        if (m == i) {
            break;
        }
        Crop t = h->items[i];
        h->items[i] = h->items[m];
        h->items[m] = t;
        i = m;
    }
    return top;
}

// each day the rotten crops dropped and one apple eaten from the soonest to rot
static int32_t eaten_apples(const int32_t *apples, const int32_t *days, int64_t n) {
    Heap queue = {0};
    int32_t eaten = 0;
    for (int64_t day = 0; day < n || queue.len > 0; day++) {
        if (day < n && apples[day] > 0) {
            heap_push(&queue, (Crop){day + days[day], apples[day]});
        }
        while (queue.len > 0 && queue.items[0].rot <= day) {
            heap_pop(&queue);
        }
        if (queue.len > 0) {
            Crop c = heap_pop(&queue);
            eaten++;
            if (c.left > 1) {
                heap_push(&queue, (Crop){c.rot, c.left - 1});
            }
        }
    }
    free(queue.items);
    return eaten;
}

// ---- the harness ----------------------------------------------------------

static int64_t seed = 1705;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int32_t *apples = malloc((size_t)COUNT * N * sizeof *apples);
    int32_t *days = malloc((size_t)COUNT * N * sizeof *days);
    for (int c = 0; c < COUNT; c++) {
        for (int64_t i = 0; i < N; i++) {
            // one day in four grows nothing
            int64_t grown = next_random() % 4 == 0 ? 0 : next_random() % 20000 + 1;
            apples[(int64_t)c * N + i] = (int32_t)grown;
            days[(int64_t)c * N + i] = grown == 0 ? 0 : (int32_t)(next_random() % 20000 + 1);
        }
    }
    int64_t sum = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int c = 0; c < COUNT; c++) {
            int64_t answer = eaten_apples(apples + (int64_t)c * N, days + (int64_t)c * N, N);
            sum += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    printf("%d trees of %d days, %d rounds: answers sum to %lld, checksum %lld\n", COUNT, N, ROUNDS, (long long)sum, (long long)check);
    free(apples);
    free(days);
    return 0;
}
