// Benchmark for #671: a pruned walk, as the Kara ★ arm.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left;
    struct TreeNode *right;
} TreeNode;

static int64_t smallest_above(const TreeNode *n, int64_t low) {
    if (!n) {
        return -1;
    }
    if (n->val > low) {
        return n->val;
    }
    int64_t a = smallest_above(n->left, low);
    int64_t b = smallest_above(n->right, low);
    if (a == -1) {
        return b;
    }
    if (b == -1) {
        return a;
    }
    return a < b ? a : b;
}

static int64_t find_second_minimum_value(const TreeNode *root) {
    return root ? smallest_above(root, root->val) : -1;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static TreeNode *special(int64_t levels, int64_t val, int64_t spread, int64_t *seed) {
    TreeNode *n = malloc(sizeof(TreeNode));
    n->val = val;
    n->left = n->right = NULL;
    if (levels > 1) {
        int64_t other = val + next_random(seed) % (spread + 1);
        n->left = special(levels - 1, val, spread, seed);
        n->right = special(levels - 1, other, spread, seed);
    }
    return n;
}

static void free_tree(TreeNode *n) {
    if (n) {
        free_tree(n->left);
        free_tree(n->right);
        free(n);
    }
}

int main(void) {
    int64_t seed = 671;
    TreeNode *trees[16];
    for (int64_t t = 0; t < 16; t++) {
        int64_t spread = t % 4 == 0 ? 0 : t;
        trees[t] = special(16, 7 + t, spread, &seed);
    }
    int64_t rounds = 2000;
    int64_t sum = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t s = find_second_minimum_value(trees[r % 16]);
        sum = (sum * 31 + s + 1) % 1000000007;
    }
    printf("16 trees of 65535 nodes, %lld rounds: checksum %lld\n", (long long)rounds, (long long)sum);
    for (int t = 0; t < 16; t++) {
        free_tree(trees[t]);
    }
    return 0;
}
