/* LeetCode 284 bench mirror — C. Same eager wrapper, same two-peeks-per-next
 * mix, same sink plus pull count. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define N 200000
#define ROUNDS 320
typedef struct { int64_t *data; int64_t len, pos, pulls; } Source;
static int src_has_next(Source *s) { return s->pos < s->len; }
static int64_t src_next(Source *s) { int64_t v = s->data[s->pos]; s->pos++; s->pulls++; return v; }
typedef struct { Source src; int64_t slot; int full; } Peeking;
static Peeking make_peeking(int64_t *data, int64_t n) {
    Peeking p;
    p.src.data = malloc((size_t)n*sizeof(int64_t));
    memcpy(p.src.data, data, (size_t)n*sizeof(int64_t));
    p.src.len = n; p.src.pos = 0; p.src.pulls = 0;
    p.slot = 0; p.full = 0;
    if (src_has_next(&p.src)) { p.slot = src_next(&p.src); p.full = 1; }
    return p;
}
static int64_t peek(Peeking *p) { return p->slot; }
static int has_next(Peeking *p) { return p->full; }
static int64_t next_(Peeking *p) {
    int64_t v = p->slot;
    if (src_has_next(&p->src)) p->slot = src_next(&p->src); else p->full = 0;
    return v;
}
int main(void) {
    int64_t *data = malloc((size_t)N*sizeof(int64_t));
    int64_t seed = 20260823;
    for (int64_t i = 0; i < N; i++) { seed = (seed*1103515245LL+12345LL)%2147483648LL; data[i] = seed % 100003LL; }
    int64_t sink = 0, total = 0;
    for (int r = 0; r < ROUNDS; r++) {
        Peeking p = make_peeking(data, N);
        int64_t h = 0, pos = 1;
        while (has_next(&p)) {
            h = (h*31 + peek(&p)*pos) % 1000000007LL;
            h = (h*31 + peek(&p)) % 1000000007LL;
            int64_t v = next_(&p);
            h = (h*31 + v) % 1000000007LL;
            pos++;
        }
        total += p.src.pulls;
        free(p.src.data);
        sink = (sink + h) % 1000000007LL;
    }
    printf("%lld %lld\n", (long long)sink, (long long)total);
    return 0;
}
