// Benchmark for #776: Split BST -- mirror of the ★ arm (recursive), with
// the same workload as split_bst.kara. Each round's tree is freed.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left;
    struct TreeNode *right;
} TreeNode;

static void split_bst(TreeNode *root, int64_t target, TreeNode **small, TreeNode **large) {
    if (root == NULL) {
        *small = NULL;
        *large = NULL;
        return;
    }
    if (root->val <= target) {
        TreeNode *s, *l;
        split_bst(root->right, target, &s, &l);
        root->right = s;
        *small = root;
        *large = l;
    } else {
        TreeNode *s, *l;
        split_bst(root->left, target, &s, &l);
        root->left = l;
        *small = s;
        *large = root;
    }
}

static TreeNode *insert(TreeNode *root, int64_t v) {
    TreeNode *fresh = malloc(sizeof(TreeNode));
    fresh->val = v;
    fresh->left = NULL;
    fresh->right = NULL;
    if (root == NULL) {
        return fresh;
    }
    TreeNode *node = root;
    for (;;) {
        if (v < node->val) {
            if (node->left == NULL) {
                node->left = fresh;
                break;
            }
            node = node->left;
        } else {
            if (node->right == NULL) {
                node->right = fresh;
                break;
            }
            node = node->right;
        }
    }
    return root;
}

static int64_t weigh(const TreeNode *root, int64_t depth) {
    if (root == NULL) {
        return 0;
    }
    return root->val * depth + weigh(root->left, depth + 1) + weigh(root->right, depth + 1);
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
    const int count = 64;
    int64_t seed = 776;
    int64_t orders[64][50];
    int64_t targets[64];
    for (int g = 0; g < count; g++) {
        char used[1001] = {0};
        int len = 0;
        while (len < 50) {
            int64_t v = next_random(&seed) % 1001;
            if (!used[v]) {
                used[v] = 1;
                orders[g][len++] = v;
            }
        }
        targets[g] = next_random(&seed) % 1001;
    }
    int64_t checksum = 0;
    for (int64_t round = 0; round < 200000; round++) {
        int g = (int)(round % count);
        TreeNode *root = NULL;
        for (int i = 0; i < 50; i++) {
            root = insert(root, orders[g][i]);
        }
        TreeNode *small, *large;
        split_bst(root, targets[g], &small, &large);
        checksum = (checksum * 31 + weigh(small, 1) + 3 * weigh(large, 1)) % 1000000007;
        free_tree(small);
        free_tree(large);
    }
    printf("200000 rounds of 50 values: checksum %lld\n", (long long)checksum);
    return 0;
}
