// Benchmark for #834: Sum of Distances in Tree -- the ★ arm (rerooting, with a stack).
//
// Mirrors sum_of_distances_in_tree.kara: one walk from node 0 on an
// explicit stack records parents and a visiting order; the order taken
// backwards gives subtree sizes and distance sums, and taken forwards
// moves the root along each edge. As in the Kāra program, the adjacency
// lists grow by doubling and every table is a fresh allocation per call.

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t *data;
    int64_t len, cap;
} Vec;

static void push(Vec *v, int64_t x) {
    if (v->len == v->cap) {
        v->cap = v->cap ? v->cap * 2 : 4;
        v->data = realloc(v->data, (size_t)v->cap * sizeof(int64_t));
    }
    v->data[v->len++] = x;
}

static int64_t *sum_of_distances_in_tree(int64_t n, const int64_t (*edges)[2], int64_t m) {
    Vec *adj = calloc((size_t)n, sizeof(Vec));
    for (int64_t k = 0; k < m; k++) {
        push(&adj[edges[k][0]], edges[k][1]);
        push(&adj[edges[k][1]], edges[k][0]);
    }
    int64_t *parent = malloc((size_t)n * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) parent[i] = -1;
    Vec order = {0, 0, 0};
    bool *seen = calloc((size_t)n, sizeof(bool));
    Vec stack = {0, 0, 0};
    push(&stack, 0);
    seen[0] = true;
    while (stack.len > 0) {
        int64_t u = stack.data[--stack.len];
        push(&order, u);
        for (int64_t k = 0; k < adj[u].len; k++) {
            int64_t v = adj[u].data[k];
            if (!seen[v]) {
                seen[v] = true;
                parent[v] = u;
                push(&stack, v);
            }
        }
    }
    int64_t *size = malloc((size_t)n * sizeof(int64_t));
    int64_t *down = malloc((size_t)n * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) {
        size[i] = 1;
        down[i] = 0;
    }
    for (int64_t j = 0; j < n; j++) {
        int64_t u = order.data[n - 1 - j];
        int64_t p = parent[u];
        if (p >= 0) {
            size[p] += size[u];
            down[p] += down[u] + size[u];
        }
    }
    int64_t *answer = calloc((size_t)n, sizeof(int64_t));
    answer[0] = down[0];
    for (int64_t j = 0; j < n; j++) {
        int64_t u = order.data[j];
        int64_t p = parent[u];
        if (p >= 0) answer[u] = answer[p] - size[u] + (n - size[u]);
    }
    for (int64_t i = 0; i < n; i++) free(adj[i].data);
    free(adj);
    free(parent);
    free(order.data);
    free(seen);
    free(stack.data);
    free(size);
    free(down);
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    // 16 trees drawn once, each of LeetCode's largest size, 30000 nodes:
    // node v > 0 hangs from a node among the `reach` before it, `reach`
    // running from 2 to 2^16 over the trees, with the labels shuffled.
    // Each round solves the next tree and reads one answer.
    enum { COUNT = 16, N = 30000 };
    const int64_t rounds = 320, n = N;
    int64_t seed = 834;
    static int64_t trees[COUNT][N - 1][2];
    static int64_t label[N];
    for (int64_t g = 0; g < COUNT; g++) {
        int64_t reach = (int64_t)2 << g;
        for (int64_t i = 0; i < n; i++) label[i] = i;
        int64_t i = n;
        while (i > 1) {
            int64_t j = next_random(&seed) % i;
            i -= 1;
            int64_t t = label[i];
            label[i] = label[j];
            label[j] = t;
        }
        for (int64_t v = 1; v < n; v++) {
            int64_t lo = v > reach ? v - reach : 0;
            int64_t u = lo + next_random(&seed) % (v - lo);
            trees[g][v - 1][0] = label[u];
            trees[g][v - 1][1] = label[v];
        }
    }
    int64_t total = 0, checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        int64_t *answer = sum_of_distances_in_tree(n, (const int64_t (*)[2])trees[round % COUNT], n - 1);
        int64_t x = answer[round * 7919 % n];
        free(answer);
        total += x;
        checksum = (checksum * 131 + x) % 1000000007;
    }
    printf("%lld rounds of %d trees: answers total %lld, checksum %lld\n", (long long)rounds, COUNT,
           (long long)total, (long long)checksum);
    return 0;
}
