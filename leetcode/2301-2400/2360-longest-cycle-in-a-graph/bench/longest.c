// LeetCode #2360: Longest Cycle in a Graph -- the bench, the ★ arm in C:
// each node stamped with the time it is first visited, and a walk that
// reaches a node stamped since it began has closed a cycle as long as the
// time between the two visits.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t longest_cycle(const int64_t *edges, int64_t n) {
    int64_t *stamp = malloc(n * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) {
        stamp[i] = -1;
    }
    int64_t time = 0;
    int64_t best = -1;
    for (int64_t start = 0; start < n; start++) {
        int64_t began = time;
        int64_t node = start;
        while (node != -1 && stamp[node] == -1) {
            stamp[node] = time;
            time++;
            node = edges[node];
        }
        if (node != -1 && stamp[node] >= began && time - stamp[node] > best) {
            best = time - stamp[node];
        }
    }
    free(stamp);
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
    // graph a: 10^5 nodes shuffled into one line, cut into pieces with a
    // chance of 1 in 2^(a + 4) at each link; each piece's last node points
    // back to its first with a chance of 1 in 2, and otherwise at a random
    // node
    const int64_t n = 100000;
    int64_t seed = 2360;
    int64_t *graphs[10];
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
        int64_t first = 0;
        for (int64_t i = 0; i < n; i++) {
            if (i == n - 1 || next_random(&seed) % cut == 0) {
                int64_t target = next_random(&seed) % 2 == 0 ? order[first] : wide_random(&seed) % n;
                if (target != order[i]) {
                    edges[order[i]] = target;
                }
                first = i + 1;
            } else {
                edges[order[i]] = order[i + 1];
            }
        }
        graphs[a] = edges;
    }
    free(order);
    int64_t check = 0;
    for (int64_t p = 0; p < 50; p++) {
        for (int a = 0; a < 10; a++) {
            check = (check * 31 + longest_cycle(graphs[a], n) + 2 + p) % 1000000007;
        }
    }
    printf("50 passes over 10 graphs of 10^5 nodes: checksum %lld\n", (long long)check);
    for (int a = 0; a < 10; a++) {
        free(graphs[a]);
    }
    return 0;
}
