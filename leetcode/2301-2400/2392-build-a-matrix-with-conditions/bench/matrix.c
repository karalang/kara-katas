// LeetCode #2392: Build a Matrix With Conditions -- the bench, the ★ arm
// in C: Kahn's algorithm for the rows and again for the columns, the
// edges as a CSR array.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define K 200
#define CONDS 4000

static int64_t seed = 2392;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static void conditions(int64_t k, int64_t count, int64_t (*out)[2]) {
    int64_t order[K];
    for (int64_t i = 0; i < k; i++) order[i] = i + 1;
    for (int64_t i = 1; i < k; i++) {
        int64_t j = next_random() % (i + 1);
        int64_t t = order[i];
        order[i] = order[j];
        order[j] = t;
    }
    for (int64_t n = 0; n < count; n++) {
        int64_t a = next_random() % k;
        int64_t b = next_random() % (k - 1);
        if (b >= a) b++;
        int64_t lo = a < b ? a : b, hi = a < b ? b : a;
        out[n][0] = order[lo];
        out[n][1] = order[hi];
    }
}

// Taken numbers into `taken`; returns how many. Edges kept per source in
// the order given, as the other languages keep them.
static int64_t order_of(int64_t k, int64_t (*edges)[2], int64_t count, int64_t *taken) {
    int64_t *start = calloc(k + 2, sizeof(int64_t));
    int64_t *adj = malloc(sizeof(int64_t) * count);
    int64_t *into = calloc(k + 1, sizeof(int64_t));
    int64_t *fill = malloc(sizeof(int64_t) * (k + 2));
    for (int64_t n = 0; n < count; n++) {
        start[edges[n][0] + 1]++;
        into[edges[n][1]]++;
    }
    for (int64_t v = 1; v <= k + 1; v++) start[v] += start[v - 1];
    memcpy(fill, start, sizeof(int64_t) * (k + 2));
    for (int64_t n = 0; n < count; n++) adj[fill[edges[n][0]]++] = edges[n][1];
    int64_t *queue = malloc(sizeof(int64_t) * (k + 1));
    int64_t head = 0, tail = 0, len = 0;
    for (int64_t v = 1; v <= k; v++)
        if (into[v] == 0) queue[tail++] = v;
    while (head < tail) {
        int64_t v = queue[head++];
        taken[len++] = v;
        for (int64_t e = start[v]; e < start[v + 1]; e++) {
            int64_t w = adj[e];
            if (--into[w] == 0) queue[tail++] = w;
        }
    }
    free(start);
    free(adj);
    free(into);
    free(fill);
    free(queue);
    return len;
}

static int64_t *build_matrix(int64_t k, int64_t (*rows)[2], int64_t nr, int64_t (*cols)[2], int64_t nc) {
    int64_t by_row[K], by_col[K];
    if (order_of(k, rows, nr, by_row) < k || order_of(k, cols, nc, by_col) < k) return NULL;
    int64_t col_of[K + 1];
    for (int64_t c = 0; c < k; c++) col_of[by_col[c]] = c;
    int64_t *m = calloc(k * k, sizeof(int64_t));
    for (int64_t r = 0; r < k; r++) m[r * k + col_of[by_row[r]]] = by_row[r];
    return m;
}

int main(void) {
    static int64_t rows[20][CONDS][2], cols[20][CONDS][2];
    for (int i = 0; i < 20; i++) {
        conditions(K, CONDS, rows[i]);
        conditions(K, CONDS, cols[i]);
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 500; p++) {
        for (int i = 0; i < 20; i++) {
            int64_t *m = build_matrix(K, rows[i], CONDS, cols[i], CONDS);
            for (int64_t r = 0; r < K; r++)
                for (int64_t c = 0; c < K; c++)
                    if (m[r * K + c] > 0) check = (check * 31 + m[r * K + c] * (r * K + c) + p) % 1000000007;
            free(m);
        }
    }
    printf("500 passes over 20 matrices of k = 200: checksum %lld\n", (long long)check);
    return 0;
}
