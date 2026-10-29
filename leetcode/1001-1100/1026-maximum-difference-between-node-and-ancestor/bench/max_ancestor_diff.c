// LeetCode #1026: Maximum Difference Between Node and Ancestor -- bench
// Mirrors ./max_ancestor_diff.kara; see ../README.md § Benchmarks.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left, *right;
} TreeNode;

static int64_t best_below(const TreeNode *node, int64_t low, int64_t high) {
    if (!node) return high - low;
    int64_t lo = node->val < low ? node->val : low;
    int64_t hi = node->val > high ? node->val : high;
    int64_t l = best_below(node->left, lo, hi);
    int64_t r = best_below(node->right, lo, hi);
    return l > r ? l : r;
}

static int64_t max_ancestor_diff(const TreeNode *root) {
    if (!root) return 0;
    return best_below(root, root->val, root->val);
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t random_value(int64_t *seed, int64_t top) {
    int64_t high = next_random(seed);
    return (high * 32768 + next_random(seed)) % top;
}

static TreeNode *new_node(int64_t val) {
    TreeNode *n = malloc(sizeof *n);
    n->val = val;
    n->left = n->right = NULL;
    return n;
}

static TreeNode *random_tree(int64_t *seed, int64_t n) {
    TreeNode *root = new_node(random_value(seed, 100001));
    int64_t placed = 1;
    while (placed < n) {
        TreeNode *node = root;
        for (;;) {
            int go_left = next_random(seed) % 2 == 0;
            TreeNode *next = go_left ? node->left : node->right;
            if (next) {
                node = next;
            } else {
                TreeNode *leaf = new_node(random_value(seed, 100001));
                if (go_left)
                    node->left = leaf;
                else
                    node->right = leaf;
                placed += 1;
                break;
            }
        }
    }
    return root;
}

int main(void) {
    const int64_t count = 200, rounds = 50;
    int64_t seed = 1026, nodes = 0;
    TreeNode **trees = malloc(count * sizeof *trees);
    for (int64_t g = 0; g < count; g++) {
        int64_t n = next_random(&seed) % 4999 + 2;
        nodes += n;
        trees[g] = random_tree(&seed, n);
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t g = 0; g < count; g++) {
            int64_t answer = max_ancestor_diff(trees[g]);
            total += answer;
            check = (check * 31 + answer) % 1000000007;
        }
    }
    printf("%lld trees, %lld nodes, %lld rounds: sum %lld, checksum %lld\n", (long long)count, (long long)nodes,
           (long long)rounds, (long long)total, (long long)check);
    return 0;
}
