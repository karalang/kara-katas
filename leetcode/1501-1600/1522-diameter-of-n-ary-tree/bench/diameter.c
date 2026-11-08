// LeetCode #1522: Diameter of N-Ary Tree -- bench: the ★ arm over 1000
// random trees of 1 to 2000 nodes, built once and answered 20 times.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int64_t val;
    int64_t count;
    struct Node **children;
} Node;

static int64_t height(const Node *node, int64_t *best) {
    int64_t first = 0, second = 0;
    for (int64_t i = 0; i < node->count; i++) {
        int64_t h = height(node->children[i], best) + 1;
        if (h > first) {
            second = first;
            first = h;
        } else if (h > second) {
            second = h;
        }
    }
    if (first + second > *best) {
        *best = first + second;
    }
    return first;
}

static int64_t diameter(const Node *root) {
    int64_t best = 0;
    height(root, &best);
    return best;
}

static int64_t seed = 1522;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) {
    return (check * 31 + x + 1) % 1000000007;
}

int main(void) {
    enum { COUNT = 1000 };
    static Node *trees[COUNT];
    for (int t = 0; t < COUNT; t++) {
        int64_t n = next_random() % 2000 + 1;
        int64_t window = next_random() % 64 + 1;
        Node *nodes = malloc((size_t)n * sizeof(Node));
        int64_t *parent = malloc((size_t)n * sizeof(int64_t));
        for (int64_t i = 0; i < n; i++) {
            nodes[i].val = next_random() % 1000;
            nodes[i].count = 0;
            nodes[i].children = NULL;
            parent[i] = -1;
            if (i > 0) {
                int64_t span = i < window ? i : window;
                parent[i] = i - 1 - next_random() % span;
                nodes[parent[i]].count++;
            }
        }
        int64_t *filled = calloc((size_t)n, sizeof(int64_t));
        for (int64_t i = 0; i < n; i++) {
            if (nodes[i].count > 0) {
                nodes[i].children = malloc((size_t)nodes[i].count * sizeof(Node *));
            }
        }
        for (int64_t i = 1; i < n; i++) {
            int64_t p = parent[i];
            nodes[p].children[filled[p]++] = &nodes[i];
        }
        free(filled);
        free(parent);
        trees[t] = nodes;
    }
    int64_t check = 0, total = 0;
    for (int pass = 0; pass < 20; pass++) {
        for (int t = 0; t < COUNT; t++) {
            int64_t d = diameter(trees[t]);
            total += d;
            check = mix(check, d);
        }
    }
    printf("20 passes over 1000 trees of up to 2000 nodes: diameters sum to %lld, checksum %lld\n",
           (long long)total, (long long)check);
    return 0;
}
