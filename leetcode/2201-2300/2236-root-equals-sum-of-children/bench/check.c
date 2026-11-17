// LeetCode #2236: Root Equals Sum of Children -- the benchmark's C
// mirror of check.kara: 10^6 trees of three nodes, each node `malloc`ed,
// checked, and freed.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

struct TreeNode {
    int val;
    struct TreeNode *left;
    struct TreeNode *right;
};

static struct TreeNode *new_node(int val) {
    struct TreeNode *node = malloc(sizeof *node);
    node->val = val;
    node->left = NULL;
    node->right = NULL;
    return node;
}

static int check_tree(const struct TreeNode *root) {
    if (root == NULL || root->left == NULL || root->right == NULL) return 0;
    return root->val == root->left->val + root->right->val;
}

static struct TreeNode *tree(int64_t root, int64_t left, int64_t right) {
    struct TreeNode *node = new_node((int)root);
    node->left = new_node((int)left);
    node->right = new_node((int)right);
    return node;
}

static void free_tree(struct TreeNode *node) {
    if (node == NULL) return;
    free_tree(node->left);
    free_tree(node->right);
    free(node);
}

static int64_t seed = 2236;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int64_t holding = 0, check = 0;
    for (int i = 0; i < 1000000; i++) {
        int64_t left = next_random() % 101 - 50;
        int64_t right = next_random() % 101 - 50;
        int64_t root = left + right + next_random() % 3 - 1;
        struct TreeNode *t = tree(root, left, right);
        int holds = check_tree(t);
        free_tree(t);
        if (holds) holding++;
        check = (check * 2 + holds) % 1000000007;
    }
    printf("10^6 trees: %lld hold, checksum %lld\n", (long long)holding, (long long)check);
    return 0;
}
