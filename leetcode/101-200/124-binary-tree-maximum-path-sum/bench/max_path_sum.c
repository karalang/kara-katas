/* LeetCode #124 benchmark mirror (C) — raw-pointer binary tree, the metal floor.
 * Same algorithm and tree construction as the Kara/Rust/Go/Python mirrors. */
#include <stdio.h>
#include <stdlib.h>

#define TREE_COUNT 2048
#define NODE_COUNT 511
#define REPS 60

typedef struct TreeNode {
    long val;
    struct TreeNode *left;
    struct TreeNode *right;
} TreeNode;

static long node_value(long i, long seed) {
    return ((i * 37 + seed * 13) % 41) - 20;
}

static TreeNode *build_balanced(long lo, long hi, long seed) {
    if (lo > hi) return NULL;
    long mid = (lo + hi) / 2;
    TreeNode *node = (TreeNode *)malloc(sizeof(TreeNode));
    node->val = node_value(mid, seed);
    node->left = build_balanced(lo, mid - 1, seed);
    node->right = build_balanced(mid + 1, hi, seed);
    return node;
}

static long max_gain(TreeNode *node, long *best) {
    if (node == NULL) return 0;
    long lg = max_gain(node->left, best);
    long rg = max_gain(node->right, best);
    long left_gain = lg > 0 ? lg : 0;
    long right_gain = rg > 0 ? rg : 0;
    long through = node->val + left_gain + right_gain;
    if (through > *best) *best = through;
    long branch = left_gain > right_gain ? left_gain : right_gain;
    return node->val + branch;
}

static long max_path_sum(TreeNode *root) {
    long best = -1000000000L;
    max_gain(root, &best);
    return best;
}

int main(void) {
    TreeNode **forest = (TreeNode **)malloc(sizeof(TreeNode *) * TREE_COUNT);
    for (long t = 0; t < TREE_COUNT; t++)
        forest[t] = build_balanced(0, NODE_COUNT - 1, t + 1);

    long sink = 0;
    for (long k = 0; k < REPS; k++)
        for (long i = 0; i < TREE_COUNT; i++)
            sink += max_path_sum(forest[i]);

    printf("%ld\n", sink);
    return 0;
}
