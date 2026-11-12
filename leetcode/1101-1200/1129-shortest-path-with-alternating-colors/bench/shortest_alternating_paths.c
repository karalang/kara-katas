// LeetCode #1129: Shortest Path with Alternating Colors -- the bench in C,
// the same algorithm and workload as shortest_alternating_paths.kara: each
// edge a two-number array allocated by itself, the adjacency built per
// call as growable lists per node and colour, a breadth-first search over
// (node, colour) with an array queue, the same 32 graphs and 1000 rounds.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct { int64_t *items; int64_t len, cap; } List;

static void push(List *l, int64_t x) {
    if (l->len == l->cap) {
        l->cap = l->cap ? 2 * l->cap : 4;
        l->items = realloc(l->items, l->cap * sizeof(int64_t));
    }
    l->items[l->len++] = x;
}

static int64_t *shortest_alternating_paths(int64_t n, int64_t **red, int64_t nr, int64_t **blue, int64_t nb) {
    List *adj[2] = { calloc(n, sizeof(List)), calloc(n, sizeof(List)) };
    for (int64_t k = 0; k < nr; k++) push(&adj[0][red[k][0]], red[k][1]);
    for (int64_t k = 0; k < nb; k++) push(&adj[1][blue[k][0]], blue[k][1]);
    int64_t *dist[2] = { malloc(n * sizeof(int64_t)), malloc(n * sizeof(int64_t)) };
    for (int64_t i = 0; i < n; i++) dist[0][i] = dist[1][i] = -1;
    dist[0][0] = 0;
    dist[1][0] = 0;
    int64_t *qnode = malloc(2 * n * sizeof(int64_t));
    int64_t *qcolour = malloc(2 * n * sizeof(int64_t));
    int64_t head = 0, tail = 0;
    qnode[tail] = 0; qcolour[tail++] = 0;
    qnode[tail] = 0; qcolour[tail++] = 1;
    while (head < tail) {
        int64_t node = qnode[head], colour = qcolour[head++];
        int64_t next = 1 - colour;
        List *l = &adj[next][node];
        for (int64_t k = 0; k < l->len; k++) {
            int64_t m = l->items[k];
            if (dist[next][m] < 0) {
                dist[next][m] = dist[colour][node] + 1;
                qnode[tail] = m; qcolour[tail++] = next;
            }
        }
    }
    int64_t *answer = malloc(n * sizeof(int64_t));
    for (int64_t x = 0; x < n; x++) {
        int64_t a = dist[0][x], b = dist[1][x];
        answer[x] = a < 0 ? b : b < 0 ? a : (a < b ? a : b);
    }
    for (int c = 0; c < 2; c++) {
        for (int64_t i = 0; i < n; i++) free(adj[c][i].items);
        free(adj[c]);
        free(dist[c]);
    }
    free(qnode);
    free(qcolour);
    return answer;
}

static int64_t seed = 1129;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t **edges(int64_t n, int64_t m) {
    int64_t **out = malloc(m * sizeof(int64_t *));
    for (int64_t k = 0; k < m; k++) {
        int64_t a = next_random() % n;
        int64_t b = next_random() % n;
        out[k] = malloc(2 * sizeof(int64_t));
        out[k][0] = a;
        out[k][1] = b;
    }
    return out;
}

int main(void) {
    int64_t **reds[32], **blues[32];
    for (int j = 0; j < 32; j++) {
        reds[j] = edges(100, 400);
        blues[j] = edges(100, 400);
    }
    int64_t total = 0, check = 0;
    for (int64_t round = 0; round < 1000; round++) {
        for (int64_t j = 0; j < 32; j++) {
            int64_t at = (round * 7919 + j * 104729) % 400;
            int64_t **e = round % 2 == 0 ? reds[j] : blues[j];
            e[at][1] = (e[at][1] + 1 + round % 7) % 100;
            int64_t *answer = shortest_alternating_paths(100, reds[j], 400, blues[j], 400);
            for (int64_t x = 0; x < 100; x++) {
                total += answer[x];
                check = (check * 31 + answer[x] + 2) % 1000000007;
            }
            free(answer);
        }
    }
    printf("1000 rounds over 32 graphs of 100 nodes and 400 edges of each colour: lengths total %lld, checksum %lld\n",
           (long long)total, (long long)check);
    for (int j = 0; j < 32; j++) {
        for (int k = 0; k < 400; k++) { free(reds[j][k]); free(blues[j][k]); }
        free(reds[j]);
        free(blues[j]);
    }
    return 0;
}
