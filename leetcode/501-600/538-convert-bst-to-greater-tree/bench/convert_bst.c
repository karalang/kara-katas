// Benchmark for #538: C mirror of the ★ arm (reverse in order,
// recursively); see convert_bst.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left, *right;
} TreeNode;

static void visit(TreeNode *n, int64_t *total) {
    if (!n) return;
    visit(n->right, total);
    *total += n->val;
    n->val = *total;
    visit(n->left, total);
}

static TreeNode *convert_bst(TreeNode *root) {
    int64_t total = 0;
    visit(root, &total);
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

// A search tree of distinct values, inserted in the order given; every
// node is also listed in `nodes`, in the same order.
static TreeNode *build(const int64_t *values, int64_t len, TreeNode **nodes) {
    TreeNode *root = leaf(values[0]);
    nodes[0] = root;
    for (int64_t i = 1; i < len; i++) {
        int64_t v = values[i];
        TreeNode *node = root;
        for (;;) {
            if (v < node->val) {
                if (node->left) {
                    node = node->left;
                } else {
                    node->left = nodes[i] = leaf(v);
                    break;
                }
            } else {
                if (node->right) {
                    node = node->right;
                } else {
                    node->right = nodes[i] = leaf(v);
                    break;
                }
            }
        }
    }
    return root;
}

int main(void) {
    // 100 random search trees of 10,000 distinct values (the problem's
    // most) from -10,000 to 10,000, built once. Then 50 times over, each
    // tree has its values put back and is converted.
    int64_t trees = 100;
    int64_t seed = 538;
    int64_t pool[20001];
    for (int64_t v = 0; v < 20001; v++) pool[v] = v - 10000;
    TreeNode **roots = malloc(trees * sizeof(TreeNode *));
    TreeNode **lists = malloc(trees * 10000 * sizeof(TreeNode *));
    int64_t *originals = malloc(trees * 10000 * sizeof(int64_t));
    for (int64_t t = 0; t < trees; t++) {
        for (int64_t i = 0; i < 10000; i++) {
            int64_t high = next_random(&seed);
            int64_t j = i + (high * 32768 + next_random(&seed)) % (20001 - i);
            int64_t x = pool[i];
            pool[i] = pool[j];
            pool[j] = x;
        }
        for (int64_t i = 0; i < 10000; i++) originals[t * 10000 + i] = pool[i];
        roots[t] = build(&originals[t * 10000], 10000, &lists[t * 10000]);
    }
    int64_t total = 0, checksum = 0;
    for (int r = 0; r < 50; r++) {
        for (int64_t t = 0; t < trees; t++) {
            TreeNode **nodes = &lists[t * 10000];
            const int64_t *values = &originals[t * 10000];
            for (int64_t i = 0; i < 10000; i++) nodes[i]->val = values[i];
            int64_t top = convert_bst(roots[t])->val;
            total += top;
            checksum = (checksum * 31 + top + 1000000000) % 1000000007;
        }
    }
    printf("%lld trees of 10000 values, 50 times each: total %lld, checksum %lld\n",
           (long long)trees, (long long)total, (long long)checksum);
    return 0;
}
