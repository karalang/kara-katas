// LeetCode 802 -- Find Eventual Safe States: the bench, mirroring
// eventual_safe_nodes.kara with the same three-colour search.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t n;
    int64_t **edges;
    int64_t *len;
} Graph;

static int64_t seed = 802;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int is_safe(const Graph *g, int64_t node, int64_t *colour) {
    if (colour[node] != 0) {
        return colour[node] == 2;
    }
    colour[node] = 1;
    for (int64_t i = 0; i < g->len[node]; i++) {
        if (!is_safe(g, g->edges[node][i], colour)) {
            return 0;
        }
    }
    colour[node] = 2;
    return 1;
}

// The safe nodes in increasing order; their count goes in *count.
static int64_t *eventual_safe_nodes(const Graph *g, int64_t *count) {
    int64_t n = g->n;
    int64_t *colour = calloc((size_t)n, sizeof(int64_t));
    int64_t *safe = malloc((size_t)n * sizeof(int64_t));
    int64_t k = 0;
    for (int64_t node = 0; node < n; node++) {
        if (is_safe(g, node, colour)) {
            safe[k++] = node;
        }
    }
    free(colour);
    *count = k;
    return safe;
}

static int cmp(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

int main(void) {
    int64_t n = 10000;
    Graph graphs[16];
    for (int g = 0; g < 16; g++) {
        graphs[g].n = n;
        graphs[g].edges = malloc((size_t)n * sizeof(int64_t *));
        graphs[g].len = malloc((size_t)n * sizeof(int64_t));
        for (int64_t a = 0; a < n; a++) {
            int64_t picked[4];
            int64_t np = 0;
            int64_t edges = next_random() % 5;
            for (int64_t e = 0; e < edges; e++) {
                int64_t b;
                if (next_random() % 1000 == 0) {
                    b = a - 1 - next_random() % 50;
                    if (b < 0) {
                        b = 0;
                    }
                } else {
                    b = a + 1 + next_random() % 50;
                }
                if (b < n) {
                    picked[np++] = b;
                }
            }
            // In increasing order with no edge twice, as LeetCode gives.
            qsort(picked, (size_t)np, sizeof(int64_t), cmp);
            int64_t *out = malloc((size_t)(np > 0 ? np : 1) * sizeof(int64_t));
            int64_t k = 0;
            for (int64_t i = 0; i < np; i++) {
                if (k == 0 || out[k - 1] != picked[i]) {
                    out[k++] = picked[i];
                }
            }
            graphs[g].edges[a] = out;
            graphs[g].len[a] = k;
        }
    }
    int64_t rounds = 4000;
    int64_t total = 0;
    int64_t check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t count;
        int64_t *safe = eventual_safe_nodes(&graphs[r % 16], &count);
        total += count;
        check = (check * 131 + count + safe[count / 2]) % 1000000007;
        free(safe);
    }
    printf("%lld rounds of %lld nodes: %lld safe nodes in all, checksum %lld\n", (long long)rounds,
           (long long)n, (long long)total, (long long)check);
    return 0;
}
