// LeetCode #933: Number of Recent Calls -- bench: a queue of the recent
// pings. Mirrors recent_counter.kara, .rs, .py and go-seq/. The queue is
// a ring buffer whose size is a power of two, doubled when full, as Rust's
// VecDeque does.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t *items;
    int64_t cap;
    int64_t head;
    int64_t len;
} RecentCounter;

static void counter_init(RecentCounter *c) {
    c->cap = 0;
    c->items = NULL;
    c->head = 0;
    c->len = 0;
}

static void counter_free(RecentCounter *c) { free(c->items); }

static void push_back(RecentCounter *c, int64_t t) {
    if (c->len == c->cap) {
        int64_t cap = c->cap == 0 ? 4 : 2 * c->cap;
        int64_t *items = malloc(sizeof(int64_t) * (size_t)cap);
        for (int64_t i = 0; i < c->len; i++) {
            items[i] = c->items[(c->head + i) & (c->cap - 1)];
        }
        free(c->items);
        c->items = items;
        c->cap = cap;
        c->head = 0;
    }
    c->items[(c->head + c->len) & (c->cap - 1)] = t;
    c->len++;
}

static int64_t ping(RecentCounter *c, int64_t t) {
    push_back(c, t);
    while (c->items[c->head] < t - 3000) {
        c->head = (c->head + 1) & (c->cap - 1);
        c->len--;
    }
    return c->len;
}

static int64_t seed = 933;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t rounds = 50;
    int64_t count = 100;
    int64_t len = 10000;
    // count streams of len pings, each from 1 to gap after the one before,
    // gap from 1 to 600 a stream, built once
    int64_t *streams = malloc(sizeof(int64_t) * (size_t)(count * len));
    for (int64_t s = 0; s < count; s++) {
        int64_t gap = 1 + next_random() % 600;
        int64_t t = 0;
        for (int64_t k = 0; k < len; k++) {
            t += 1 + next_random() % gap;
            streams[s * len + k] = t;
        }
    }
    int64_t total = 0;
    int64_t check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        // each round plays every stream into a new counter, starting from
        // a different one
        for (int64_t i = 0; i < count; i++) {
            RecentCounter counter;
            counter_init(&counter);
            int64_t last = 0;
            int64_t *times = streams + ((r + i) % count) * len;
            for (int64_t k = 0; k < len; k++) {
                last = ping(&counter, times[k]);
                total += last;
            }
            check = (check * 1000003 + last) % 1000000007;
            counter_free(&counter);
        }
    }
    printf("%lld rounds over %lld streams of %lld pings: answers summing to %lld, checksum %lld\n",
           (long long)rounds, (long long)count, (long long)len, (long long)total,
           (long long)check);
    free(streams);
    return 0;
}
