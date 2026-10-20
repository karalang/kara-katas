// Benchmark for #814: Binary Tree Pruning -- mirror of the ★ arm
// (post-order recursion), with the same workload as prune_tree.kara. A
// pruned node is freed, and so is each round's tree.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left;
    struct TreeNode *right;
} TreeNode;

static TreeNode *prune_tree(TreeNode *root) {
    if (root == NULL) {
        return NULL;
    }
    root->left = prune_tree(root->left);
    root->right = prune_tree(root->right);
    if (root->val == 0 && root->left == NULL && root->right == NULL) {
        free(root);
        return NULL;
    }
    return root;
}

static TreeNode *build(const int64_t *vals, const int64_t *left, const int64_t *right, int64_t i) {
    if (i < 0) {
        return NULL;
    }
    TreeNode *l = build(vals, left, right, left[i]);
    TreeNode *r = build(vals, left, right, right[i]);
    TreeNode *node = malloc(sizeof(TreeNode));
    node->val = vals[i];
    node->left = l;
    node->right = r;
    return node;
}

static int64_t weigh(const TreeNode *root, int64_t depth) {
    if (root == NULL) {
        return 0;
    }
    return (root->val + 1) * depth + weigh(root->left, depth + 1) + weigh(root->right, depth + 1);
}

static void free_tree(TreeNode *root) {
    if (root != NULL) {
        free_tree(root->left);
        free_tree(root->right);
        free(root);
    }
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    enum { COUNT = 64, N = 200 };
    const int64_t rounds = 300000;
    int64_t seed = 814;
    static int64_t vals[COUNT][N], lefts[COUNT][N], rights[COUNT][N];
    for (int g = 0; g < COUNT; g++) {
        for (int i = 0; i < N; i++) {
            vals[g][i] = next_random(&seed) % 8 == 0 ? 1 : 0;
            lefts[g][i] = -1;
            rights[g][i] = -1;
        }
        for (int64_t i = 1; i < N; i++) {
            for (;;) {
                int64_t p = next_random(&seed) % i;
                if (next_random(&seed) % 2 == 0) {
                    if (lefts[g][p] < 0) {
                        lefts[g][p] = i;
                        break;
                    }
                } else if (rights[g][p] < 0) {
                    rights[g][p] = i;
                    break;
                }
            }
        }
    }
    int64_t checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        int g = (int)(round % COUNT);
        int64_t i = next_random(&seed) % N;
        vals[g][i] = 1 - vals[g][i];
        TreeNode *root = prune_tree(build(vals[g], lefts[g], rights[g], 0));
        checksum = (checksum * 31 + weigh(root, 1)) % 1000000007;
        free_tree(root);
    }
    printf("%lld rounds of %d nodes: checksum %lld\n", (long long)rounds, N, (long long)checksum);
    return 0;
}
