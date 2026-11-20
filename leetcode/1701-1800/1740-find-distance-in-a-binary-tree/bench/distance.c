// LeetCode #1740: Find Distance in a Binary Tree -- the bench's C mirror:
// the ★ arm on one tree of 10000 nodes asked about 1000 pairs of values,
// all drawn first, each asked 4 times. Nodes are malloc'd one by one.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 10000
#define QUERIES 1000
#define ROUNDS 4

typedef struct TreeNode {
    int32_t val;
    struct TreeNode *left, *right;
} TreeNode;

static TreeNode *common(TreeNode *node, int32_t p, int32_t q) {
    if (node == NULL) return NULL;
    if (node->val == p || node->val == q) return node;
    TreeNode *left = common(node->left, p, q);
    TreeNode *right = common(node->right, p, q);
    if (left != NULL && right != NULL) return node;
    return left != NULL ? left : right;
}

static int32_t depth(TreeNode *node, int32_t value) {
    if (node == NULL) return -1;
    if (node->val == value) return 0;
    int32_t l = depth(node->left, value), r = depth(node->right, value);
    int32_t below = l > r ? l : r;
    return below < 0 ? -1 : below + 1;
}

static int32_t find_distance(TreeNode *root, int32_t p, int32_t q) {
    TreeNode *ancestor = common(root, p, q);
    return depth(ancestor, p) + depth(ancestor, q);
}

// ---- the harness ----------------------------------------------------------

static int64_t seed = 1740;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    static int32_t values[N];
    static TreeNode *nodes[N];
    for (int64_t i = 0; i < N; i++) values[i] = (int32_t)i;
    for (int64_t i = N - 1; i >= 1; i--) {
        int64_t j = next_random() % (i + 1);
        int32_t t = values[i];
        values[i] = values[j];
        values[j] = t;
    }
    for (int64_t i = 0; i < N; i++) {
        TreeNode *node = malloc(sizeof *node);
        node->val = values[i];
        node->left = node->right = NULL;
        if (i > 0) {
            TreeNode *at = nodes[next_random() % i];
            for (;;) {
                if (next_random() % 2 == 0) {
                    if (at->left != NULL) at = at->left;
                    else { at->left = node; break; }
                } else {
                    if (at->right != NULL) at = at->right;
                    else { at->right = node; break; }
                }
            }
        }
        nodes[i] = node;
    }
    TreeNode *root = nodes[0];
    static int32_t ps[QUERIES], qs[QUERIES];
    for (int i = 0; i < QUERIES; i++) {
        ps[i] = (int32_t)(next_random() % N);
        qs[i] = (int32_t)(next_random() % N);
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int i = 0; i < QUERIES; i++) {
            int64_t found = find_distance(root, ps[i], qs[i]);
            total += found;
            check = (check * 31 + found + r) % 1000000007;
        }
    }
    printf("%d nodes, %d pairs, %d rounds: distances sum to %lld, checksum %lld\n", N, QUERIES, ROUNDS, (long long)total, (long long)check);
    for (int64_t i = 0; i < N; i++) free(nodes[i]);
    return 0;
}
