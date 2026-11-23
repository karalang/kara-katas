// LeetCode #2532: Time to Cross a Bridge -- benchmark mirror of the ★ arm
// (bridge.kara): 200 cases built once, then the passes, each asking every
// case from an offset the checksum picks. The four queues are binary heaps
// of (key, worker) pairs, two largest first and two smallest first.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t key;
    int64_t i;
} Pair;

typedef struct {
    Pair *a;
    int64_t len;
    int max_first;
} Heap;

static int before(const Heap *h, Pair x, Pair y) {
    int less = x.key < y.key || (x.key == y.key && x.i < y.i);
    int greater = x.key > y.key || (x.key == y.key && x.i > y.i);
    return h->max_first ? greater : less;
}

static void push(Heap *h, int64_t key, int64_t i) {
    int64_t at = h->len++;
    h->a[at] = (Pair){key, i};
    while (at > 0) {
        int64_t up = (at - 1) / 2;
        if (!before(h, h->a[at], h->a[up])) break;
        Pair t = h->a[at];
        h->a[at] = h->a[up];
        h->a[up] = t;
        at = up;
    }
}

static Pair pop(Heap *h) {
    Pair top = h->a[0];
    h->a[0] = h->a[--h->len];
    int64_t at = 0;
    for (;;) {
        int64_t l = 2 * at + 1, r = l + 1, best = at;
        if (l < h->len && before(h, h->a[l], h->a[best])) best = l;
        if (r < h->len && before(h, h->a[r], h->a[best])) best = r;
        if (best == at) break;
        Pair t = h->a[at];
        h->a[at] = h->a[best];
        h->a[best] = t;
        at = best;
    }
    return top;
}

static int64_t find_crossing_time(int64_t n, int64_t k, const int64_t (*time)[4], Pair *store) {
    Heap left = {store, 0, 1}, right = {store + k, 0, 1};
    Heap picking = {store + 2 * k, 0, 0}, putting = {store + 3 * k, 0, 0};
    for (int64_t i = 0; i < k; i++) push(&left, time[i][0] + time[i][2], i);
    int64_t boxes = n, now = 0;
    while (boxes > 0 || right.len > 0 || picking.len > 0) {
        while (putting.len > 0 && putting.a[0].key <= now) {
            int64_t i = pop(&putting).i;
            push(&left, time[i][0] + time[i][2], i);
        }
        while (picking.len > 0 && picking.a[0].key <= now) {
            int64_t i = pop(&picking).i;
            push(&right, time[i][0] + time[i][2], i);
        }
        if (right.len > 0) {
            int64_t i = pop(&right).i;
            now += time[i][2];
            push(&putting, now + time[i][3], i);
        } else if (boxes > 0 && left.len > 0) {
            int64_t i = pop(&left).i;
            now += time[i][0];
            boxes -= 1;
            push(&picking, now + time[i][1], i);
        } else {
            int64_t next = INT64_MAX;
            if (picking.len > 0 && picking.a[0].key < next) next = picking.a[0].key;
            if (boxes > 0 && putting.len > 0 && putting.a[0].key < next) next = putting.a[0].key;
            now = next;
        }
    }
    return now;
}

static int64_t seed = 2532;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t ns[200], ks[200];
    int64_t (*times[200])[4];
    for (int t = 0; t < 200; t++) {
        ns[t] = next_random() % 1000 + 1;
        ks[t] = next_random() % 100 + 1;
        times[t] = malloc(sizeof(int64_t[4]) * ks[t]);
        for (int64_t i = 0; i < ks[t]; i++)
            for (int j = 0; j < 4; j++) times[t][i][j] = next_random() % 1000 + 1;
    }
    Pair *store = malloc(sizeof(Pair) * 4 * 100);
    const int64_t passes = 100;
    int64_t check = 0;
    for (int64_t p = 0; p < passes; p++) {
        int64_t start = check % 200;
        for (int64_t i = 0; i < 200; i++) {
            int64_t at = (start + i) % 200;
            check = (check * 31 + find_crossing_time(ns[at], ks[at], (const int64_t (*)[4])times[at], store) + p) % 1000000007;
        }
    }
    printf("%lld passes over 200 cases: checksum %lld\n", (long long)passes, (long long)check);
    return 0;
}
