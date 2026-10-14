// Benchmark for #543: C mirror of the ★ arm (heights, recursively); see
// diameter_of_binary_tree.kara. The nodes are malloc'd one at a time and
// never freed, as the trees live to the end.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left, *right;
} TreeNode;

static int64_t height(const TreeNode *node, int64_t *best) {
    if (!node) return 0;
    int64_t l = height(node->left, best);
    int64_t r = height(node->right, best);
    if (l + r > *best) *best = l + r;
    return 1 + (l > r ? l : r);
}

static int64_t diameter_of_binary_tree(const TreeNode *root) {
    int64_t best = 0;
    height(root, &best);
    return best;
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
    // added. Then 200 times over every tree the subtree at one of its
    // first 16 nodes, picked by the round and the tree, is answered.
    int64_t trees = 20, seed = 543;
    TreeNode ***all = malloc(trees * sizeof(TreeNode **));
    for (int64_t g = 0; g < trees; g++) {
        int64_t lean = 50 + 2 * g;
        all[g] = malloc(10000 * sizeof(TreeNode *));
        TreeNode *root = new_node(next_random(&seed) % 201 - 100);
        all[g][0] = root;
        for (int i = 1; i < 10000; i++) {
            TreeNode *c = new_node(next_random(&seed) % 201 - 100);
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
    for (int64_t r = 0; r < 200; r++) {
        for (int64_t t = 0; t < trees; t++) {
            int64_t d = diameter_of_binary_tree(all[t][(r * 37 + t * 11) % 16]);
            total += d;
            checksum = (checksum * 31 + d) % 1000000007;
        }
    }
    printf("%lld trees, 200 times each: diameters %lld, checksum %lld\n", (long long)trees,
           (long long)total, (long long)checksum);
    return 0;
}
