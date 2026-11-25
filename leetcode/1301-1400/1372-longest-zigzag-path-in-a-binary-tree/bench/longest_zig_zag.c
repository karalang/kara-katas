// LeetCode #1372 bench -- C: one walk up from the leaves, each node
// reporting the longest zigzag starting at it going left and going right,
// each one more than its child's the other way.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define TREES 20
#define NODES 50000
#define ROUNDS 300

typedef struct TreeNode {
    int val;
    struct TreeNode *left;
    struct TreeNode *right;
} TreeNode;

typedef struct {
    int64_t left, right;
} Lengths;

// the longest zigzag from `node` going left first, going right first
static Lengths lengths(const TreeNode *node, int64_t *best) {
    Lengths out = {0, 0};
    if (node->left) out.left = 1 + lengths(node->left, best).right;
    if (node->right) out.right = 1 + lengths(node->right, best).left;
    if (out.left > *best) *best = out.left;
    if (out.right > *best) *best = out.right;
    return out;
}

static int32_t longest_zig_zag(const TreeNode *root) {
    int64_t best = 0;
    if (root) lengths(root, &best);
    return (int32_t)best;
}

static int64_t seed = 1372;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

typedef struct {
    TreeNode *node;
    bool left;
} Place;

static TreeNode *new_node(void) {
    TreeNode *n = malloc(sizeof *n);
    n->val = 1;
    n->left = n->right = NULL;
    return n;
}

static void hang(Place *free, size_t *count, size_t k) {
    Place p = free[k];
    free[k] = free[--*count];
    TreeNode *node = new_node();
    if (p.left) {
        p.node->left = node;
    } else {
        p.node->right = node;
    }
    free[(*count)++] = (Place){node, true};
    free[(*count)++] = (Place){node, false};
}

int main(void) {
    // 20 trees of 5 * 10^4 nodes, the constraints' most, each node hung
    // on a random empty child place, built once; then 300 rounds, each
    // hanging one more leaf on one tree, on a place drawn from the
    // checksum so far, and finding that tree's longest zigzag
    static TreeNode *roots[TREES];
    static Place *places[TREES];
    static size_t counts[TREES];
    for (int t = 0; t < TREES; t++) {
        roots[t] = new_node();
        places[t] = malloc(sizeof(Place) * (2 * (NODES + ROUNDS) + 2));
        counts[t] = 0;
        places[t][counts[t]++] = (Place){roots[t], true};
        places[t][counts[t]++] = (Place){roots[t], false};
        for (int i = 1; i < NODES; i++) hang(places[t], &counts[t], (size_t)(next_random() % (int64_t)counts[t]));
    }
    int64_t check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        int64_t t = check % 20;
        hang(places[t], &counts[t], (size_t)((check / 20) % (int64_t)counts[t]));
        int64_t got = longest_zig_zag(roots[t]);
        check = (check * 31 + got + r) % 1000000007;
    }
    printf("300 rounds over 20 trees of 50000 nodes: checksum %lld\n", (long long)check);
    return 0;
}
