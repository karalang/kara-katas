// LeetCode #2415: Reverse Odd Levels of Binary Tree -- the bench, the ★ arm
// in C: mirror pairs walked down together, the values of each pair on an
// odd level swapped.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int32_t val;
    struct TreeNode *left, *right;
} TreeNode;

static void swap_pairs(TreeNode *a, TreeNode *b, int odd) {
    if (a && b) {
        if (odd) {
            int32_t t = a->val;
            a->val = b->val;
            b->val = t;
        }
        swap_pairs(a->left, b->right, !odd);
        swap_pairs(a->right, b->left, !odd);
    }
}

static TreeNode *reverse_odd_levels(TreeNode *root) {
    if (root) swap_pairs(root->left, root->right, 1);
    return root;
}

static int64_t seed = 2415;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t edge(TreeNode *root, int left) {
    TreeNode *at = root;
    for (;;) {
        TreeNode *next = left ? at->left : at->right;
        if (!next) return at->val;
        at = next;
    }
}

int main(void) {
    TreeNode *pools[10];
    for (int t = 0; t < 10; t++) {
        TreeNode *nodes = malloc(16383 * sizeof(TreeNode));
        for (int i = 0; i < 16383; i++) {
            int64_t hi = next_random();
            int64_t lo = next_random();
            nodes[i].val = (int32_t)((hi * 32768 + lo) % 100000);
            nodes[i].left = nodes[i].right = NULL;
        }
        for (int i = 0; i < 8191; i++) {
            nodes[i].left = &nodes[2 * i + 1];
            nodes[i].right = &nodes[2 * i + 2];
        }
        pools[t] = nodes;
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 1000; p++) {
        for (int t = 0; t < 10; t++) {
            TreeNode *r = reverse_odd_levels(&pools[t][0]);
            check = (check * 31 + r->left->val + p) % 1000000007;
            check = (check * 31 + r->right->val + edge(r, 1) + edge(r, 0)) % 1000000007;
        }
    }
    printf("1000 passes over 10 trees of 2^14 - 1 nodes: checksum %lld\n", (long long)check);
    for (int t = 0; t < 10; t++) free(pools[t]);
    return 0;
}
