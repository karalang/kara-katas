// LeetCode #2374: Node With Highest Edge Score -- the bench, the ★ arm in
// C: each node adds its label to the score of the node its edge points
// to, and the answer is the highest score's node, the smallest on a tie.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t edge_score(const int64_t *edges, int64_t n) {
    int64_t *score = calloc(n, sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) {
        score[edges[i]] += i;
    }
    int64_t best = 0;
    for (int64_t v = 1; v < n; v++) {
        if (score[v] > score[best]) {
            best = v;
        }
    }
    free(score);
    return best;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    // graph a: 10^5 nodes, each edge to one of the first 4^(a + 1) nodes
    // (at most all of them), another node than its own
    const int64_t n = 100000;
    int64_t seed = 2374;
    int64_t *graphs[10];
    int64_t width = 4;
    for (int a = 0; a < 10; a++) {
        graphs[a] = malloc(n * sizeof(int64_t));
        int64_t w = width < n ? width : n;
        for (int64_t i = 0; i < n; i++) {
            int64_t hi = next_random(&seed);
            int64_t e = (hi * 32768 + next_random(&seed)) % w;
            graphs[a][i] = e == i ? (e + 1) % n : e;
        }
        width *= 4;
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 50; p++) {
        for (int a = 0; a < 10; a++) {
            check = (check * 31 + edge_score(graphs[a], n) + p) % 1000000007;
        }
    }
    printf("50 passes over 10 graphs of 10^5 nodes: checksum %lld\n", (long long)check);
    for (int a = 0; a < 10; a++) {
        free(graphs[a]);
    }
    return 0;
}
