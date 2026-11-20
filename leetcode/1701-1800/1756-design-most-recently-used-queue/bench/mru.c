// LeetCode #1756: Design Most Recently Used Queue -- the bench (mru.kara in
// C): an array.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

enum { COUNT = 10000, N = 2000, CALLS = 2000 };

typedef struct {
    int32_t values[N];
    int64_t n;
} MruQueue;

static void mru_init(MruQueue *q, int32_t n) {
    q->n = n;
    for (int32_t i = 0; i < n; i++) q->values[i] = i + 1;
}

static int32_t mru_fetch(MruQueue *q, int32_t k) {
    int32_t value = q->values[k - 1];
    memmove(q->values + k - 1, q->values + k, (q->n - k) * sizeof(int32_t));
    q->values[q->n - 1] = value;
    return value;
}

static int64_t seed = 1756;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int32_t fetches[CALLS];
    for (int i = 0; i < CALLS; i++) fetches[i] = (int32_t)(next_random() % N + 1);
    static MruQueue queue;
    int64_t sum = 0, check = 0;
    for (int64_t r = 0; r < COUNT; r++) {
        mru_init(&queue, N);
        for (int i = 0; i < CALLS; i++) {
            int64_t got = mru_fetch(&queue, fetches[i]);
            sum += got;
            check = (check * 31 + got + r) % 1000000007;
        }
    }
    printf("%d queues of %d values, %d fetches each: fetched values add to %lld, checksum %lld\n", COUNT, N, CALLS, (long long)sum, (long long)check);
    return 0;
}
