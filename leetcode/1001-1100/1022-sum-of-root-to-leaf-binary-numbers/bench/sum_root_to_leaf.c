// LeetCode #1022: Sum of Root To Leaf Binary Numbers -- bench
// Mirrors ./sum_root_to_leaf.kara; see ../README.md § Benchmarks.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left, *right;
} TreeNode;

static int64_t sum_from(const TreeNode *node, int64_t above) {
    if (!node) return 0;
    int64_t value = above * 2 + node->val;
    if (!node->left && !node->right) return value;
    return sum_from(node->left, value) + sum_from(node->right, value);
}

static int64_t sum_root_to_leaf(const TreeNode *root) { return sum_from(root, 0); }

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static TreeNode *new_node(int64_t val) {
    TreeNode *n = malloc(sizeof *n);
    n->val = val;
    n->left = n->right = NULL;
    return n;
}

static TreeNode *random_tree(int64_t *seed, int64_t n) {
    TreeNode *root = new_node(next_random(seed) % 2);
    int64_t placed = 1;
    while (placed < n) {
        TreeNode *node = root;
        int64_t level = 1;
        for (;;) {
            int go_left = next_random(seed) % 2 == 0;
            TreeNode *next = go_left ? node->left : node->right;
            if (next) {
                node = next;
                level += 1;
                if (level == 31) break;
            } else {
                TreeNode *leaf = new_node(next_random(seed) % 2);
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
    const int64_t count = 200, rounds = 500;
    int64_t seed = 1022, nodes = 0;
    TreeNode **trees = malloc(count * sizeof *trees);
    for (int64_t g = 0; g < count; g++) {
        int64_t n = next_random(&seed) % 1000 + 1;
        nodes += n;
        trees[g] = random_tree(&seed, n);
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t g = 0; g < count; g++) {
            int64_t answer = sum_root_to_leaf(trees[g]);
            total += answer;
            check = (check * 31 + answer) % 1000000007;
        }
    }
    printf("%lld trees, %lld nodes, %lld rounds: sum %lld, checksum %lld\n", (long long)count, (long long)nodes,
           (long long)rounds, (long long)total, (long long)check);
    return 0;
}
