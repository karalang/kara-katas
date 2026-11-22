// LeetCode #2867: Count Valid Paths in a Tree -- the bench, as
// paths.kara: 10 trees of 10^5 nodes, each answered 10 times by the
// disjoint-set arm. Each prime's neighbours sit in one array indexed
// by offsets, counted first, where the others push onto a list per
// node; everything is allocated on each call.

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t find(int64_t *parent, int64_t x) {
    int64_t root = x;
    while (parent[root] != root) root = parent[root];
    while (parent[x] != root) {
        int64_t next = parent[x];
        parent[x] = root;
        x = next;
    }
    return root;
}

static int64_t count_paths(int64_t n, const int64_t *edges) {
    bool *prime = malloc(n + 1);
    for (int64_t i = 0; i <= n; i++) prime[i] = i >= 2;
    for (int64_t i = 2; i * i <= n; i++)
        if (prime[i])
            for (int64_t j = i * i; j <= n; j += i) prime[j] = false;
    int64_t *parent = malloc((n + 1) * sizeof *parent), *size = malloc((n + 1) * sizeof *size);
    int64_t *start = calloc(n + 2, sizeof *start), *around = malloc(2 * n * sizeof *around);
    for (int64_t i = 0; i <= n; i++) parent[i] = i, size[i] = 1;
    for (int64_t e = 0; e < n - 1; e++) {
        int64_t a = edges[2 * e], b = edges[2 * e + 1];
        if (prime[a] || prime[b]) {
            start[a + 1]++;
            start[b + 1]++;
        } else {
            int64_t ra = find(parent, a), rb = find(parent, b);
            if (ra != rb) {
                parent[ra] = rb;
                size[rb] += size[ra];
            }
        }
    }
    for (int64_t i = 0; i <= n; i++) start[i + 1] += start[i];
    int64_t *fill = malloc((n + 1) * sizeof *fill);
    for (int64_t i = 0; i <= n; i++) fill[i] = start[i];
    for (int64_t e = 0; e < n - 1; e++) {
        int64_t a = edges[2 * e], b = edges[2 * e + 1];
        if (prime[a] || prime[b]) {
            around[fill[a]++] = b;
            around[fill[b]++] = a;
        }
    }
    int64_t count = 0;
    for (int64_t p = 2; p <= n; p++) {
        if (!prime[p]) continue;
        int64_t before = 0;
        for (int64_t k = start[p]; k < start[p + 1]; k++) {
            int64_t v = around[k];
            if (!prime[v]) {
                int64_t s = size[find(parent, v)];
                count += s + s * before;
                before += s;
            }
        }
    }
    free(prime);
    free(parent);
    free(size);
    free(start);
    free(around);
    free(fill);
    return count;
}

static int64_t seed = 2867;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}
static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

int main(void) {
    const int64_t count = 10, rounds = 10, n = 100000;
    int64_t *trees = malloc(count * 2 * (n - 1) * sizeof *trees);
    for (int64_t c = 0; c < count; c++) {
        int64_t *edges = trees + c * 2 * (n - 1);
        for (int64_t v = 2; v <= n; v++) {
            int64_t reach = c % 2 == 1 ? (v - 1 < 5 ? v - 1 : 5) : v - 1;
            edges[2 * (v - 2)] = v - 1 - wide() % reach;
            edges[2 * (v - 2) + 1] = v;
        }
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t c = 0; c < count; c++) {
            int64_t paths = count_paths(n, trees + c * 2 * (n - 1));
            total += paths;
            check = (check * 31 + paths % 1000000007 + r) % 1000000007;
        }
    }
    printf("%lld trees of %lld, %lld rounds: %lld paths, checksum %lld\n", (long long)count, (long long)n,
           (long long)rounds, (long long)total, (long long)check);
    free(trees);
    return 0;
}
