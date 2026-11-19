// LeetCode #1644: Lowest Common Ancestor of a Binary Tree II -- the bench's
// C mirror: the ★ arm on 60 random trees of 10000 nodes, each asked about
// 50 pairs of values, one in five of them not in the tree, all drawn
// first. Every node is malloc'd on its own, as LeetCode's C tree is.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define TREES 60
#define NODES 10000
#define PAIRS 50

struct TreeNode {
    int32_t val;
    struct TreeNode *left;
    struct TreeNode *right;
};

static struct TreeNode *leaf(int32_t val) {
    struct TreeNode *n = malloc(sizeof *n);
    n->val = val;
    n->left = NULL;
    n->right = NULL;
    return n;
}

static int64_t count_below(struct TreeNode *node, int32_t p, int32_t q, struct TreeNode **found) {
    if (node == NULL) return 0;
    int64_t here = (node->val == p || node->val == q) ? 1 : 0;
    int64_t count = count_below(node->left, p, q, found) + count_below(node->right, p, q, found) + here;
    if (count == 2 && *found == NULL) *found = node;
    return count;
}

static struct TreeNode *lowest_common_ancestor(struct TreeNode *root, struct TreeNode *p, struct TreeNode *q) {
    struct TreeNode *found = NULL;
    count_below(root, p->val, q->val, &found);
    return found;
}

static int64_t seed = 1644;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static struct TreeNode *random_tree(int64_t n, struct TreeNode **nodes) {
    int32_t *values = malloc((size_t)n * sizeof *values);
    for (int64_t i = 0; i < n; i++) values[i] = (int32_t)i;
    for (int64_t i = n - 1; i >= 1; i--) {
        int64_t j = next_random() % (i + 1);
        int32_t t = values[i];
        values[i] = values[j];
        values[j] = t;
    }
    for (int64_t i = 0; i < n; i++) {
        struct TreeNode *node = leaf(values[i]);
        if (i > 0) {
            struct TreeNode *at = nodes[next_random() % i];
            for (;;) {
                if (next_random() % 2 == 0) {
                    if (at->left) at = at->left;
                    else { at->left = node; break; }
                } else {
                    if (at->right) at = at->right;
                    else { at->right = node; break; }
                }
            }
        }
        nodes[i] = node;
    }
    free(values);
    return nodes[0];
}

int main(void) {
    static struct TreeNode *nodes[TREES][NODES];
    static int32_t pairs[TREES][PAIRS][2];
    for (int t = 0; t < TREES; t++) {
        random_tree(NODES, nodes[t]);
        for (int k = 0; k < PAIRS; k++) {
            int64_t p = next_random() % 12500;
            int64_t q = next_random() % 12500;
            if (q == p) q = (q + 1) % 12500;
            pairs[t][k][0] = (int32_t)p;
            pairs[t][k][1] = (int32_t)q;
        }
    }
    int64_t check = 0, total = 0;
    for (int t = 0; t < TREES; t++) {
        for (int k = 0; k < PAIRS; k++) {
            struct TreeNode *p = leaf(pairs[t][k][0]);
            struct TreeNode *q = leaf(pairs[t][k][1]);
            struct TreeNode *node = lowest_common_ancestor(nodes[t][0], p, q);
            int64_t found = node ? node->val : -1;
            free(p);
            free(q);
            total += found + 1;
            check = (check * 31 + found + 2) % 1000000007;
        }
    }
    for (int t = 0; t < TREES; t++)
        for (int i = 0; i < NODES; i++) free(nodes[t][i]);
    printf("60 trees of 10000 nodes, 50 pairs each: answers sum to %lld, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
