// LeetCode #938: Range Sum of BST -- bench: recursion that skips
// subtrees. Mirrors range_sum_bst.kara, .rs, .py and go-seq/.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left;
    struct TreeNode *right;
} TreeNode;

static int64_t seed = 938;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static TreeNode *new_node(int64_t val) {
    TreeNode *n = malloc(sizeof(TreeNode));
    n->val = val;
    n->left = NULL;
    n->right = NULL;
    return n;
}

static int64_t range_sum_bst(const TreeNode *root, int64_t low, int64_t high) {
    if (root == NULL) {
        return 0;
    }
    if (root->val < low) {
        return range_sum_bst(root->right, low, high);
    }
    if (root->val > high) {
        return range_sum_bst(root->left, low, high);
    }
    return root->val + range_sum_bst(root->left, low, high) + range_sum_bst(root->right, low, high);
}

int main(void) {
    const int64_t rounds = 20;
    const int64_t count = 20;
    const int64_t queries = 50;
    TreeNode *trees[20];
    int64_t lows[20 * 50];
    int64_t highs[20 * 50];
    int64_t *pool = malloc(100000 * sizeof(int64_t));
    for (int64_t v = 1; v <= 100000; v++) {
        pool[v - 1] = v;
    }
    for (int64_t c = 0; c < count; c++) {
        for (int64_t i = 0; i < 20000; i++) {
            int64_t j = i + next_random() % (100000 - i);
            int64_t x = pool[i];
            pool[i] = pool[j];
            pool[j] = x;
        }
        TreeNode *root = new_node(pool[0]);
        for (int64_t i = 1; i < 20000; i++) {
            int64_t v = pool[i];
            TreeNode *cur = root;
            for (;;) {
                if (v < cur->val) {
                    if (cur->left == NULL) {
                        cur->left = new_node(v);
                        break;
                    }
                    cur = cur->left;
                } else {
                    if (cur->right == NULL) {
                        cur->right = new_node(v);
                        break;
                    }
                    cur = cur->right;
                }
            }
        }
        trees[c] = root;
        for (int64_t q = 0; q < queries; q++) {
            int64_t a = 1 + next_random() % 100000;
            int64_t b = 1 + next_random() % 100000;
            lows[c * queries + q] = a < b ? a : b;
            highs[c * queries + q] = a < b ? b : a;
        }
    }
    int64_t total = 0;
    int64_t check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t i = 0; i < count; i++) {
            int64_t c = (r + i) % count;
            for (int64_t q = 0; q < queries; q++) {
                int64_t s = range_sum_bst(trees[c], lows[c * queries + q], highs[c * queries + q]);
                total += s;
                check = (check * 1000003 + s) % 1000000007;
            }
        }
    }
    printf("%lld rounds over %lld trees of 20000 nodes, %lld ranges each: sums adding to %lld, "
           "checksum %lld\n",
           (long long)rounds, (long long)count, (long long)queries, (long long)total,
           (long long)check);
    return 0;
}
