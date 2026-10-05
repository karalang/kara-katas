// Benchmark workload for LeetCode #346 — C mirror of moving_average.kara.
//
// C has no standard queue, so the window is a growable ring deque, the
// structure behind Rust's VecDeque and Kāra's: push at the back, pop at the
// front, double the buffer when it fills.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define LEN 10000000LL
#define WINDOW 1000

typedef struct {
    int64_t *buf;
    int64_t cap, head, len;
} Deque;

static void push_back(Deque *d, int64_t v) {
    if (d->len == d->cap) {
        int64_t cap = d->cap ? d->cap * 2 : 4;
        int64_t *nb = malloc(sizeof(int64_t) * cap);
        for (int64_t k = 0; k < d->len; k++) {
            nb[k] = d->buf[(d->head + k) % d->cap];
        }
        free(d->buf);
        d->buf = nb;
        d->cap = cap;
        d->head = 0;
    }
    d->buf[(d->head + d->len) % d->cap] = v;
    d->len++;
}

static int64_t pop_front(Deque *d) {
    int64_t v = d->buf[d->head];
    d->head = (d->head + 1) % d->cap;
    d->len--;
    return v;
}

typedef struct {
    int64_t size;
    Deque window;
    int64_t sum;
} MovingAverage;

static double next(MovingAverage *m, int64_t val) {
    push_back(&m->window, val);
    m->sum += val;
    if (m->window.len > m->size) {
        m->sum -= pop_front(&m->window);
    }
    return (double)m->sum / (double)m->window.len;
}

int main(void) {
    MovingAverage m = {WINDOW, {NULL, 0, 0, 0}, 0};
    int64_t seed = 346;
    double sink = 0.0;
    for (int64_t i = 0; i < LEN; i++) {
        seed = (seed * 1103515245 + 12345) % 2147483648LL;
        sink += next(&m, seed / 16 % 200001 - 100000);
    }
    printf("sink %.3f\n", sink);
    free(m.window.buf);
    return 0;
}
