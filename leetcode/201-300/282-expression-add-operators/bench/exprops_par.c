/* LeetCode 282 par-lane mirror — C + pthreads. The metal floor for the Kara
 * `#[par_order_free]` lane: the same 220 independent searches, hand-threaded.
 *
 * Otherwise identical to exprops.c: same backtracking search, same per-branch
 * heap allocation, same order-invariant per-input sink.
 *
 * EACH BRANCH HEAP-ALLOCATES ITS EXPRESSION, deliberately. A stack buffer is the
 * natural C move and measured 4.6x faster than the other three lanes — but Kara,
 * Rust and Go all allocate a fresh string per branch, so a stack-buffer C lane is
 * not running the same algorithm. malloc/free per branch is what parity costs. */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
#include <pthread.h>
#define INPUTS 220
#define NTHREADS 4
#define NDIG 9

static void make_input(int64_t idx, char *num) {
    int64_t seed = (20260820LL + idx * 7919LL) % 2147483648LL;
    for (int d = 0; d < NDIG; d++) {
        seed = (seed*1103515245LL+12345LL)%2147483648LL;
        num[d] = (char)('0' + 1 + (seed/19) % 6);
    }
    num[NDIG] = 0;
}
static int64_t target_for(int64_t idx) {
    int64_t seed = (20260820LL + idx * 7919LL) % 2147483648LL;
    for (int d = 0; d < 10; d++) seed = (seed*1103515245LL+12345LL)%2147483648LL;
    return (seed/23) % 40;
}

static void search(const char *num, int64_t target, int pos, char *expr, int elen,
                   int64_t cur, int64_t last, int64_t *found, int64_t *hash) {
    if (pos == NDIG) {
        if (cur == target) { (*found)++; *hash = (*hash * 31 + elen) % 1000000007LL; }
        return;
    }
    for (int end = pos + 1; end <= NDIG; end++) {
        if (end > pos + 1 && num[pos] == '0') return;
        int64_t n = 0;
        for (int k = pos; k < end; k++) n = n * 10 + (num[k] - '0');
        int plen = end - pos;
        if (pos == 0) {
            char *buf = malloc((size_t)plen + 1);
            memcpy(buf, num + pos, (size_t)plen); buf[plen] = 0;
            search(num, target, end, buf, plen, n, n, found, hash);
            free(buf);
        } else {
            const char ops[3] = {'+', '-', '*'};
            for (int o = 0; o < 3; o++) {
                int nl = elen + 1 + plen;
                char *buf = malloc((size_t)nl + 1);
                memcpy(buf, expr, (size_t)elen);
                buf[elen] = ops[o];
                memcpy(buf + elen + 1, num + pos, (size_t)plen);
                buf[nl] = 0;
                if (o == 0)      search(num, target, end, buf, nl, cur + n, n, found, hash);
                else if (o == 1) search(num, target, end, buf, nl, cur - n, -n, found, hash);
                else             search(num, target, end, buf, nl, cur - last + last*n, last*n, found, hash);
                free(buf);
            }
        }
    }
}

int64_t solve_one(int64_t i) {
    char num[NDIG + 1];
    make_input(i, num);
    int64_t target = target_for(i), found = 0, hash = 0;
    char *empty = malloc(1); empty[0] = 0;
    search(num, target, 0, empty, 0, 0, 0, &found, &hash);
    free(empty);
    return (i * 1000003LL + found * 31LL + hash) % 1000000007LL;
}

struct arg { int64_t lo, hi, out; };
static void *worker(void *v) {
    struct arg *a = (struct arg *)v;
    int64_t s = 0;
    for (int64_t i = a->lo; i < a->hi; i++) s = (s + solve_one(i)) % 1000000007LL;
    a->out = s;
    return NULL;
}
int main(void) {
    pthread_t th[NTHREADS];
    struct arg args[NTHREADS];
    int64_t per = (INPUTS + NTHREADS - 1) / NTHREADS;
    for (int t = 0; t < NTHREADS; t++) {
        args[t].lo = t * per;
        args[t].hi = (t + 1) * per < INPUTS ? (t + 1) * per : INPUTS;
        if (args[t].lo > INPUTS) args[t].lo = INPUTS;
        args[t].out = 0;
        pthread_create(&th[t], NULL, worker, &args[t]);
    }
    int64_t sink = 0;
    for (int t = 0; t < NTHREADS; t++) { pthread_join(th[t], NULL); sink = (sink + args[t].out) % 1000000007LL; }
    printf("%lld\n", (long long)sink);
    return 0;
}
