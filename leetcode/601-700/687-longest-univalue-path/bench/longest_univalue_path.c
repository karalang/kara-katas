// LeetCode #687: Longest Univalue Path -- one walk, two arms per node.
// Bench.
//
// 100 random trees of up to 16 levels, values 1 and 2, are built once;
// then 30 rounds answer every tree.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left;
    struct TreeNode *right;
} TreeNode;

// The node's longest downward path of its own value, in edges; `best`
// takes the longest path that bends at the node.
static int64_t arm(const TreeNode *node, int64_t *best) {
    if (node == NULL) {
        return 0;
    }
    int64_t l = arm(node->left, best);
    int64_t r = arm(node->right, best);
    int64_t left = 0, right = 0;
    if (node->left != NULL && node->left->val == node->val) {
        left = l + 1;
    }
    if (node->right != NULL && node->right->val == node->val) {
        right = r + 1;
    }
    if (left + right > *best) {
        *best = left + right;
    }
    return left > right ? left : right;
}

static int64_t longest_univalue_path(const TreeNode *root) {
    int64_t best = 0;
    arm(root, &best);
    return best;
}

static int64_t seed = 687;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static TreeNode *random_tree(int64_t levels) {
    TreeNode *n = malloc(sizeof(TreeNode));
    n->val = 1 + next_random() % 2;
    n->left = NULL;
    n->right = NULL;
    if (levels > 1) {
        if (next_random() % 100 < 88) {
            n->left = random_tree(levels - 1);
        }
        if (next_random() % 100 < 88) {
            n->right = random_tree(levels - 1);
        }
    }
    return n;
}

static void free_tree(TreeNode *n) {
    if (n != NULL) {
        free_tree(n->left);
        free_tree(n->right);
        free(n);
    }
}

int main(void) {
    const int64_t count = 100, rounds = 30;
    TreeNode *trees[100];
    for (int64_t c = 0; c < count; c++) {
        trees[c] = random_tree(16);
    }
    int64_t sum = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t c = 0; c < count; c++) {
            int64_t k = longest_univalue_path(trees[c]);
            sum = (sum * 31 + k + r) % 1000000007;
        }
    }
    printf("%lld trees answered, checksum %lld\n", (long long)(count * rounds), (long long)sum);
    for (int64_t c = 0; c < count; c++) {
        free_tree(trees[c]);
    }
    return 0;
}
