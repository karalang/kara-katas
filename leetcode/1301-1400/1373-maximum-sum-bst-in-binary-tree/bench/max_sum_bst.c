// LeetCode #1373 bench -- C: the ★ arm over plain pointers: one walk up
// from the leaves; each subtree reports whether it is a search tree, its
// smallest and largest key, and its sum.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int val;
    struct TreeNode *left;
    struct TreeNode *right;
} TreeNode;

typedef struct {
    bool search;
    int64_t low;
    int64_t high;
    int64_t sum;
} Summary;

static Summary summarize(const TreeNode *node, int64_t *best) {
    if (node == NULL) {
        // an empty tree is a search tree with no keys
        return (Summary){true, INT64_MAX, INT64_MIN, 0};
    }
    Summary l = summarize(node->left, best);
    Summary r = summarize(node->right, best);
    int64_t key = node->val;
    if (l.search && r.search && l.high < key && key < r.low) {
        int64_t sum = l.sum + key + r.sum;
        if (sum > *best) *best = sum;
        return (Summary){true, l.low < key ? l.low : key, r.high > key ? r.high : key, sum};
    }
    return (Summary){false, 0, 0, 0};
}

static int max_sum_bst(const TreeNode *root) {
    int64_t best = 0;
    summarize(root, &best);
    return (int)best;
}

static int64_t seed = 1373;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static TreeNode *new_node(int val) {
    TreeNode *n = malloc(sizeof(TreeNode));
    n->val = val;
    n->left = NULL;
    n->right = NULL;
    return n;
}

int main(void) {
    // 4 search trees of 4 * 10^4 nodes, keys from -4 * 10^4 to 4 * 10^4
    // put in one by one, a key already there skipped, built once; then 300
    // rounds, each giving one node of one tree a new key, both drawn from
    // the checksum so far, and finding that tree's largest search tree
    enum { TREES = 4, NODES = 40000 };
    TreeNode *roots[TREES];
    TreeNode **nodes[TREES];
    for (int t = 0; t < TREES; t++) {
        TreeNode *root = new_node(0);
        TreeNode **all = malloc(sizeof(TreeNode *) * NODES);
        int count = 0;
        all[count++] = root;
        while (count < NODES) {
            int64_t a = next_random();
            int key = (int)((a * 32768 + next_random()) % 80001 - 40000);
            TreeNode *at = root;
            while (key != at->val) {
                TreeNode *child = key < at->val ? at->left : at->right;
                if (child == NULL) {
                    TreeNode *node = new_node(key);
                    if (key < at->val) {
                        at->left = node;
                    } else {
                        at->right = node;
                    }
                    all[count++] = node;
                    break;
                }
                at = child;
            }
        }
        roots[t] = root;
        nodes[t] = all;
    }
    int64_t check = 0;
    for (int64_t r = 0; r < 300; r++) {
        int64_t t = check % TREES;
        nodes[t][(check / TREES) % NODES]->val = (int)((check / 160000) % 80001 - 40000);
        int64_t got = max_sum_bst(roots[t]);
        check = (check * 31 + got + r) % 1000000007;
    }
    printf("300 rounds over 4 trees of 40000 nodes: checksum %lld\n", (long long)check);
    return 0;
}
