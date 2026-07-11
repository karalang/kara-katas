/*
 * Benchmark workload — Binary Tree Inorder Traversal (LeetCode #94).
 * C mirror of bench/inorder.kara. Each of K=320,000 iterations builds a fresh 63-node
 * balanced tree (malloc'd raw-pointer nodes — the metal floor, single-owner) and folds
 * a recursive inorder walk into a rolling hash in visit order. Nodes are freed after
 * each traversal. See ../README.md § Benchmarks.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left, *right;
} TreeNode;

static TreeNode *build(int64_t lo, int64_t hi, int64_t shift) {
    if (lo > hi) return NULL;
    int64_t mid = lo + (hi - lo) / 2;
    TreeNode *n = malloc(sizeof(TreeNode));
    n->val = shift + mid;
    n->left = build(lo, mid - 1, shift);
    n->right = build(mid + 1, hi, shift);
    return n;
}

static void inorder_fold(TreeNode *node, int64_t *acc) {
    if (!node) return;
    inorder_fold(node->left, acc);
    *acc = (*acc * 131 + (node->val + 1)) % 1000000007;
    inorder_fold(node->right, acc);
}

static void free_tree(TreeNode *node) {
    if (!node) return;
    free_tree(node->left);
    free_tree(node->right);
    free(node);
}

int main(void) {
    const int64_t total = 320000, modulus = 1000000007, size = 63;
    int64_t sum = 0;
    for (int64_t k = 0; k < total; k++) {
        int64_t shift = k % 1000;
        TreeNode *root = build(0, size - 1, shift);
        int64_t acc = 0;
        inorder_fold(root, &acc);
        sum = (sum * 131 + acc) % modulus;
        free_tree(root);
    }
    printf("%lld\n", (long long)sum);
    return 0;
}
