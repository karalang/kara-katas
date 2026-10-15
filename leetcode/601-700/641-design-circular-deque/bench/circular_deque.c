// Benchmark for #641: mirror of circular_deque.kara (the ★ arm: a ring
// with a start and a count) on the same workload.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t *data;
    int64_t len;
    int64_t head;
    int64_t count;
} MyCircularDeque;

static MyCircularDeque deque_new(int64_t k) {
    MyCircularDeque q;
    q.data = calloc((size_t)k, sizeof(int64_t));
    q.len = k;
    q.head = 0;
    q.count = 0;
    return q;
}

static int insert_front(MyCircularDeque *q, int64_t value) {
    if (q->count == q->len) {
        return 0;
    }
    q->head = (q->head + q->len - 1) % q->len;
    q->data[q->head] = value;
    q->count++;
    return 1;
}

static int insert_last(MyCircularDeque *q, int64_t value) {
    if (q->count == q->len) {
        return 0;
    }
    int64_t at = (q->head + q->count) % q->len;
    q->data[at] = value;
    q->count++;
    return 1;
}

static int delete_front(MyCircularDeque *q) {
    if (q->count == 0) {
        return 0;
    }
    q->head = (q->head + 1) % q->len;
    q->count--;
    return 1;
}

static int delete_last(MyCircularDeque *q) {
    if (q->count == 0) {
        return 0;
    }
    q->count--;
    return 1;
}

static int64_t get_front(const MyCircularDeque *q) {
    return q->count == 0 ? -1 : q->data[q->head];
}

static int64_t get_rear(const MyCircularDeque *q) {
    return q->count == 0 ? -1 : q->data[(q->head + q->count - 1) % q->len];
}

static int is_empty(const MyCircularDeque *q) { return q->count == 0; }

static int is_full(const MyCircularDeque *q) { return q->count == q->len; }

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t *script(int64_t count, int64_t *seed) {
    int64_t *ops = malloc((size_t)count * sizeof(int64_t));
    for (int64_t i = 0; i < count; i++) {
        int64_t roll = next_random(seed) % 40;
        if (roll < 8) {
            ops[i] = next_random(seed) % 1001;
        } else if (roll < 16) {
            ops[i] = 1001 + next_random(seed) % 1001;
        } else if (roll < 21) {
            ops[i] = -1;
        } else if (roll < 26) {
            ops[i] = -2;
        } else if (roll < 30) {
            ops[i] = -3;
        } else if (roll < 34) {
            ops[i] = -4;
        } else if (roll < 37) {
            ops[i] = -5;
        } else {
            ops[i] = -6;
        }
    }
    return ops;
}

int main(void) {
    int64_t rounds = 300;
    int64_t seed = 641;
    int64_t n = 100000;
    int64_t *ops = script(n, &seed);
    int64_t checksum = 0;
    for (int64_t r = 0; r < rounds; r++) {
        MyCircularDeque q = deque_new(1 + (r * 37) % 1000);
        for (int64_t i = 0; i < n; i++) {
            int64_t op = ops[i];
            int64_t v;
            if (op >= 1001) {
                v = insert_last(&q, op - 1001);
            } else if (op >= 0) {
                v = insert_front(&q, op);
            } else if (op == -1) {
                v = delete_front(&q);
            } else if (op == -2) {
                v = delete_last(&q);
            } else if (op == -3) {
                v = get_front(&q);
            } else if (op == -4) {
                v = get_rear(&q);
            } else if (op == -5) {
                v = is_empty(&q);
            } else {
                v = is_full(&q);
            }
            checksum = (checksum * 31 + v + 2) % 1000000007;
        }
        free(q.data);
    }
    free(ops);
    printf("%lld deques, %lld operations each: checksum %lld\n", (long long)rounds,
           (long long)n, (long long)checksum);
    return 0;
}
