// LeetCode #2359: Find Closest Node to Given Two Nodes -- the bench, the ★
// arm in C: each start's path walked for its distances, then every node
// both reach scanned for the least of the larger distance.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t *distances(const int64_t *edges, int64_t n, int64_t start) {
    int64_t *dist = malloc(n * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) {
        dist[i] = -1;
    }
    int64_t node = start;
    int64_t d = 0;
    while (node != -1 && dist[node] == -1) {
        dist[node] = d;
        node = edges[node];
        d++;
    }
    return dist;
}

static int64_t closest_meeting_node(const int64_t *edges, int64_t n, int64_t node1, int64_t node2) {
    int64_t *d1 = distances(edges, n, node1);
    int64_t *d2 = distances(edges, n, node2);
    int64_t best = -1;
    int64_t best_dist = -1;
    for (int64_t v = 0; v < n; v++) {
        if (d1[v] >= 0 && d2[v] >= 0) {
            int64_t far = d1[v] > d2[v] ? d1[v] : d2[v];
            if (best < 0 || far < best_dist) {
                best = v;
                best_dist = far;
            }
        }
    }
    free(d1);
    free(d2);
    return best;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t wide_random(int64_t *seed) {
    int64_t hi = next_random(seed);
    return hi * 32768 + next_random(seed);
}

int main(void) {
    // graph a: 10^5 nodes shuffled into one line, each link cut with a
    // chance of 1 in 2^(a + 4), the last node linked back to the first
    // when a is odd; 20 random pairs of starts in each
    const int64_t n = 100000;
    int64_t seed = 2359;
    int64_t *graphs[10];
    int64_t starts[10][40];
    int64_t *order = malloc(n * sizeof(int64_t));
    for (int64_t a = 0; a < 10; a++) {
        for (int64_t i = 0; i < n; i++) {
            order[i] = i;
        }
        for (int64_t i = n - 1; i >= 1; i--) {
            int64_t j = wide_random(&seed) % (i + 1);
            int64_t t = order[i];
            order[i] = order[j];
            order[j] = t;
        }
        int64_t cut = (int64_t)1 << (a + 4);
        int64_t *edges = malloc(n * sizeof(int64_t));
        for (int64_t i = 0; i < n; i++) {
            edges[i] = -1;
        }
        for (int64_t i = 0; i < n - 1; i++) {
            if (next_random(&seed) % cut != 0) {
                edges[order[i]] = order[i + 1];
            }
        }
        if (a % 2 == 1) {
            edges[order[n - 1]] = order[0];
        }
        graphs[a] = edges;
        for (int j = 0; j < 40; j++) {
            starts[a][j] = wide_random(&seed) % n;
        }
    }
    free(order);
    int64_t check = 0;
    for (int64_t p = 0; p < 10; p++) {
        for (int a = 0; a < 10; a++) {
            for (int j = 0; j < 20; j++) {
                int64_t m = closest_meeting_node(graphs[a], n, starts[a][2 * j], starts[a][2 * j + 1]);
                check = (check * 31 + m + 2 + p) % 1000000007;
            }
        }
    }
    printf("10 passes over 10 graphs of 10^5 nodes: checksum %lld\n", (long long)check);
    for (int a = 0; a < 10; a++) {
        free(graphs[a]);
    }
    return 0;
}
