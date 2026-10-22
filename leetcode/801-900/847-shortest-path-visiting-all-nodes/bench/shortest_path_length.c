// Benchmark for #847: Shortest Path Visiting All Nodes -- C twin of the
// Kāra ★ arm (breadth-first search over (visited set, node) states).
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

#define N 12

typedef struct {
    int64_t mask, v, steps;
} State;

static int64_t shortest_path_length(int64_t adj[][N], const int64_t *deg, int64_t n) {
    int64_t all = (1LL << n) - 1;
    char *seen = calloc((size_t)(n << n), 1);
    // every state is queued at most once, so the queue needs no wrapping
    State *queue = malloc(sizeof(State) * (size_t)(n << n));
    int64_t head = 0, tail = 0, answer = 0;
    for (int64_t v = 0; v < n; v++) {
        seen[(1LL << v) * n + v] = 1;
        queue[tail++] = (State){1LL << v, v, 0};
    }
    while (head < tail) {
        State s = queue[head++];
        if (s.mask == all) {
            answer = s.steps;
            break;
        }
        for (int64_t k = 0; k < deg[s.v]; k++) {
            int64_t w = adj[s.v][k];
            int64_t next = s.mask | (1LL << w);
            if (!seen[next * n + w]) {
                seen[next * n + w] = 1;
                queue[tail++] = (State){next, w, s.steps + 1};
            }
        }
    }
    free(queue);
    free(seen);
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    const int64_t count = 64, rounds = 4000, n = N;
    int64_t seed = 847;
    static int64_t adj[64][N][N];
    static int64_t deg[64][N];
    for (int64_t g = 0; g < count; g++) {
        char edge[N * N] = {0};
        for (int64_t v = 1; v < n; v++) {
            int64_t w = next_random(&seed) % v;
            edge[v * n + w] = edge[w * n + v] = 1;
        }
        for (int64_t e = 0; e < g % 16 * 3; e++) {
            int64_t v = next_random(&seed) % n;
            int64_t w = next_random(&seed) % n;
            if (v != w) edge[v * n + w] = edge[w * n + v] = 1;
        }
        for (int64_t v = 0; v < n; v++)
            for (int64_t w = 0; w < n; w++)
                if (edge[v * n + w]) adj[g][v][deg[g][v]++] = w;
    }
    int64_t total = 0, checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        int64_t length = shortest_path_length(adj[round % count], deg[round % count], n);
        total += length;
        checksum = (checksum * 31 + length) % 1000000007;
    }
    printf("%lld rounds of %lld graphs: lengths sum to %lld, checksum %lld\n", (long long)rounds,
           (long long)count, (long long)total, (long long)checksum);
    return 0;
}
