// LeetCode #1650: Lowest Common Ancestor of a Binary Tree III -- the
// bench's C mirror: the ★ arm on 30 random trees of 100000 nodes with
// parent links, each asked about 50000 pairs of its nodes, all drawn
// first. Every node is malloc'd on its own.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define TREES 30
#define NODES 100000
#define PAIRS 50000

struct Node {
    int32_t val;
    struct Node *left;
    struct Node *right;
    struct Node *parent;
};

static struct Node *lowest_common_ancestor(struct Node *p, struct Node *q) {
    struct Node *a = p, *b = q;
    while (a->val != b->val) {
        a = a->parent ? a->parent : q;
        b = b->parent ? b->parent : p;
    }
    return a;
}

static int64_t seed = 1650;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

static void random_tree(int64_t n, struct Node **nodes) {
    int32_t *values = malloc((size_t)n * sizeof *values);
    for (int64_t i = 0; i < n; i++) values[i] = (int32_t)i;
    for (int64_t i = n - 1; i >= 1; i--) {
        int64_t j = wide() % (i + 1);
        int32_t t = values[i];
        values[i] = values[j];
        values[j] = t;
    }
    for (int64_t i = 0; i < n; i++) {
        struct Node *node = calloc(1, sizeof *node);
        node->val = values[i];
        if (i > 0) {
            struct Node *at = nodes[wide() % i];
            for (;;) {
                if (next_random() % 2 == 0) {
                    if (at->left) at = at->left;
                    else { node->parent = at; at->left = node; break; }
                } else {
                    if (at->right) at = at->right;
                    else { node->parent = at; at->right = node; break; }
                }
            }
        }
        nodes[i] = node;
    }
    free(values);
}

int main(void) {
    static struct Node *nodes[TREES][NODES];
    static int32_t pairs[TREES][PAIRS][2];
    for (int t = 0; t < TREES; t++) {
        random_tree(NODES, nodes[t]);
        for (int k = 0; k < PAIRS; k++) {
            int64_t p = wide() % NODES;
            int64_t q = wide() % NODES;
            if (q == p) q = (q + 1) % NODES;
            pairs[t][k][0] = (int32_t)p;
            pairs[t][k][1] = (int32_t)q;
        }
    }
    int64_t check = 0, total = 0;
    for (int t = 0; t < TREES; t++) {
        for (int k = 0; k < PAIRS; k++) {
            int64_t found = lowest_common_ancestor(nodes[t][pairs[t][k][0]], nodes[t][pairs[t][k][1]])->val;
            total += found;
            check = (check * 31 + found + 1) % 1000000007;
        }
    }
    for (int t = 0; t < TREES; t++)
        for (int i = 0; i < NODES; i++) free(nodes[t][i]);
    printf("30 trees of 100000 nodes, 50000 pairs each: answers sum to %lld, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
