// Benchmark for #663: the subtree sums, listed, as the Kara ★ arm.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left;
    struct TreeNode *right;
} TreeNode;

typedef struct {
    int64_t *data;
    size_t len, cap;
} Sums;

static void push(Sums *v, int64_t x) {
    if (v->len == v->cap) {
        v->cap = v->cap ? v->cap * 2 : 4;
        v->data = realloc(v->data, v->cap * sizeof(int64_t));
    }
    v->data[v->len++] = x;
}

static int64_t subtree_sum(TreeNode *node, Sums *sums) {
    if (!node) {
        return 0;
    }
    int64_t s = node->val + subtree_sum(node->left, sums) + subtree_sum(node->right, sums);
    push(sums, s);
    return s;
}

static bool check_equal_tree(TreeNode *root) {
    Sums sums = {NULL, 0, 0};
    int64_t total = subtree_sum(root, &sums);
    bool found = false;
    if (total % 2 == 0) {
        sums.len--;
        for (size_t i = 0; i < sums.len; i++) {
            if (sums.data[i] == total / 2) {
                found = true;
                break;
            }
        }
    }
    free(sums.data);
    return found;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static TreeNode *leaf(int64_t v) {
    TreeNode *n = malloc(sizeof(TreeNode));
    n->val = v;
    n->left = NULL;
    n->right = NULL;
    return n;
}

static TreeNode *grown_tree(int64_t count, int64_t *seed) {
    TreeNode *root = leaf(next_random(seed) % 200001 - 100000);
    for (int64_t i = 1; i < count; i++) {
        TreeNode *at = root;
        bool placed = false;
        while (!placed) {
            if (next_random(seed) % 2 == 0) {
                if (at->left) {
                    at = at->left;
                } else {
                    at->left = leaf(next_random(seed) % 200001 - 100000);
                    placed = true;
                }
            } else {
                if (at->right) {
                    at = at->right;
                } else {
                    at->right = leaf(next_random(seed) % 200001 - 100000);
                    placed = true;
                }
            }
        }
    }
    return root;
}

static TreeNode *copy(TreeNode *node) {
    if (!node) {
        return NULL;
    }
    TreeNode *n = leaf(node->val);
    n->left = copy(node->left);
    n->right = copy(node->right);
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
    int64_t seed = 663;
    TreeNode *trees[8];
    for (int i = 0; i < 4; i++) {
        trees[2 * i] = grown_tree(10000, &seed);
        TreeNode *root = leaf(0);
        root->left = grown_tree(4999, &seed);
        root->right = copy(root->left);
        trees[2 * i + 1] = root;
    }
    int64_t rounds = 4000;
    int64_t split = 0;
    int64_t sum = 0;
    for (int64_t r = 0; r < rounds; r++) {
        bool ok = check_equal_tree(trees[r % 8]);
        if (ok) {
            split++;
        }
        sum = (sum * 31 + r * 2 + (ok ? 1 : 0)) % 1000000007;
    }
    printf("8 trees of 10000 nodes, %lld rounds: %lld split, checksum %lld\n", (long long)rounds,
           (long long)split, (long long)sum);
    for (int i = 0; i < 8; i++) {
        free_tree(trees[i]);
    }
    return 0;
}
