// LeetCode #1379 bench -- C: the ★ arm: the two trees walked together,
// depth first; the clone's node where the original's is the target itself
// (the same pointer) is the answer.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int val;
    struct TreeNode *left;
    struct TreeNode *right;
} TreeNode;

static TreeNode *new_node(int val) {
    TreeNode *t = malloc(sizeof(TreeNode));
    t->val = val;
    t->left = NULL;
    t->right = NULL;
    return t;
}

static TreeNode *find(TreeNode *o, TreeNode *c, TreeNode *target) {
    if (o == target) {
        return c;
    }
    if (o->left && c->left) {
        TreeNode *found = find(o->left, c->left, target);
        if (found) {
            return found;
        }
    }
    if (o->right && c->right) {
        return find(o->right, c->right, target);
    }
    return NULL;
}

static TreeNode *get_target_copy(TreeNode *original, TreeNode *cloned, TreeNode *target) {
    return find(original, cloned, target);
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static TreeNode *clone_tree(TreeNode *node) {
    TreeNode *copy = new_node(node->val);
    if (node->left) {
        copy->left = clone_tree(node->left);
    }
    if (node->right) {
        copy->right = clone_tree(node->right);
    }
    return copy;
}

typedef struct {
    TreeNode *node;
    int left;
} Place;

int main(void) {
    // 10 trees of 10^4 nodes built once, with their clones; then 3000
    // rounds, each asking one tree's clone for the copy of one node (see
    // the Kāra bench)
    const int64_t n = 10000;
    int64_t seed = 1379;
    TreeNode *originals[10], *clones[10];
    TreeNode **nodes[10];
    Place *open = malloc(sizeof(Place) * (size_t)(2 * n + 2));
    for (int t = 0; t < 10; t++) {
        TreeNode *root = new_node(1);
        nodes[t] = malloc(sizeof(TreeNode *) * (size_t)n);
        nodes[t][0] = root;
        int64_t len = 0;
        open[len++] = (Place){root, 1};
        open[len++] = (Place){root, 0};
        for (int64_t k = 1; k < n; k++) {
            int64_t at = next_random(&seed) % len;
            Place p = open[at];
            open[at] = open[--len];
            TreeNode *node = new_node((int)(k + 1));
            if (p.left) {
                p.node->left = node;
            } else {
                p.node->right = node;
            }
            open[len++] = (Place){node, 1};
            open[len++] = (Place){node, 0};
            nodes[t][k] = node;
        }
        originals[t] = root;
        clones[t] = clone_tree(root);
    }
    int64_t check = 0;
    for (int64_t r = 0; r < 3000; r++) {
        int64_t t = check % 10;
        TreeNode *target = nodes[t][(check / 10 + r) % n];
        TreeNode *found = get_target_copy(originals[t], clones[t], target);
        int64_t own = found == target ? 0 : 1;
        check = (check * 31 + (int64_t)found->val * 2 + own + r) % 1000000007;
    }
    printf("3000 rounds over 10 trees of 10000 nodes: checksum %lld\n", (long long)check);
    return 0;
}
