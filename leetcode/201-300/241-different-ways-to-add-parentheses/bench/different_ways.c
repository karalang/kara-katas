/* Benchmark harness for LeetCode #241 — Different Ways to Add Parentheses.
 * Mirrors different_ways.kara algorithm-for-algorithm, including the
 * deliberately unmemoized recursion.
 *
 * The result vectors are heap-allocated per recursive call, exactly as the
 * Vec/Vec<i64>/slice the other four languages build. Using a shared scratch
 * arena would be faster but would not be the same algorithm.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define NP 6
#define NOPS 11
#define ITERS 30
#define MAXTOK 64

typedef struct {
    long long *v;
    long long n;
    long long cap;
} Vec;

static void vec_init(Vec *x) {
    x->cap = 8;
    x->n = 0;
    x->v = malloc(sizeof(long long) * (size_t)x->cap);
}

static void vec_push(Vec *x, long long val) {
    if (x->n == x->cap) {
        x->cap *= 2;
        x->v = realloc(x->v, sizeof(long long) * (size_t)x->cap);
    }
    x->v[x->n++] = val;
}

static void vec_free(Vec *x) { free(x->v); }

static long long tokenize(const char *expr, long long *tok) {
    long long ntok = 0;
    size_t i = 0;
    size_t n = strlen(expr);
    while (i < n) {
        long long b = (unsigned char)expr[i];
        if (b == 43 || b == 45 || b == 42) {
            tok[ntok++] = b;
            i++;
        } else {
            long long v = 0;
            while (i < n) {
                long long d = (unsigned char)expr[i];
                if (d >= 48 && d <= 57) {
                    v = v * 10 + (d - 48);
                    i++;
                } else {
                    break;
                }
            }
            tok[ntok++] = v;
        }
    }
    return ntok;
}

static Vec ways(const long long *tok, long long lo, long long hi) {
    Vec res;
    vec_init(&res);
    if (lo == hi) {
        vec_push(&res, tok[lo]);
        return res;
    }
    for (long long k = lo + 1; k < hi; k += 2) {
        long long op = tok[k];
        Vec left = ways(tok, lo, k - 1);
        Vec right = ways(tok, k + 1, hi);
        for (long long a = 0; a < left.n; a++) {
            for (long long b = 0; b < right.n; b++) {
                long long l = left.v[a];
                long long r = right.v[b];
                if (op == 43) {
                    vec_push(&res, l + r);
                } else if (op == 45) {
                    vec_push(&res, l - r);
                } else {
                    vec_push(&res, l * r);
                }
            }
        }
        vec_free(&left);
        vec_free(&right);
    }
    return res;
}

static long long toks[NP][MAXTOK];
static long long ntoks[NP];

int main(void) {
    const char *ops[3] = {"+", "-", "*"};
    char e[256];

    for (long long j = 0; j < NP; j++) {
        size_t p = 0;
        for (long long t = 0; t <= NOPS; t++) {
            p += (size_t)sprintf(e + p, "%lld", (t % 9) + 1);
            if (t < NOPS) {
                p += (size_t)sprintf(e + p, "%s", ops[(t + j) % 3]);
            }
        }
        e[p] = '\0';
        ntoks[j] = tokenize(e, toks[j]);
    }

    long long sink = 0;
    for (long long it = 0; it < ITERS; it++) {
        long long idx = (it * 5) % NP;
        Vec vals = ways(toks[idx], 0, ntoks[idx] - 1);
        for (long long v = 0; v < vals.n; v++) {
            sink += vals.v[v];
        }
        vec_free(&vals);
    }
    printf("%lld\n", sink);
    return 0;
}
