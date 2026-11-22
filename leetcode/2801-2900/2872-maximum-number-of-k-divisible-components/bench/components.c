// LeetCode #2872: Maximum Number of K-Divisible Components -- the bench,
// as components.kara: 30 trees of 3 * 10^4 nodes, each answered 20 times
// by the breadth-first arm. The adjacency is one array indexed by
// offsets, counted first, and everything is allocated on each call.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t max_k_divisible_components(int64_t n, const int64_t *edges, const int64_t *values, int64_t k) {
    int64_t *start = calloc(n + 1, sizeof *start), *adjacent = malloc(2 * (n - 1) * sizeof *adjacent);
    int64_t *fill = malloc(n * sizeof *fill), *parent = malloc(n * sizeof *parent);
    int64_t *order = malloc(n * sizeof *order), *rest = malloc(n * sizeof *rest);
    for (int64_t e = 0; e < n - 1; e++) {
        start[edges[2 * e] + 1]++;
        start[edges[2 * e + 1] + 1]++;
    }
    for (int64_t i = 0; i < n; i++) start[i + 1] += start[i];
    for (int64_t i = 0; i < n; i++) fill[i] = start[i], parent[i] = -1;
    for (int64_t e = 0; e < n - 1; e++) {
        int64_t a = edges[2 * e], b = edges[2 * e + 1];
        adjacent[fill[a]++] = b;
        adjacent[fill[b]++] = a;
    }
    int64_t len = 1;
    order[0] = 0;
    for (int64_t head = 0; head < len; head++) {
        int64_t u = order[head];
        for (int64_t j = start[u]; j < start[u + 1]; j++) {
            int64_t w = adjacent[j];
            if (w != parent[u]) {
                parent[w] = u;
                order[len++] = w;
            }
        }
    }
    for (int64_t i = 0; i < n; i++) rest[i] = values[i] % k;
    int64_t parts = 0;
    for (int64_t i = n - 1; i >= 0; i--) {
        int64_t u = order[i];
        if (rest[u] == 0) {
            parts++;
        } else if (parent[u] >= 0) {
            rest[parent[u]] = (rest[parent[u]] + rest[u]) % k;
        }
    }
    free(start);
    free(adjacent);
    free(fill);
    free(parent);
    free(order);
    free(rest);
    return parts;
}

static int64_t seed = 2872;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}
static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

int main(void) {
    enum { count = 30 };
    const int64_t rounds = 20, n = 30000;
    int64_t *edges = malloc(count * 2 * (n - 1) * sizeof *edges), *values = malloc(count * n * sizeof *values);
    int64_t ks[count];
    for (int64_t c = 0; c < count; c++) {
        ks[c] = next_random() % 9 + 2;
        for (int64_t v = 1; v < n; v++) {
            int64_t reach = c % 2 == 1 ? (v < 5 ? v : 5) : v;
            edges[c * 2 * (n - 1) + 2 * (v - 1)] = v - 1 - wide() % reach;
            edges[c * 2 * (n - 1) + 2 * (v - 1) + 1] = v;
        }
        int64_t sum = 0;
        for (int64_t i = 0; i < n; i++) sum += values[c * n + i] = wide() % 1000000001;
        values[c * n] += (ks[c] - sum % ks[c]) % ks[c];
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t c = 0; c < count; c++) {
            int64_t parts = max_k_divisible_components(n, edges + c * 2 * (n - 1), values + c * n, ks[c]);
            total += parts;
            check = (check * 31 + parts + r) % 1000000007;
        }
    }
    printf("%d trees of %lld, %lld rounds: %lld components, checksum %lld\n", count, (long long)n, (long long)rounds,
           (long long)total, (long long)check);
    free(edges);
    free(values);
    return 0;
}
