// Benchmark for #450: mirror of delete_node.kara (recursive, successor's
// value copied in) on one random search tree of 1,000,000 values, built
// once, then 1,000,000 deletes of random keys.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left;
    struct TreeNode *right;
} TreeNode;

static TreeNode *delete_node(TreeNode *root, int64_t key) {
    TreeNode *node = root;
    if (!node) {
        return NULL;
    }
    if (key < node->val) {
        node->left = delete_node(node->left, key);
        return node;
    }
    if (key > node->val) {
        node->right = delete_node(node->right, key);
        return node;
    }
    if (!node->left) {
        TreeNode *right = node->right;
        free(node);
        return right;
    }
    if (!node->right) {
        TreeNode *left = node->left;
        free(node);
        return left;
    }
    TreeNode *successor = node->right;
    while (successor->left) {
        successor = successor->left;
    }
    node->val = successor->val;
    node->right = delete_node(node->right, successor->val);
    return node;
}

static TreeNode *insert(TreeNode *root, int64_t v) {
    TreeNode *fresh = malloc(sizeof(TreeNode));
    fresh->val = v;
    fresh->left = NULL;
    fresh->right = NULL;
    if (!root) {
        return fresh;
    }
    TreeNode *node = root;
    for (;;) {
        if (v < node->val) {
            if (!node->left) {
                node->left = fresh;
                break;
            }
            node = node->left;
        } else {
            if (!node->right) {
                node->right = fresh;
                break;
            }
            node = node->right;
        }
    }
    return root;
}

static void walk(const TreeNode *node, int64_t *out, int64_t *count) {
    if (node) {
        walk(node->left, out, count);
        out[(*count)++] = node->val;
        walk(node->right, out, count);
    }
}

static void free_tree(TreeNode *node) {
    if (node) {
        free_tree(node->left);
        free_tree(node->right);
        free(node);
    }
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    const int64_t n = 1000000, deletes = 1000000;
    int64_t seed = 450;
    // A shuffle of the even numbers below 2n.
    int64_t *values = malloc(n * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) {
        values[i] = i * 2;
    }
    for (int64_t i = 0; i < n; i++) {
        int64_t r = next_random(&seed) * 32768;
        r += next_random(&seed);
        int64_t j = i + r % (n - i);
        int64_t tmp = values[i];
        values[i] = values[j];
        values[j] = tmp;
    }
    TreeNode *root = NULL;
    for (int64_t i = 0; i < n; i++) {
        root = insert(root, values[i]);
    }
    for (int64_t d = 0; d < deletes; d++) {
        int64_t key = next_random(&seed) * 32768;
        key = (key + next_random(&seed)) % (2 * n);
        root = delete_node(root, key);
    }
    int64_t count = 0;
    walk(root, values, &count);
    int64_t checksum = 0;
    for (int64_t i = 0; i < count; i++) {
        checksum = (checksum * 31 + values[i]) % 1000000007;
    }
    free_tree(root);
    free(values);
    printf("%lld deletes from %lld values: %lld nodes left, checksum %lld\n", (long long)deletes,
           (long long)n, (long long)count, (long long)checksum);
    return 0;
}
