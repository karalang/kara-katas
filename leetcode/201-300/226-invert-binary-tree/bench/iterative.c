/*
 * LeetCode 226 — iterative BFS invert, bench mirror in C.
 *
 * Algorithmic mirror of bench/iterative.{kara,rs,py}. N=2000 nodes, LCG
 * seed 12345, K=10 invert cycles, BFS-position-weighted sink.
 * Stdout sink: 2666665501.
 *
 * See ../README.md § Benchmarks for what the numbers mean.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left;
    struct TreeNode *right;
} TreeNode;

static TreeNode *invert(TreeNode *root) {
    if (root == NULL) {
        return root;
    }
    TreeNode **queue = (TreeNode **)malloc(2000 * sizeof(TreeNode *));
    if (!queue) {
        return root;
    }
    size_t head = 0, tail = 0;
    queue[tail++] = root;
    while (head < tail) {
        TreeNode *current = queue[head++];
        TreeNode *new_right = current->left;
        TreeNode *new_left = current->right;
        current->left = new_left;
        current->right = new_right;
        if (current->left != NULL) {
            queue[tail++] = current->left;
        }
        if (current->right != NULL) {
            queue[tail++] = current->right;
        }
    }
    free(queue);
    return root;
}

static TreeNode *build_tree(int64_t n) {
    if (n <= 0) {
        return NULL;
    }
    TreeNode **nodes = (TreeNode **)malloc((size_t)n * sizeof(TreeNode *));
    if (!nodes) {
        return NULL;
    }
    for (int64_t i = 0; i < n; i++) {
        nodes[i] = (TreeNode *)malloc(sizeof(TreeNode));
        if (!nodes[i]) {
            return NULL;
        }
        nodes[i]->val = i;
        nodes[i]->left = NULL;
        nodes[i]->right = NULL;
    }
    int64_t state = 12345;
    for (int64_t i = 1; i < n; i++) {
        TreeNode *cur = nodes[0];
        for (;;) {
            state = (state * 1103515245 + 12345) & 2147483647;
            int64_t bit = state & 1;
            if (bit == 0) {
                if (cur->left == NULL) {
                    cur->left = nodes[i];
                    break;
                }
                cur = cur->left;
            } else {
                if (cur->right == NULL) {
                    cur->right = nodes[i];
                    break;
                }
                cur = cur->right;
            }
        }
    }
    TreeNode *root = nodes[0];
    free(nodes);
    return root;
}

static int64_t bfs_sink(TreeNode *root) {
    if (root == NULL) {
        return 0;
    }
    TreeNode **queue = (TreeNode **)malloc(2000 * sizeof(TreeNode *));
    if (!queue) {
        return 0;
    }
    size_t head = 0, tail = 0;
    queue[tail++] = root;
    int64_t sum = 0;
    int64_t pos = 0;
    while (head < tail) {
        TreeNode *cur = queue[head++];
        pos++;
        sum += cur->val * pos;
        if (cur->left != NULL) {
            queue[tail++] = cur->left;
        }
        if (cur->right != NULL) {
            queue[tail++] = cur->right;
        }
    }
    free(queue);
    return sum;
}

int main(void) {
    TreeNode *root = build_tree(2000);
    for (int k = 0; k < 10; k++) {
        root = invert(root);
    }
    printf("%lld\n", (long long)bfs_sink(root));
    return 0;
}
