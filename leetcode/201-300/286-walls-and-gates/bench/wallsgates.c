// C mirror of wallsgates_seq.kara — see ../README.md § Benchmarks.
// Same LCG, same board parameters, same flat queue, same build-once/punch-many
// shape. Heap-allocated per board and per solve, matching what the Kara, Rust
// and Go lanes do; a stack buffer here would measure a different program.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define INF 2147483647LL

static long long *make_board(long long b, long long n) {
    long long *g = malloc((size_t)n * sizeof(long long));
    long long s = 777LL + b * 1013LL;
    for (long long i = 0; i < n; i++) {
        s = (s * 1103515245LL + 12345LL) % 2147483648LL;
        long long roll = s % 100LL;
        if (roll < 20) g[i] = -1;
        else if (roll < 21) g[i] = 0;
        else g[i] = INF;
    }
    return g;
}

static long long solve(const long long *template, long long r, long long c,
                       long long *out_unreachable) {
    long long n = r * c;
    long long *g = malloc((size_t)n * sizeof(long long));
    memcpy(g, template, (size_t)n * sizeof(long long));

    long long *q = malloc((size_t)n * sizeof(long long));
    long long tail = 0;
    for (long long k = 0; k < n; k++)
        if (g[k] == 0) q[tail++] = k;

    for (long long head = 0; head < tail; head++) {
        long long cell = q[head];
        long long row = cell / c, col = cell % c;
        long long d = g[cell] + 1;
        long long nb;
        if (row > 0)     { nb = cell - c; if (g[nb] == INF) { g[nb] = d; q[tail++] = nb; } }
        if (row < r - 1) { nb = cell + c; if (g[nb] == INF) { g[nb] = d; q[tail++] = nb; } }
        if (col > 0)     { nb = cell - 1; if (g[nb] == INF) { g[nb] = d; q[tail++] = nb; } }
        if (col < c - 1) { nb = cell + 1; if (g[nb] == INF) { g[nb] = d; q[tail++] = nb; } }
    }

    long long total = 0, unreachable = 0;
    for (long long j = 0; j < n; j++) {
        if (g[j] == INF) unreachable++;
        else if (g[j] > 0) total += g[j];
    }
    free(q);
    free(g);
    *out_unreachable = unreachable;
    return total;
}

typedef struct { long long total, unreachable; } BoardResult;

static BoardResult run_board(long long b, long long r, long long c, long long reps) {
    long long *template = make_board(b, r * c);
    BoardResult out = {0, 0};
    for (long long rep = 0; rep < reps; rep++) {
        long long u = 0;
        out.total += solve(template, r, c, &u);
        out.unreachable += u;
    }
    free(template);
    return out;
}

int main(void) {
    const long long boards = 16, r = 512, c = 512, reps = 8;
    long long total = 0, unreachable = 0;
    for (long long b = 0; b < boards; b++) {
        BoardResult part = run_board(b, r, c, reps);
        total += part.total;
        unreachable += part.unreachable;
    }
    printf("%lld %lld\n", total, unreachable);
    return 0;
}
