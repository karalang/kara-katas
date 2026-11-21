// LeetCode #2493: Divide Nodes Into the Maximum Number of Groups -- C
// mirror of the benchmark (groups.kara): the same graph, passes and
// checksum; adjacency in compressed rows built afresh on every ask, a
// breadth-first search from every node.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t seed = 2493;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t magnificent_sets(int64_t n, int64_t m, int64_t (*edges)[2]) {
    int64_t *start = calloc(n + 2, sizeof(int64_t));
    for (int64_t i = 0; i < m; i++) {
        start[edges[i][0] + 1]++;
        start[edges[i][1] + 1]++;
    }
    for (int64_t c = 1; c <= n + 1; c++) start[c] += start[c - 1];
    int64_t *fill = malloc((n + 1) * sizeof(int64_t));
    memcpy(fill, start, (n + 1) * sizeof(int64_t));
    int64_t *next = malloc((2 * m + 1) * sizeof(int64_t));
    for (int64_t i = 0; i < m; i++) {
        next[fill[edges[i][0]]++] = edges[i][1];
        next[fill[edges[i][1]]++] = edges[i][0];
    }
    int64_t *most = calloc(n + 1, sizeof(int64_t));
    int64_t *depth = malloc((n + 1) * sizeof(int64_t));
    int64_t *queue = malloc((n + 1) * sizeof(int64_t));
    int64_t answer = 0;
    for (int64_t s = 1; s <= n && answer >= 0; s++) {
        for (int64_t c = 0; c <= n; c++) depth[c] = -1;
        depth[s] = 0;
        int64_t len = 0, head = 0, least = s, deepest = 0;
        queue[len++] = s;
        while (head < len && answer >= 0) {
            int64_t node = queue[head++];
            if (node < least) least = node;
            if (depth[node] > deepest) deepest = depth[node];
            for (int64_t e = start[node]; e < start[node + 1]; e++) {
                int64_t other = next[e];
                if (depth[other] == -1) {
                    depth[other] = depth[node] + 1;
                    queue[len++] = other;
                } else if (depth[other] == depth[node]) {
                    answer = -1;
                    break;
                }
            }
        }
        if (deepest + 1 > most[least]) most[least] = deepest + 1;
    }
    if (answer >= 0)
        for (int64_t c = 0; c <= n; c++) answer += most[c];
    free(start); free(fill); free(next); free(most); free(depth); free(queue);
    return answer;
}

int main(void) {
    const int64_t n = 500, passes = 38;
    int64_t side[501];
    for (int64_t v = 1; v <= n; v++) side[v] = next_random() % 2;
    char *taken = calloc(501 * 1000 + 501, 1);
    int64_t (*edges)[2] = malloc(8000 * sizeof *edges);
    int64_t m = 0;
    for (int i = 0; i < 8000; i++) {
        int64_t a = next_random() % n + 1;
        int64_t b = next_random() % n + 1;
        int64_t lo = a < b ? a : b, hi = a < b ? b : a;
        if (a != b && side[a] != side[b] && !taken[lo * 1000 + hi]) {
            taken[lo * 1000 + hi] = 1;
            edges[m][0] = a; edges[m][1] = b; m++;
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < passes; p++) {
        check = (check * 31 + magnificent_sets(n, m - check % 100, edges) + p) % 1000000007;
    }
    printf("%lld passes over 500 nodes and %lld edges: checksum %lld\n",
           (long long)passes, (long long)m, (long long)check);
    free(taken); free(edges);
    return 0;
}
