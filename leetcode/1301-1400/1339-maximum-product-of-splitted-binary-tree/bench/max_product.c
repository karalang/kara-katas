// LeetCode #1339 bench in C: the ★ arm (one recursive walk for the total,
// a second for every subtree's sum, keeping the best product, taken modulo
// 10^9 + 7 at the end) on the same 10 trees of 5 * 10^4 nodes and 20
// passes.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int val;
    struct TreeNode *left;
    struct TreeNode *right;
} TreeNode;

static int64_t total(TreeNode *node) {
    if (!node) return 0;
    return node->val + total(node->left) + total(node->right);
}

static int64_t best_cut(TreeNode *node, int64_t all, int64_t *best) {
    if (!node) return 0;
    int64_t s = node->val + best_cut(node->left, all, best) + best_cut(node->right, all, best);
    int64_t p = s * (all - s);
    if (p > *best) *best = p;
    return s;
}

static int max_product(TreeNode *root) {
    int64_t all = total(root);
    int64_t best = 0;
    best_cut(root, all, &best);
    return (int)(best % 1000000007);
}

static int64_t seed = 1339;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static TreeNode *new_node(void) {
    TreeNode *t = malloc(sizeof(TreeNode));
    t->val = (int)(1 + next_random() % 10000);
    t->left = NULL;
    t->right = NULL;
    return t;
}

typedef struct {
    TreeNode *node;
    int left;
} Place;

static void build(int n, TreeNode **nodes) {
    TreeNode *root = new_node();
    int count = 0;
    nodes[count++] = root;
    Place *places = malloc(sizeof(Place) * (size_t)(n + 2));
    size_t len = 0;
    places[len++] = (Place){root, 1};
    places[len++] = (Place){root, 0};
    while (count < n) {
        size_t k = (size_t)(next_random() % (int64_t)len);
        Place p = places[k];
        places[k] = places[--len];
        TreeNode *node = new_node();
        if (p.left) p.node->left = node; else p.node->right = node;
        places[len++] = (Place){node, 1};
        places[len++] = (Place){node, 0};
        nodes[count++] = node;
    }
    free(places);
}

int main(void) {
    int n = 50000;
    TreeNode **trees[10];
    for (int t = 0; t < 10; t++) {
        trees[t] = malloc(sizeof(TreeNode *) * (size_t)n);
        build(n, trees[t]);
    }
    int64_t check = 0;
    for (int64_t pass = 0; pass < 20; pass++) {
        for (int t = 0; t < 10; t++) {
            TreeNode **nodes = trees[t];
            nodes[check % n]->val = (int)(1 + (check / 7) % 10000);
            int answer = max_product(nodes[0]);
            check = (check * 31 + answer + pass) % 1000000007;
        }
    }
    printf("20 passes over 10 trees of 5 * 10^4: checksum %lld\n", (long long)check);
    return 0;
}
