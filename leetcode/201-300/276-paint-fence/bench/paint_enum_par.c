/* LeetCode 276 par-lane mirror — pthreads. The metal floor for the Kara
 * `#[par_order_free]` lane: the same 16-branch split, hand-parallelized the way
 * a C programmer would write it. Same algorithm as paint_enum.c otherwise. */
#include <stdio.h>
#include <stdint.h>
#include <pthread.h>

#define N 13
#define K 4
#define PREFIXES (K * K)
#define NTHREADS 4

static int64_t count_prefix(int p0, int p1) {
    int c[N] = {0};
    c[0] = p0;
    c[1] = p1;
    int64_t count = 0;
    for (;;) {
        int ok = 1;
        for (int i = 2; i < N; i++)
            if (c[i] == c[i - 1] && c[i - 1] == c[i - 2]) ok = 0;
        if (ok) count++;
        int p = N - 1;
        while (p >= 2 && c[p] == K - 1) { c[p] = 0; p--; }
        if (p < 2) break;
        c[p]++;
    }
    return count;
}

struct arg { int lo, hi; int64_t out; };

static void *worker(void *v) {
    struct arg *a = (struct arg *)v;
    int64_t s = 0;
    for (int pre = a->lo; pre < a->hi; pre++) s += count_prefix(pre / K, pre % K);
    a->out = s;
    return NULL;
}

int main(void) {
    pthread_t th[NTHREADS];
    struct arg args[NTHREADS];
    int per = (PREFIXES + NTHREADS - 1) / NTHREADS;
    for (int t = 0; t < NTHREADS; t++) {
        args[t].lo = t * per;
        args[t].hi = (t + 1) * per < PREFIXES ? (t + 1) * per : PREFIXES;
        if (args[t].lo > PREFIXES) args[t].lo = PREFIXES;
        args[t].out = 0;
        pthread_create(&th[t], NULL, worker, &args[t]);
    }
    int64_t total = 0;
    for (int t = 0; t < NTHREADS; t++) { pthread_join(th[t], NULL); total += args[t].out; }
    printf("%lld\n", (long long)total);
    return 0;
}
