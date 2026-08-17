/* LeetCode 277 par-lane mirror — pthreads. The metal floor for the Kara
 * `#[par_order_free]` lane: the same instance split, hand-threaded. */
#include <stdio.h>
#include <stdint.h>
#include <pthread.h>

#define N 2500000
#define INSTANCES 64
#define NTHREADS 4

static int knows(int64_t star, int64_t a, int64_t b) {
    if (b == star) return 1;
    if (a == star) return 0;
    int64_t h = (a * 1103515245LL + b * 12345LL) % 2147483647LL;
    return h % 2 == 0;
}
static int64_t find_celebrity(int64_t n, int64_t star) {
    int64_t cand = 0;
    for (int64_t i = 1; i < n; i++) if (knows(star, cand, i)) cand = i;
    for (int64_t j = 0; j < n; j++)
        if (j != cand) {
            if (knows(star, cand, j)) return -1;
            if (!knows(star, j, cand)) return -1;
        }
    return cand;
}
struct arg { int lo, hi; int64_t out; };
static void *worker(void *v) {
    struct arg *a = (struct arg *)v;
    int64_t s = 0;
    for (int i = a->lo; i < a->hi; i++) {
        int64_t star = ((int64_t)i * 7919LL) % N;
        s = (s + ((int64_t)i * 1000003LL + find_celebrity(N, star)) % 1000000007LL) % 1000000007LL;
    }
    a->out = s;
    return NULL;
}
int main(void) {
    pthread_t th[NTHREADS];
    struct arg args[NTHREADS];
    int per = (INSTANCES + NTHREADS - 1) / NTHREADS;
    for (int t = 0; t < NTHREADS; t++) {
        args[t].lo = t * per;
        args[t].hi = (t + 1) * per < INSTANCES ? (t + 1) * per : INSTANCES;
        if (args[t].lo > INSTANCES) args[t].lo = INSTANCES;
        args[t].out = 0;
        pthread_create(&th[t], NULL, worker, &args[t]);
    }
    int64_t sink = 0;
    for (int t = 0; t < NTHREADS; t++) { pthread_join(th[t], NULL); sink = (sink + args[t].out) % 1000000007LL; }
    printf("%lld\n", (long long)sink);
    return 0;
}
