// Benchmark for #545: C mirror of the ★ arm (three walks); see
// boundary_of_binary_tree.kara. The nodes are malloc'd one at a time and
// never freed, as the trees live to the end; the answer is a growable
// array, freed after use.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left, *right;
} TreeNode;

typedef struct {
    int64_t *data, len, cap;
} Vec;

static void push(Vec *v, int64_t x) {
    if (v->len == v->cap) {
        v->cap = v->cap ? v->cap * 2 : 4;
        v->data = realloc(v->data, v->cap * sizeof(int64_t));
    }
    v->data[v->len++] = x;
}

static int is_leaf(const TreeNode *n) { return !n->left && !n->right; }

static void leaves(const TreeNode *node, Vec *out) {
    if (!node) return;
    if (is_leaf(node)) {
        push(out, node->val);
    } else {
        leaves(node->left, out);
        leaves(node->right, out);
    }
}

static Vec boundary_of_binary_tree(const TreeNode *r) {
    Vec out = {0};
    if (!r) return out;
    push(&out, r->val);
    if (is_leaf(r)) return out;
    for (const TreeNode *n = r->left; n && !is_leaf(n); n = n->left ? n->left : n->right)
        push(&out, n->val);
    leaves(r->left, &out);
    leaves(r->right, &out);
    Vec right = {0};
    for (const TreeNode *n = r->right; n && !is_leaf(n); n = n->right ? n->right : n->left)
        push(&right, n->val);
    for (int64_t i = right.len - 1; i >= 0; i--) push(&out, right.data[i]);
    free(right.data);
    return out;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static TreeNode *new_node(int64_t v) {
    TreeNode *n = malloc(sizeof(TreeNode));
    n->val = v;
    n->left = n->right = NULL;
    return n;
}

int main(void) {
    // 20 random trees of 10,000 nodes (the problem's most) with values
    // from -1,000 to 1,000, each new node walking down from the root and
    // going left with chance 50 to 88 in 100, built once, the nodes kept
    // in the order they were added. Then 200 times over every tree the
    // subtree at one of its first 16 nodes, picked by the round and the
    // tree, is answered; every value on the boundary goes into the
    // checksum.
    int64_t trees = 20, seed = 545;
    TreeNode ***all = malloc(trees * sizeof(TreeNode **));
    for (int64_t g = 0; g < trees; g++) {
        int64_t lean = 50 + 2 * g;
        all[g] = malloc(10000 * sizeof(TreeNode *));
        TreeNode *root = new_node(next_random(&seed) % 2001 - 1000);
        all[g][0] = root;
        for (int i = 1; i < 10000; i++) {
            TreeNode *c = new_node(next_random(&seed) % 2001 - 1000);
            TreeNode *node = root;
            for (;;) {
                if (next_random(&seed) % 100 < lean) {
                    if (node->left) node = node->left;
                    else { node->left = c; break; }
                } else {
                    if (node->right) node = node->right;
                    else { node->right = c; break; }
                }
            }
            all[g][i] = c;
        }
    }
    int64_t total = 0, checksum = 0;
    for (int64_t r = 0; r < 200; r++) {
        for (int64_t t = 0; t < trees; t++) {
            Vec b = boundary_of_binary_tree(all[t][(r * 37 + t * 11) % 16]);
            total += b.len;
            for (int64_t i = 0; i < b.len; i++) checksum = (checksum * 31 + b.data[i] + 1001) % 1000000007;
            free(b.data);
        }
    }
    printf("%lld trees, 200 times each: %lld on the boundary, checksum %lld\n", (long long)trees,
           (long long)total, (long long)checksum);
    return 0;
}
