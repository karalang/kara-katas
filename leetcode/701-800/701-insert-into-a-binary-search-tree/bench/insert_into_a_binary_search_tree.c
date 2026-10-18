// LeetCode #701: Insert into a Binary Search Tree -- bench program, C mirror of the loop arm.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left;
    struct TreeNode *right;
} TreeNode;

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static TreeNode *insert_into_bst(TreeNode *root, int64_t val) {
    TreeNode *fresh = malloc(sizeof(TreeNode));
    fresh->val = val;
    fresh->left = NULL;
    fresh->right = NULL;
    if (root == NULL) {
        return fresh;
    }
    TreeNode *at = root;
    for (;;) {
        if (val < at->val) {
            if (at->left != NULL) {
                at = at->left;
            } else {
                at->left = fresh;
                return root;
            }
        } else {
            if (at->right != NULL) {
                at = at->right;
            } else {
                at->right = fresh;
                return root;
            }
        }
    }
}

typedef struct {
    TreeNode *node;
    int64_t depth;
} Frame;

static int64_t height(TreeNode *root, Frame *stack) {
    int64_t best = 0;
    int64_t top = 0;
    if (root != NULL) {
        stack[top++] = (Frame){root, 1};
    }
    while (top > 0) {
        Frame f = stack[--top];
        if (f.depth > best) {
            best = f.depth;
        }
        if (f.node->right != NULL) {
            stack[top++] = (Frame){f.node->right, f.depth + 1};
        }
        if (f.node->left != NULL) {
            stack[top++] = (Frame){f.node->left, f.depth + 1};
        }
    }
    return best;
}

static void free_tree(TreeNode *n) {
    if (n == NULL) {
        return;
    }
    free_tree(n->left);
    free_tree(n->right);
    free(n);
}

int main(void) {
    int64_t seed = 701;
    const int64_t n = 50000;
    int64_t *orders[10];
    for (int t = 0; t < 10; t++) {
        int64_t *values = malloc(n * sizeof(int64_t));
        for (int64_t i = 0; i < n; i++) {
            values[i] = 2 * i;
        }
        for (int64_t i = 1; i < n; i++) {
            int64_t hi = next_random(&seed);
            int64_t lo = next_random(&seed);
            int64_t j = (hi * 32768 + lo) % (i + 1);
            int64_t tmp = values[i];
            values[i] = values[j];
            values[j] = tmp;
        }
        orders[t] = values;
    }
    Frame *stack = malloc(n * sizeof(Frame));
    const int rounds = 5;
    int64_t total = 0;
    int64_t checksum = 0;
    for (int r = 0; r < rounds; r++) {
        for (int t = 0; t < 10; t++) {
            TreeNode *root = NULL;
            for (int64_t i = 0; i < n; i++) {
                root = insert_into_bst(root, orders[t][i]);
            }
            int64_t h = height(root, stack);
            total += h;
            checksum = (checksum * 31 + h) % 1000000007;
            free_tree(root);
        }
    }
    printf("%d rounds of 10 trees grown to %lld: heights sum to %lld, checksum %lld\n", rounds,
           (long long)n, (long long)total, (long long)checksum);
    for (int t = 0; t < 10; t++) {
        free(orders[t]);
    }
    free(stack);
    return 0;
}
