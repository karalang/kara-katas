#include <stdio.h>
#include <stdlib.h>

typedef struct {
    long *data;
    long len;
    long cap;
    long head;
} Queue;

static void q_init(Queue *q) {
    q->cap = 64;
    q->data = malloc(q->cap * sizeof(long));
    q->len = 0;
    q->head = 0;
}

static void q_free(Queue *q) { free(q->data); }

static long q_size(const Queue *q) { return q->len - q->head; }

static void q_enqueue(Queue *q, long x) {
    if (q->len == q->cap) {
        q->cap *= 2;
        q->data = realloc(q->data, q->cap * sizeof(long));
    }
    q->data[q->len++] = x;
}

static long q_dequeue(Queue *q) {
    long v = q->data[q->head];
    q->head++;
    return v;
}

static long q_front(const Queue *q) { return q->data[q->head]; }

static void stack_push(Queue *q, long x) {
    q_enqueue(q, x);
    long rotations = q_size(q) - 1;
    while (rotations > 0) {
        long front = q_dequeue(q);
        q_enqueue(q, front);
        rotations--;
    }
}

static long stack_pop(Queue *q) { return q_dequeue(q); }
static long stack_top(const Queue *q) { return q_front(q); }

int main(void) {
    long passes = 12000;
    long ops_per_pass = 1500;
    long cap = 48;
    long modulus = 1000000007;

    long state = 12345;
    long sink = 0;
    for (long p = 0; p < passes; p++) {
        Queue s;
        q_init(&s);
        for (long j = 0; j < ops_per_pass; j++) {
            state = (state * 1103515245L + 12345L) & 2147483647L;
            long v = (state % 1000) + 1;
            long sel = state % 4;
            long size = q_size(&s);
            if (size == 0) {
                stack_push(&s, v);
            } else if (size >= cap) {
                if ((state & 1) == 0) {
                    sink = (sink + stack_pop(&s)) % modulus;
                } else {
                    sink = (sink + stack_top(&s)) % modulus;
                }
            } else {
                if (sel <= 1) {
                    stack_push(&s, v);
                } else if (sel == 2) {
                    sink = (sink + stack_pop(&s)) % modulus;
                } else {
                    sink = (sink + stack_top(&s)) % modulus;
                }
            }
        }
        q_free(&s);
    }
    printf("%ld\n", sink);
    return 0;
}
