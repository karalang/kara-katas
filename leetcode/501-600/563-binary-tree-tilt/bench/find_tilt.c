// Benchmark for #563: C mirror of the ★ arm (subtree sums, recursively);
// see find_tilt.kara. The nodes are malloc'd one at a time and
// never freed, as the trees live to the end.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left, *right;
} TreeNode;

static int64_t subtree_sum(const TreeNode *node, int64_t *total) {
    if (!node) return 0;
    int64_t l = subtree_sum(node->left, total);
    int64_t r = subtree_sum(node->right, total);
    *total += l > r ? l - r : r - l;
    return node->val + l + r;
}

static int64_t find_tilt(const TreeNode *root) {
    int64_t total = 0;
    subtree_sum(root, &total);
    return total;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static TreeNode *new_node(int64_t v) {
    TreeNode *n = malloc(sizeof(TreeNode));
    n->val = v;
    n->left = n->right = NULL;
    return n;
}

int main(void) {
    // 20 random trees of 10,000 nodes (the problem's most), each new
    // node walking down from the root and going left with chance 50 to
    // 88 in 100, built once, the nodes kept in the order they were
    // added. Then 1,000 times over every tree the subtree at one of its
    // first 16 nodes, picked by the round and the tree, is answered.
    int64_t trees = 20, seed = 563;
    TreeNode ***all = malloc(trees * sizeof(TreeNode **));
    for (int64_t g = 0; g < trees; g++) {
        int64_t lean = 50 + 2 * g;
        all[g] = malloc(10000 * sizeof(TreeNode *));
        TreeNode *root = new_node(next_random(&seed) % 2001 - 1000);
        all[g][0] = root;
        for (int i = 1; i < 10000; i++) {
            TreeNode *c = new_node(next_random(&seed) % 2001 - 1000);
            TreeNode *node = root;
            for (;;) {
                if (next_random(&seed) % 100 < lean) {
                    if (node->left) node = node->left;
                    else { node->left = c; break; }
                } else {
                    if (node->right) node = node->right;
                    else { node->right = c; break; }
                }
            }
            all[g][i] = c;
        }
    }
    int64_t total = 0, checksum = 0;
    for (int64_t r = 0; r < 1000; r++) {
        for (int64_t t = 0; t < trees; t++) {
            int64_t d = find_tilt(all[t][(r * 37 + t * 11) % 16]);
            total += d;
            checksum = (checksum * 31 + d) % 1000000007;
        }
    }
    printf("%lld trees, 1000 times each: tilts %lld, checksum %lld\n", (long long)trees,
           (long long)total, (long long)checksum);
    return 0;
}
