// LeetCode #1382 bench -- C: the ★ arm: the values read off in order,
// then a new tree built with the middle value at the root and each half
// built the same way beneath it. Nodes from malloc, a replaced tree freed.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int val;
    struct TreeNode *left, *right;
} TreeNode;

static TreeNode *new_node(int val) {
    TreeNode *n = malloc(sizeof(TreeNode));
    n->val = val;
    n->left = n->right = NULL;
    return n;
}

static void free_tree(TreeNode *n) {
    if (!n) return;
    free_tree(n->left);
    free_tree(n->right);
    free(n);
}

static void values_in_order(TreeNode *node, int *values, int *count) {
    if (!node) return;
    values_in_order(node->left, values, count);
    values[(*count)++] = node->val;
    values_in_order(node->right, values, count);
}

static TreeNode *build(const int *values, int lo, int hi) {
    if (lo >= hi) return NULL;
    int mid = (lo + hi) / 2;
    TreeNode *n = new_node(values[mid]);
    n->left = build(values, lo, mid);
    n->right = build(values, mid + 1, hi);
    return n;
}

static int scratch[10000];

static TreeNode *balance_bst(TreeNode *root) {
    int count = 0;
    values_in_order(root, scratch, &count);
    return build(scratch, 0, count);
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static TreeNode *search_tree(const int *values, int n) {
    TreeNode *root = new_node(values[0]);
    for (int i = 1; i < n; i++) {
        int v = values[i];
        TreeNode *at = root;
        for (;;) {
            TreeNode **next = v < at->val ? &at->left : &at->right;
            if (*next) {
                at = *next;
            } else {
                *next = new_node(v);
                break;
            }
        }
    }
    return root;
}

int main(void) {
    int64_t seed = 1382;
    TreeNode *trees[10];
    static int values[10000];
    for (int t = 0; t < 10; t++) {
        int64_t step = 1 + next_random(&seed) % 99990;
        int64_t start = next_random(&seed) % 99991;
        for (int64_t k = 0; k < 10000; k++) values[k] = (int)(1 + (start + k * step) % 99991);
        for (int i = 9999; i >= 1; i--) {
            int j = (int)(next_random(&seed) % (i + 1));
            int tmp = values[i];
            values[i] = values[j];
            values[j] = tmp;
        }
        trees[t] = search_tree(values, 10000);
    }
    int64_t check = 0;
    for (int round = 0; round < 500; round++) {
        int t = (int)((check + next_random(&seed)) % 10);
        TreeNode *balanced = balance_bst(trees[t]);
        for (TreeNode *at = balanced; at;) {
            check = (check * 131 + at->val) % 1000000007;
            at = next_random(&seed) % 2 == 0 ? at->left : at->right;
        }
        free_tree(trees[t]);
        trees[t] = balanced;
    }
    printf("500 rounds over 10 trees of 10000 nodes: checksum %lld\n", (long long)check);
    for (int t = 0; t < 10; t++) free_tree(trees[t]);
    return 0;
}
