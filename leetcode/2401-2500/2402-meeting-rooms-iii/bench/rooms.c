// LeetCode #2402: Meeting Rooms III -- the bench, the ★ arm in C: a binary
// heap of free rooms and one of (end, room) for the rooms in use, over the
// meetings sorted by start.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t a, b;
} pair;

static int64_t seed = 2402;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int less(pair x, pair y) { return x.a < y.a || (x.a == y.a && x.b < y.b); }

static int cmp_pair(const void *p, const void *q) {
    pair x = *(const pair *)p, y = *(const pair *)q;
    return less(x, y) ? -1 : less(y, x) ? 1 : 0;
}

// A min-heap of pairs; the free rooms use it with a = room.
typedef struct {
    pair *v;
    int64_t len;
} heap;

static void push(heap *h, pair x) {
    int64_t i = h->len++;
    h->v[i] = x;
    while (i > 0 && less(h->v[i], h->v[(i - 1) / 2])) {
        pair t = h->v[i];
        h->v[i] = h->v[(i - 1) / 2];
        h->v[(i - 1) / 2] = t;
        i = (i - 1) / 2;
    }
}

static pair pop(heap *h) {
    pair top = h->v[0];
    h->v[0] = h->v[--h->len];
    int64_t i = 0;
    for (;;) {
        int64_t l = 2 * i + 1, r = l + 1, m = i;
        if (l < h->len && less(h->v[l], h->v[m])) m = l;
        if (r < h->len && less(h->v[r], h->v[m])) m = r;
        if (m == i) break;
        pair t = h->v[i];
        h->v[i] = h->v[m];
        h->v[m] = t;
        i = m;
    }
    return top;
}

static int64_t most_booked(int64_t n, const pair *meetings, int64_t m) {
    pair *order = malloc(m * sizeof *order);
    memcpy(order, meetings, m * sizeof *order);
    qsort(order, m, sizeof *order, cmp_pair);
    heap free_rooms = {malloc(n * sizeof(pair)), 0}, busy = {malloc(n * sizeof(pair)), 0};
    int64_t *count = calloc(n, sizeof *count);
    for (int64_t r = 0; r < n; r++) push(&free_rooms, (pair){r, 0});
    for (int64_t i = 0; i < m; i++) {
        int64_t start = order[i].a, end = order[i].b;
        while (busy.len > 0 && busy.v[0].a <= start) push(&free_rooms, (pair){pop(&busy).b, 0});
        if (free_rooms.len > 0) {
            int64_t room = pop(&free_rooms).a;
            count[room]++;
            push(&busy, (pair){end, room});
        } else {
            pair p = pop(&busy);
            count[p.b]++;
            push(&busy, (pair){p.a + end - start, p.b});
        }
    }
    int64_t best = 0;
    for (int64_t r = 1; r < n; r++)
        if (count[r] > count[best]) best = r;
    free(order);
    free(free_rooms.v);
    free(busy.v);
    free(count);
    return best;
}

int main(void) {
    pair *cases[10];
    int64_t *starts = malloc(500000 * sizeof *starts);
    for (int64_t c = 0; c < 10; c++) {
        for (int64_t i = 0; i < 500000; i++) starts[i] = i;
        for (int64_t i = 0; i < 100000; i++) {
            int64_t hi = next_random();
            int64_t j = i + (hi * 32768 + next_random()) % (500000 - i);
            int64_t t = starts[i];
            starts[i] = starts[j];
            starts[j] = t;
        }
        cases[c] = malloc(100000 * sizeof(pair));
        for (int64_t i = 0; i < 100000; i++)
            cases[c][i] = (pair){starts[i], starts[i] + 1 + next_random() % (1 + 500 * c)};
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 10; p++)
        for (int c = 0; c < 10; c++) check = (check * 31 + most_booked(100, cases[c], 100000) + p) % 1000000007;
    printf("10 passes over 10 cases of 10^5 meetings in 100 rooms: checksum %lld\n", (long long)check);
    for (int c = 0; c < 10; c++) free(cases[c]);
    free(starts);
    return 0;
}
