// LeetCode #2368: Reachable Nodes With Restrictions -- the bench, the ★
// arm in C: the restricted nodes marked, and a breadth-first search from
// node 0 that never enters a marked node. C has no growable list, so the
// adjacency lists are laid out in one array by counting each node's
// degree first (compressed sparse rows), built afresh in each call.

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t reachable_nodes(int64_t n, const int64_t *ea, const int64_t *eb, int64_t m,
                               const int64_t *restricted, int64_t k) {
    int64_t *start = calloc(n + 1, sizeof(int64_t));
    for (int64_t i = 0; i < m; i++) {
        start[ea[i] + 1]++;
        start[eb[i] + 1]++;
    }
    for (int64_t v = 0; v < n; v++) {
        start[v + 1] += start[v];
    }
    int64_t *fill = malloc(n * sizeof(int64_t));
    for (int64_t v = 0; v < n; v++) {
        fill[v] = start[v];
    }
    int64_t *next = malloc(2 * m * sizeof(int64_t) + 1);
    for (int64_t i = 0; i < m; i++) {
        next[fill[ea[i]]++] = eb[i];
        next[fill[eb[i]]++] = ea[i];
    }
    bool *seen = calloc(n, sizeof(bool));
    for (int64_t i = 0; i < k; i++) {
        seen[restricted[i]] = true;
    }
    seen[0] = true;
    int64_t *queue = malloc(n * sizeof(int64_t));
    int64_t head = 0, tail = 0;
    queue[tail++] = 0;
    while (head < tail) {
        int64_t u = queue[head++];
        for (int64_t j = start[u]; j < start[u + 1]; j++) {
            int64_t v = next[j];
            if (!seen[v]) {
                seen[v] = true;
                queue[tail++] = v;
            }
        }
    }
    free(start);
    free(fill);
    free(next);
    free(seen);
    free(queue);
    return tail;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    // tree a: 10^5 nodes, node i joined to one of the 4^a nodes before it,
    // and each node but 0 restricted with a chance of 1 in 2^(a + 4)
    const int64_t n = 100000;
    int64_t seed = 2368;
    int64_t *ea[10], *eb[10], *rs[10], ks[10];
    int64_t width = 1;
    for (int a = 0; a < 10; a++) {
        ea[a] = malloc((n - 1) * sizeof(int64_t));
        eb[a] = malloc((n - 1) * sizeof(int64_t));
        for (int64_t i = 1; i < n; i++) {
            int64_t w = width < i ? width : i;
            ea[a][i - 1] = i - 1 - next_random(&seed) % w;
            eb[a][i - 1] = i;
        }
        rs[a] = malloc(n * sizeof(int64_t));
        ks[a] = 0;
        for (int64_t i = 1; i < n; i++) {
            if (next_random(&seed) % (16LL << a) == 0) {
                rs[a][ks[a]++] = i;
            }
        }
        width *= 4;
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 20; p++) {
        for (int a = 0; a < 10; a++) {
            check = (check * 31 + reachable_nodes(n, ea[a], eb[a], n - 1, rs[a], ks[a]) + p) % 1000000007;
        }
    }
    printf("20 passes over 10 trees of 10^5 nodes: checksum %lld\n", (long long)check);
    for (int a = 0; a < 10; a++) {
        free(ea[a]);
        free(eb[a]);
        free(rs[a]);
    }
    return 0;
}
