// LeetCode #2331: Evaluate Boolean Binary Tree -- the bench, the ★ arm in
// C. A leaf is its own truth, and an OR or an AND node its two subtrees
// evaluated recursively and joined by `||` or `&&`, which stop at the
// first child that settles it. O(n). Nodes are `malloc`ed structs.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int32_t val;
    struct TreeNode *left, *right;
} TreeNode;

static bool evaluate_tree(const TreeNode *node) {
    if (node == NULL) return false;
    switch (node->val) {
    case 0: return false;
    case 1: return true;
    case 2: return evaluate_tree(node->left) || evaluate_tree(node->right);
    default: return evaluate_tree(node->left) && evaluate_tree(node->right);
    }
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static TreeNode *make(int32_t val, TreeNode *left, TreeNode *right) {
    TreeNode *node = malloc(sizeof(TreeNode));
    node->val = val;
    node->left = left;
    node->right = right;
    return node;
}

static TreeNode *random_tree(int64_t *seed, int64_t depth) {
    if (depth == 0 || next_random(seed) % 8 == 0) return make((int32_t)(next_random(seed) % 2), NULL, NULL);
    int32_t op = (int32_t)(next_random(seed) % 2 + 2);
    TreeNode *left = random_tree(seed, depth - 1);
    TreeNode *right = random_tree(seed, depth - 1);
    return make(op, left, right);
}

int main(void) {
    int64_t seed = 2331;
    TreeNode *trees[200];
    for (int k = 0; k < 200; k++) trees[k] = random_tree(&seed, 14);
    int64_t check = 0;
    for (int64_t p = 0; p < 500; p++)
        for (int k = 0; k < 200; k++) {
            int64_t truth = evaluate_tree(trees[k]) ? 1 : 2;
            check = (check * 3 + truth + p) % 1000000007LL;
        }
    printf("500 passes over 200 trees of depth up to 14: checksum %lld\n", (long long)check);
    return 0;
}
