// LeetCode #1666: Change the Root of a Binary Tree -- the bench's C
// mirror: the ★ arm on 30 random trees of 100000 nodes with parent links,
// each turned 50000 times to hang from a leaf reached by a random walk
// down from a random node, the start nodes drawn first. Every node is
// malloc'd on its own.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define TREES 30
#define NODES 100000
#define TURNS 50000

struct Node {
    int32_t val;
    struct Node *left;
    struct Node *right;
    struct Node *parent;
};

static struct Node *flip_binary_tree(struct Node *root, struct Node *leaf) {
    (void)root;
    struct Node *cur = leaf, *below = NULL;
    for (;;) {
        struct Node *p = cur->parent;
        cur->parent = below;
        if (!p) break;
        if (p->left == cur) p->left = NULL;
        else p->right = NULL;
        if (cur->left) cur->right = cur->left;
        cur->left = p;
        below = cur;
        cur = p;
    }
    return leaf;
}

static int64_t seed = 1666;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static void random_tree(int64_t n, struct Node **nodes) {
    int32_t *values = malloc((size_t)n * sizeof *values);
    for (int64_t i = 0; i < n; i++) values[i] = (int32_t)i;
    for (int64_t i = n - 1; i >= 1; i--) {
        int64_t j = next_random() % (i + 1);
        int32_t t = values[i];
        values[i] = values[j];
        values[j] = t;
    }
    for (int64_t i = 0; i < n; i++) {
        struct Node *node = calloc(1, sizeof *node);
        node->val = values[i];
        if (i > 0) {
            struct Node *at = nodes[next_random() % i];
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
    static int32_t starts[TREES][TURNS];
    for (int t = 0; t < TREES; t++) {
        random_tree(NODES, nodes[t]);
        for (int k = 0; k < TURNS; k++) starts[t][k] = (int32_t)(next_random() % NODES);
    }
    int64_t check = 0, steps = 0;
    for (int t = 0; t < TREES; t++) {
        struct Node *root = nodes[t][0];
        for (int k = 0; k < TURNS; k++) {
            struct Node *at = nodes[t][starts[t][k]];
            for (;;) {
                struct Node *first = next_random() % 2 == 0 ? at->left : at->right;
                struct Node *child = first ? first : at->left ? at->left : at->right;
                if (!child) break;
                at = child;
                steps++;
            }
            root = flip_binary_tree(root, at);
            check = (check * 31 + root->val + 1) % 1000000007;
        }
    }
    for (int t = 0; t < TREES; t++)
        for (int i = 0; i < NODES; i++) free(nodes[t][i]);
    printf("30 trees of 100000 nodes, 50000 turns each: %lld steps down, checksum %lld\n", (long long)steps, (long long)check);
    return 0;
}
