// Benchmark for #362 -- mirror of hit_counter.kara.
// The queue is a growable ring buffer, as VecDeque is.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct { int64_t *buf; int64_t cap, head, len; } Queue;

static void push_back(Queue *q, int64_t v) {
    if (q->len == q->cap) {
        int64_t cap = q->cap ? q->cap * 2 : 16;
        int64_t *buf = malloc(sizeof(int64_t) * cap);
        for (int64_t i = 0; i < q->len; i++) buf[i] = q->buf[(q->head + i) % q->cap];
        free(q->buf);
        q->buf = buf; q->cap = cap; q->head = 0;
    }
    q->buf[(q->head + q->len) % q->cap] = v;
    q->len++;
}

static int64_t get_hits(Queue *q, int64_t timestamp) {
    while (q->len > 0 && q->buf[q->head] <= timestamp - 300) {
        q->head = (q->head + 1) % q->cap;
        q->len--;
    }
    return q->len;
}

int main(void) {
    Queue q = {0};
    int64_t seed = 362, t = 1, checksum = 0;
    for (int i = 0; i < 2000000; i++) {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        t += (seed / 65536) % 3;
        seed = (seed * 1103515245 + 12345) % 2147483648;
        if ((seed / 65536) % 4 == 0) checksum = (checksum * 31 + get_hits(&q, t)) % 1000000007;
        else push_back(&q, t);
    }
    printf("checksum %lld\n", (long long)checksum);
    free(q.buf);
    return 0;
}
