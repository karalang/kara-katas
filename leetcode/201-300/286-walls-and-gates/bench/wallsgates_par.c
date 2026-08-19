// pthreads mirror of wallsgates.kara's par lane — the metal floor for the PAR
// table. One thread per board, joined at the end, results reduced in main.
// The per-board algorithm is byte-for-byte the sequential mirror's.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>

#define INF 2147483647LL
#define BOARDS 16
#define R 512
#define C 512
#define REPS 8

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

typedef struct { long long b, total, unreachable; } Task;

static void *worker(void *arg) {
    Task *t = (Task *)arg;
    long long *template = make_board(t->b, (long long)R * C);
    for (int rep = 0; rep < REPS; rep++) {
        long long u = 0;
        t->total += solve(template, R, C, &u);
        t->unreachable += u;
    }
    free(template);
    return NULL;
}

int main(void) {
    pthread_t th[BOARDS];
    Task tasks[BOARDS];
    for (int b = 0; b < BOARDS; b++) {
        tasks[b].b = b;
        tasks[b].total = 0;
        tasks[b].unreachable = 0;
        pthread_create(&th[b], NULL, worker, &tasks[b]);
    }
    long long total = 0, unreachable = 0;
    for (int b = 0; b < BOARDS; b++) {
        pthread_join(th[b], NULL);
        total += tasks[b].total;
        unreachable += tasks[b].unreachable;
    }
    printf("%lld %lld\n", total, unreachable);
    return 0;
}
