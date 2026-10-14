// LeetCode #622: Design Circular Queue -- C mirror of the Kāra bench.
//
// The ★ arm's ring with a start and a count, on the same script and
// queues.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t *data;
    int64_t len;
    int64_t head;
    int64_t count;
} MyCircularQueue;

static MyCircularQueue queue_new(int64_t k) {
    MyCircularQueue q = {calloc(k, sizeof(int64_t)), k, 0, 0};
    return q;
}

static bool en_queue(MyCircularQueue *q, int64_t value) {
    if (q->count == q->len) {
        return false;
    }
    q->data[(q->head + q->count) % q->len] = value;
    q->count += 1;
    return true;
}

static bool de_queue(MyCircularQueue *q) {
    if (q->count == 0) {
        return false;
    }
    q->head = (q->head + 1) % q->len;
    q->count -= 1;
    return true;
}

static int64_t front(const MyCircularQueue *q) {
    return q->count == 0 ? -1 : q->data[q->head];
}

static int64_t rear(const MyCircularQueue *q) {
    return q->count == 0 ? -1 : q->data[(q->head + q->count - 1) % q->len];
}

static bool is_empty(const MyCircularQueue *q) { return q->count == 0; }

static bool is_full(const MyCircularQueue *q) { return q->count == q->len; }

static int64_t seed = 622;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    enum { ROUNDS = 300, COUNT = 100000 };
    int64_t *ops = malloc(COUNT * sizeof(int64_t));
    for (int64_t i = 0; i < COUNT; i++) {
        int64_t roll = next_random() % 40;
        if (roll < 16) {
            ops[i] = next_random() % 1001;
        } else if (roll < 26) {
            ops[i] = -1;
        } else if (roll < 30) {
            ops[i] = -2;
        } else if (roll < 34) {
            ops[i] = -3;
        } else if (roll < 37) {
            ops[i] = -4;
        } else {
            ops[i] = -5;
        }
    }
    int64_t checksum = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        MyCircularQueue q = queue_new(1 + (r * 37) % 1000);
        for (int64_t i = 0; i < COUNT; i++) {
            int64_t op = ops[i];
            int64_t v;
            if (op >= 0) {
                v = en_queue(&q, op);
            } else if (op == -1) {
                v = de_queue(&q);
            } else if (op == -2) {
                v = front(&q);
            } else if (op == -3) {
                v = rear(&q);
            } else if (op == -4) {
                v = is_empty(&q);
            } else {
                v = is_full(&q);
            }
            checksum = (checksum * 31 + v + 2) % 1000000007;
        }
        free(q.data);
    }
    printf("%d queues, %d operations each: checksum %lld\n", ROUNDS, COUNT, (long long)checksum);
    free(ops);
    return 0;
}
