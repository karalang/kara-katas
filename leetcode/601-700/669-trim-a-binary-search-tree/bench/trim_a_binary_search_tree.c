// Benchmark for #669: recursion, in place, as the Kara ★ arm.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left;
    struct TreeNode *right;
} TreeNode;

static void free_tree(TreeNode *n) {
    if (n) {
        free_tree(n->left);
        free_tree(n->right);
        free(n);
    }
}

// Trimmed-away nodes are freed as they go, the work Kara's and Rust's
// reference counts do when the last handle to a node drops.
static TreeNode *trim_bst(TreeNode *root, int64_t low, int64_t high) {
    if (!root) {
        return NULL;
    }
    if (root->val < low) {
        TreeNode *r = trim_bst(root->right, low, high);
        free_tree(root->left);
        free(root);
        return r;
    }
    if (root->val > high) {
        TreeNode *l = trim_bst(root->left, low, high);
        free_tree(root->right);
        free(root);
        return l;
    }
    root->left = trim_bst(root->left, low, high);
    root->right = trim_bst(root->right, low, high);
    return root;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static TreeNode *leaf(int64_t v) {
    TreeNode *n = malloc(sizeof(TreeNode));
    n->val = v;
    n->left = n->right = NULL;
    return n;
}

static TreeNode *bst(const int64_t *values, int64_t count) {
    TreeNode *root = leaf(values[0]);
    for (int64_t i = 1; i < count; i++) {
        int64_t v = values[i];
        TreeNode *at = root;
        for (;;) {
            TreeNode **next = v < at->val ? &at->left : &at->right;
            if (!*next) {
                *next = leaf(v);
                break;
            }
            at = *next;
        }
    }
    return root;
}

static int64_t checksum(TreeNode *root) {
    int64_t sum = 0;
    TreeNode **stack = malloc(10000 * sizeof(TreeNode *));
    int64_t top = 0;
    if (root) {
        stack[top++] = root;
    }
    while (top > 0) {
        TreeNode *n = stack[--top];
        sum = (sum * 31 + n->val) % 1000000007;
        if (n->right) {
            stack[top++] = n->right;
        }
        if (n->left) {
            stack[top++] = n->left;
        }
    }
    free(stack);
    return sum;
}

int main(void) {
    int64_t seed = 669;
    static int64_t order[10000];
    for (int64_t i = 0; i < 10000; i++) {
        order[i] = i;
    }
    for (int64_t i = 1; i < 10000; i++) {
        int64_t j = next_random(&seed) % (i + 1);
        int64_t t = order[i];
        order[i] = order[j];
        order[j] = t;
    }
    int64_t rounds = 300;
    int64_t sum = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t low = r * 37 % 10000;
        int64_t high = low + r * 53 % 5000;
        TreeNode *kept = trim_bst(bst(order, 10000), low, high);
        sum = (sum * 31 + checksum(kept)) % 1000000007;
        free_tree(kept);
    }
    printf("10000 nodes, %lld rounds: checksum %lld\n", (long long)rounds, (long long)sum);
    return 0;
}
