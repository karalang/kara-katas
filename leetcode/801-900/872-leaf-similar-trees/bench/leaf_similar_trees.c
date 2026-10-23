// LeetCode #872: Leaf-Similar Trees -- C mirror of the bench program (the
// ★ arm, the leaves of each collected by recursion), with malloc'd nodes
// and growable arrays for the leaf sequences.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left, *right;
} TreeNode;

typedef struct {
    int64_t *data;
    int64_t len, cap;
} Vec;

static void push(Vec *v, int64_t x) {
    if (v->len == v->cap) {
        v->cap = v->cap ? 2 * v->cap : 4;
        v->data = realloc(v->data, v->cap * sizeof(int64_t));
    }
    v->data[v->len++] = x;
}

static void leaves(const TreeNode *node, Vec *out) {
    if (node) {
        if (!node->left && !node->right) {
            push(out, node->val);
        } else {
            leaves(node->left, out);
            leaves(node->right, out);
        }
    }
}

static int leaf_similar(const TreeNode *root1, const TreeNode *root2) {
    Vec first = {0}, second = {0};
    leaves(root1, &first);
    leaves(root2, &second);
    int same = first.len == second.len && (first.len == 0 || memcmp(first.data, second.data, first.len * sizeof(int64_t)) == 0);
    free(first.data);
    free(second.data);
    return same;
}

static int64_t seed = 872;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static TreeNode *new_node(int64_t val, TreeNode *left, TreeNode *right) {
    TreeNode *n = malloc(sizeof(TreeNode));
    n->val = val;
    n->left = left;
    n->right = right;
    return n;
}

static TreeNode *random_tree(int64_t n, int64_t limit) {
    TreeNode **nodes = malloc(n * sizeof(TreeNode *));
    for (int64_t k = 0; k < n; k++) {
        TreeNode *node = new_node(next_random() % limit, NULL, NULL);
        if (k > 0) {
            for (;;) {
                TreeNode *parent = nodes[next_random() % k];
                if (next_random() % 2 == 0) {
                    if (!parent->left) {
                        parent->left = node;
                        break;
                    }
                } else if (!parent->right) {
                    parent->right = node;
                    break;
                }
            }
        }
        nodes[k] = node;
    }
    TreeNode *root = n ? nodes[0] : NULL;
    free(nodes);
    return root;
}

static TreeNode *tree_with_leaves(const int64_t *vals, int64_t lo, int64_t hi, int64_t limit) {
    if (hi - lo == 1) return new_node(vals[lo], NULL, NULL);
    int64_t mid = lo + 1 + next_random() % (hi - lo - 1);
    TreeNode *left = tree_with_leaves(vals, lo, mid, limit);
    TreeNode *right = tree_with_leaves(vals, mid, hi, limit);
    return new_node(next_random() % limit, left, right);
}

int main(void) {
    static TreeNode *a[2000], *b[2000];
    for (int k = 0; k < 2000; k++) {
        a[k] = random_tree(200, 201);
        if (k % 2 == 0) {
            Vec vals = {0};
            leaves(a[k], &vals);
            b[k] = tree_with_leaves(vals.data, 0, vals.len, 201);
            free(vals.data);
        } else {
            b[k] = random_tree(200, 201);
        }
    }
    int64_t check = 0;
    for (int k = 0; k < 2000; k++) {
        Vec vals = {0};
        leaves(b[k], &vals);
        for (int64_t i = 0; i < vals.len; i++) check = (check * 31 + vals.data[i] + 1) % 1000000007;
        free(vals.data);
    }
    int64_t similar = 0;
    for (int r = 0; r < 50; r++)
        for (int k = 0; k < 2000; k++)
            if (leaf_similar(a[k], b[k])) similar++;
    printf("100000 comparisons of 2000 pairs: %lld leaf-similar, leaf checksum %lld\n", (long long)similar, (long long)check);
    return 0;
}
