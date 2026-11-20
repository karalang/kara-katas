// LeetCode #1670: Design Front Middle Back Queue -- the bench's C mirror: the
// ★ arm on one run of 1000000 calls, a push three times in five, values up
// to 10^9, drawn first and then replayed 60 times, each on a new queue.
// C has no deque, so each half is a growable ring buffer, as Rust's and
// Kāra's `VecDeque` are.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define ROUNDS 60
#define CALLS 1000000

typedef struct {
    int32_t *buf;
    int64_t cap, head, len;
} Deque;

static void grow(Deque *d) {
    int64_t cap = d->cap ? d->cap * 2 : 8;
    int32_t *buf = malloc((size_t)cap * sizeof *buf);
    for (int64_t i = 0; i < d->len; i++) buf[i] = d->buf[(d->head + i) % d->cap];
    free(d->buf);
    d->buf = buf;
    d->cap = cap;
    d->head = 0;
}

static void push_front(Deque *d, int32_t v) {
    if (d->len == d->cap) grow(d);
    d->head = (d->head + d->cap - 1) % d->cap;
    d->buf[d->head] = v;
    d->len++;
}

static void push_back(Deque *d, int32_t v) {
    if (d->len == d->cap) grow(d);
    d->buf[(d->head + d->len) % d->cap] = v;
    d->len++;
}

static int32_t pop_front(Deque *d) {
    int32_t v = d->buf[d->head];
    d->head = (d->head + 1) % d->cap;
    d->len--;
    return v;
}

static int32_t pop_back(Deque *d) {
    d->len--;
    return d->buf[(d->head + d->len) % d->cap];
}

typedef struct {
    Deque front, back;
} Queue;

static void balance(Queue *q) {
    if (q->front.len > q->back.len) push_front(&q->back, pop_back(&q->front));
    else if (q->back.len > q->front.len + 1) push_back(&q->front, pop_front(&q->back));
}

static void q_push_front(Queue *q, int32_t v) {
    push_front(&q->front, v);
    balance(q);
}

static void q_push_middle(Queue *q, int32_t v) {
    push_back(&q->front, v);
    balance(q);
}

static void q_push_back(Queue *q, int32_t v) {
    push_back(&q->back, v);
    balance(q);
}

static int32_t q_pop_front(Queue *q) {
    int32_t v;
    if (q->front.len) v = pop_front(&q->front);
    else if (q->back.len) v = pop_front(&q->back);
    else return -1;
    balance(q);
    return v;
}

static int32_t q_pop_middle(Queue *q) {
    int32_t v;
    if (q->front.len == q->back.len) {
        if (!q->front.len) return -1;
        v = pop_back(&q->front);
    } else {
        v = pop_front(&q->back);
    }
    balance(q);
    return v;
}

static int32_t q_pop_back(Queue *q) {
    if (!q->back.len) return -1;
    int32_t v = pop_back(&q->back);
    balance(q);
    return v;
}

// ---- the harness ----------------------------------------------------------

static int64_t seed = 1670;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    static int64_t ops[CALLS];
    static int32_t vals[CALLS];
    for (int i = 0; i < CALLS; i++) {
        int64_t r = next_random() % 10;
        ops[i] = r < 6 ? r / 2 : r - 3;
        vals[i] = (int32_t)((next_random() * 32768 + next_random()) % 1000000000 + 1);
    }
    int64_t empty = 0, left = 0, check = 0;
    for (int round = 0; round < ROUNDS; round++) {
        Queue q;
        memset(&q, 0, sizeof q);
        for (int i = 0; i < CALLS; i++) {
            int32_t got;
            switch (ops[i]) {
            case 0: q_push_front(&q, vals[i]); continue;
            case 1: q_push_middle(&q, vals[i]); continue;
            case 2: q_push_back(&q, vals[i]); continue;
            case 3: got = q_pop_front(&q); break;
            case 4: got = q_pop_middle(&q); break;
            default: got = q_pop_back(&q); break;
            }
            if (got == -1) empty++;
            check = (check * 31 + got + 1) % 1000000007;
        }
        left += q.front.len + q.back.len;
        free(q.front.buf);
        free(q.back.buf);
    }
    printf("%d calls, %d rounds: %lld pops on an empty queue, %lld values left, checksum %lld\n", CALLS, ROUNDS, (long long)empty, (long long)left, (long long)check);
    return 0;
}
