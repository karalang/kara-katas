#include <stdio.h>
#include <stdlib.h>

typedef struct {
    long *data;
    long len;
    long cap;
} Stack;

static void st_init(Stack *s) {
    s->cap = 8;
    s->len = 0;
    s->data = malloc(s->cap * sizeof(long));
}

static void st_push(Stack *s, long x) {
    if (s->len == s->cap) {
        s->cap *= 2;
        s->data = realloc(s->data, s->cap * sizeof(long));
    }
    s->data[s->len++] = x;
}

static long st_pop(Stack *s) {
    return s->data[--s->len];
}

typedef struct {
    Stack inbox;
    Stack outbox;
} MyQueue;

static void q_push(MyQueue *q, long x) {
    st_push(&q->inbox, x);
}

static void refill(MyQueue *q) {
    if (q->outbox.len == 0) {
        while (q->inbox.len > 0) {
            long v = st_pop(&q->inbox);
            st_push(&q->outbox, v);
        }
    }
}

static long q_pop(MyQueue *q) {
    refill(q);
    return st_pop(&q->outbox);
}

static long q_peek(MyQueue *q) {
    refill(q);
    return q->outbox.data[q->outbox.len - 1];
}

static int q_empty(MyQueue *q) {
    return q->inbox.len == 0 && q->outbox.len == 0;
}

int main(void) {
    long n = 75000000;
    long cap = 4096;
    long mask = 1048575;

    MyQueue q;
    st_init(&q.inbox);
    st_init(&q.outbox);
    long sz = 0;
    long sink = 0;
    long state = 12345;

    for (long i = 0; i < n; i++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        if (q_empty(&q) || (state % 2 == 0 && sz < cap)) {
            q_push(&q, state & mask);
            sz += 1;
        } else if (state % 4 == 0) {
            sink += q_peek(&q);
        } else {
            sink += q_pop(&q);
            sz -= 1;
        }
    }
    printf("%ld\n", sink);
    free(q.inbox.data);
    free(q.outbox.data);
    return 0;
}
