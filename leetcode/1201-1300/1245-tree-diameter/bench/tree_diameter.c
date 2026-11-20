// LeetCode #1245 bench, in C: the ★ arm (two breadth-first searches over
// an adjacency list, kept as each node's neighbours packed in one array
// behind per-node offsets, with an array queue) on 100 random trees of
// 10000 nodes built once, each asked 5 times; every diameter folded into a
// checksum.

#include <stdio.h>
#include <stdlib.h>

#define N 10000
#define TREES 100

static long long seed = 1245;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static void random_tree(long long n, long long shape, long long *edges) {
    static long long label[N];
    for (long long i = 0; i < n; i++) label[i] = i;
    for (long long i = n - 1; i >= 1; i--) {
        long long j = next_random() % (i + 1);
        long long t = label[i];
        label[i] = label[j];
        label[j] = t;
    }
    for (long long v = 1; v < n; v++) {
        long long parent;
        if (shape == 0) parent = next_random() % v;
        else if (shape == 1) parent = v - 1 - next_random() % (v < 3 ? v : 3);
        else parent = next_random() % (v < 4 ? v : 4);
        edges[2 * (v - 1)] = label[parent];
        edges[2 * (v - 1) + 1] = label[v];
    }
}

static long long start[N + 1], adj[2 * N], fill[N], dist[N], queue[N];

static long long farthest(long long n, long long from, long long *far) {
    for (long long i = 0; i < n; i++) dist[i] = -1;
    long long head = 0, tail = 0, last = from;
    dist[from] = 0;
    queue[tail++] = from;
    while (head < tail) {
        long long node = queue[head++];
        last = node;
        for (long long k = start[node]; k < start[node + 1]; k++) {
            long long next = adj[k];
            if (dist[next] < 0) {
                dist[next] = dist[node] + 1;
                queue[tail++] = next;
            }
        }
    }
    *far = dist[last];
    return last;
}

static long long tree_diameter(const long long *edges, long long m) {
    long long n = m + 1;
    for (long long i = 0; i <= n; i++) start[i] = 0;
    for (long long e = 0; e < 2 * m; e++) start[edges[e] + 1]++;
    for (long long i = 0; i < n; i++) start[i + 1] += start[i];
    for (long long i = 0; i < n; i++) fill[i] = start[i];
    for (long long e = 0; e < m; e++) {
        long long a = edges[2 * e], b = edges[2 * e + 1];
        adj[fill[a]++] = b;
        adj[fill[b]++] = a;
    }
    long long d;
    long long end = farthest(n, 0, &d);
    farthest(n, end, &d);
    return d;
}

int main(void) {
    long long *trees = malloc(sizeof(long long) * TREES * 2 * (N - 1));
    for (int t = 0; t < TREES; t++) random_tree(N, t % 3, trees + (long long)t * 2 * (N - 1));
    long long check = 0;
    for (int r = 0; r < 5; r++)
        for (int t = 0; t < TREES; t++)
            check = (check * 131 + tree_diameter(trees + (long long)t * 2 * (N - 1), N - 1)) % 1000000007;
    printf("5 rounds of 100 trees of 10000 nodes: checksum %lld\n", check);
    free(trees);
    return 0;
}
