// Benchmark: LeetCode #965 Univalued Binary Tree -- the ★ arm, depth
// first, on trees of 100 nodes, LeetCode's largest. Mirrors
// is_unival_tree.kara, .rs, .py and go-seq/.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left, *right;
} TreeNode;

static bool holds(TreeNode *t, int64_t v) {
    if (t == NULL) return true;
    return t->val == v && holds(t->left, v) && holds(t->right, v);
}

static bool is_unival_tree(TreeNode *root) {
    if (root == NULL) return true;
    return holds(root->left, root->val) && holds(root->right, root->val);
}

static int64_t seed = 965;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static TreeNode *new_node(int64_t val) {
    TreeNode *t = malloc(sizeof(TreeNode));
    t->val = val;
    t->left = NULL;
    t->right = NULL;
    return t;
}

static void attach(TreeNode *root, TreeNode *node) {
    TreeNode *cur = root;
    for (;;) {
        if (next_random() % 2 == 0) {
            if (cur->left) cur = cur->left;
            else { cur->left = node; return; }
        } else {
            if (cur->right) cur = cur->right;
            else { cur->right = node; return; }
        }
    }
}

static TreeNode *make_tree(int kind, int n) {
    int64_t v = next_random() % 100;
    int64_t vals[128];
    for (int i = 0; i < n; i++) vals[i] = v;
    if (kind == 3) {
        for (int i = 0; i < n; i++) vals[i] = next_random() % 2;
    } else {
        for (int j = 0; j < kind; j++) {
            int k = next_random() % n;
            vals[k] = next_random() % 100;
        }
    }
    TreeNode *root = new_node(vals[0]);
    for (int i = 1; i < n; i++) attach(root, new_node(vals[i]));
    return root;
}

int main(void) {
    int rounds = 4000;
    TreeNode *trees[200];
    for (int i = 0; i < 200; i++) trees[i] = make_tree(i % 4, 100);
    int64_t total = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int i = 0; i < 200; i++) {
            int64_t bit = is_unival_tree(trees[(r + i) % 200]) ? 1 : 0;
            total += bit;
            check = (check * 31 + bit + 1 + i) % 1000000007;
        }
    }
    printf("%d rounds over 200 trees of 100 nodes: %lld univalued, checksum %lld\n", rounds,
           (long long)total, (long long)check);
    return 0;
}
