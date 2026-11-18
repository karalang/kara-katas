// LeetCode #2277: Closest Node to Path in Tree -- the bench, the ★ arm.
// Adjacency as a CSR: offsets per node into one array of neighbours.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static void distances(int64_t n, const int64_t *off, const int64_t *nbr, int64_t from, int64_t *dist, int64_t *queue) {
    for (int64_t i = 0; i < n; i++) dist[i] = -1;
    dist[from] = 0;
    int64_t head = 0, tail = 0;
    queue[tail++] = from;
    while (head < tail) {
        int64_t v = queue[head++];
        for (int64_t k = off[v]; k < off[v + 1]; k++) {
            int64_t w = nbr[k];
            if (dist[w] < 0) {
                dist[w] = dist[v] + 1;
                queue[tail++] = w;
            }
        }
    }
}

static void closest_node(int64_t n, const int64_t (*edges)[2], int64_t m, const int64_t (*query)[3], int64_t q, int64_t *answer) {
    int64_t *deg = calloc(n + 1, sizeof(int64_t));
    for (int64_t i = 0; i < m; i++) {
        deg[edges[i][0]]++;
        deg[edges[i][1]]++;
    }
    int64_t *off = malloc((n + 1) * sizeof(int64_t));
    off[0] = 0;
    for (int64_t v = 0; v < n; v++) off[v + 1] = off[v] + deg[v];
    int64_t *fill = calloc(n, sizeof(int64_t));
    int64_t *nbr = malloc((2 * m + 1) * sizeof(int64_t));
    for (int64_t i = 0; i < m; i++) {
        int64_t a = edges[i][0], b = edges[i][1];
        nbr[off[a] + fill[a]++] = b;
        nbr[off[b] + fill[b]++] = a;
    }
    int64_t *dist = malloc(n * n * sizeof(int64_t));
    int64_t *queue = malloc(n * sizeof(int64_t));
    for (int64_t v = 0; v < n; v++) distances(n, off, nbr, v, dist + v * n, queue);
    for (int64_t i = 0; i < q; i++) {
        int64_t start = query[i][0], end = query[i][1], node = query[i][2];
        int64_t best = start;
        for (int64_t u = 0; u < n; u++) {
            if (dist[start * n + u] + dist[u * n + end] == dist[start * n + end] && dist[u * n + node] < dist[best * n + node]) best = u;
        }
        answer[i] = best;
    }
    free(deg); free(off); free(fill); free(nbr); free(dist); free(queue);
}

// ---- bench harness ---------------------------------------------------------

static int64_t seed = 2277;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t check = 0;
    static int64_t edges[999][2];
    static int64_t query[1000][3];
    static int64_t answer[1000];
    for (int t = 0; t < 50; t++) {
        for (int64_t i = 1; i < 1000; i++) {
            edges[i - 1][0] = i;
            edges[i - 1][1] = next_random() % i;
        }
        for (int i = 0; i < 1000; i++) {
            query[i][0] = next_random() % 1000;
            query[i][1] = next_random() % 1000;
            query[i][2] = next_random() % 1000;
        }
        closest_node(1000, edges, 999, query, 1000, answer);
        for (int i = 0; i < 1000; i++) check = (check * 31 + answer[i]) % 1000000007;
    }
    printf("50 trees of 1000: checksum %lld\n", (long long)check);
    return 0;
}
