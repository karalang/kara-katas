// LeetCode #700: Search in a Binary Search Tree -- bench program, C mirror of the loop arm.
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

static TreeNode *search_bst(TreeNode *root, int64_t val) {
    TreeNode *at = root;
    while (at != NULL) {
        if (val == at->val) {
            return at;
        }
        at = val < at->val ? at->left : at->right;
    }
    return NULL;
}

static TreeNode *leaf(int64_t v) {
    TreeNode *n = malloc(sizeof(TreeNode));
    n->val = v;
    n->left = NULL;
    n->right = NULL;
    return n;
}

static void insert(TreeNode *root, int64_t v) {
    TreeNode *at = root;
    for (;;) {
        if (v < at->val) {
            if (at->left != NULL) {
                at = at->left;
            } else {
                at->left = leaf(v);
                return;
            }
        } else {
            if (at->right != NULL) {
                at = at->right;
            } else {
                at->right = leaf(v);
                return;
            }
        }
    }
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
    int64_t seed = 700;
    const int64_t n = 50000;
    TreeNode *trees[10];
    int64_t *values = malloc(n * sizeof(int64_t));
    for (int t = 0; t < 10; t++) {
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
        TreeNode *root = leaf(values[0]);
        for (int64_t i = 1; i < n; i++) {
            insert(root, values[i]);
        }
        trees[t] = root;
    }
    const int64_t searches = 40000;
    int64_t *queries = malloc(searches * sizeof(int64_t));
    for (int64_t i = 0; i < searches; i++) {
        int64_t hi = next_random(&seed);
        int64_t lo = next_random(&seed);
        queries[i] = (hi * 32768 + lo) % (2 * n);
    }
    const int rounds = 5;
    int64_t found = 0;
    int64_t checksum = 0;
    for (int r = 0; r < rounds; r++) {
        for (int t = 0; t < 10; t++) {
            for (int64_t i = 0; i < searches; i++) {
                TreeNode *hit = search_bst(trees[t], queries[i]);
                if (hit != NULL) {
                    found += 1;
                    checksum = (checksum * 31 + hit->val) % 1000000007;
                }
            }
        }
    }
    printf("%d rounds of 10 trees of %lld, %lld searches each: %lld found, checksum %lld\n", rounds,
           (long long)n, (long long)searches, (long long)found, (long long)checksum);
    for (int t = 0; t < 10; t++) {
        free_tree(trees[t]);
    }
    free(values);
    free(queries);
    return 0;
}
