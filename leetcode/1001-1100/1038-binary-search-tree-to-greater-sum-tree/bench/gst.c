// LeetCode #1038: Binary Search Tree to Greater Sum Tree -- bench
// Mirrors ../gst.kara; see ../README.md § Benchmarks. Plain pointers,
// never freed.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left, *right;
} TreeNode;

static int64_t add_greater(TreeNode *n, int64_t above) {
    if (!n) return above;
    int64_t total = add_greater(n->right, above) + n->val;
    n->val = total;
    return add_greater(n->left, total);
}

static TreeNode *bst_to_gst(TreeNode *root) {
    add_greater(root, 0);
    return root;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static TreeNode *leaf(int64_t v) {
    TreeNode *n = malloc(sizeof(TreeNode));
    n->val = v;
    n->left = n->right = NULL;
    return n;
}

// A search tree of the keys, inserted in the order given; every node is
// also listed in `nodes`, in the same order.
static TreeNode *build(const int64_t *keys, int64_t count, TreeNode **nodes) {
    TreeNode *root = leaf(keys[0]);
    nodes[0] = root;
    for (int64_t i = 1; i < count; i++) {
        int64_t v = keys[i];
        TreeNode *fresh = leaf(v);
        nodes[i] = fresh;
        TreeNode *node = root;
        for (;;) {
            if (v < node->val) {
                if (node->left) node = node->left;
                else { node->left = fresh; break; }
            } else {
                if (node->right) node = node->right;
                else { node->right = fresh; break; }
            }
        }
    }
    return root;
}

int main(void) {
    const int64_t trees = 10000, rounds = 50;
    int64_t seed = 1038;
    int64_t pool[101];
    for (int64_t v = 0; v < 101; v++) pool[v] = v;
    TreeNode **roots = malloc(trees * sizeof(TreeNode *));
    TreeNode **lists = malloc(trees * 100 * sizeof(TreeNode *));
    int64_t *originals = malloc(trees * 100 * sizeof(int64_t));
    for (int64_t t = 0; t < trees; t++) {
        for (int64_t i = 0; i < 100; i++) {
            int64_t j = i + next_random(&seed) % (101 - i);
            int64_t s = pool[i]; pool[i] = pool[j]; pool[j] = s;
        }
        for (int64_t i = 0; i < 100; i++) originals[t * 100 + i] = pool[i];
        roots[t] = build(&originals[t * 100], 100, &lists[t * 100]);
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t t = 0; t < trees; t++) {
            TreeNode **nodes = &lists[t * 100];
            const int64_t *keys = &originals[t * 100];
            for (int64_t i = 0; i < 100; i++) nodes[i]->val = keys[i];
            int64_t top = bst_to_gst(roots[t])->val;
            total += top;
            check = (check * 31 + top + 1000) % 1000000007;
        }
    }
    printf("%lld trees of 100 keys, %lld rounds: total %lld, checksum %lld\n",
           (long long)trees, (long long)rounds, (long long)total, (long long)check);
    return 0;
}
