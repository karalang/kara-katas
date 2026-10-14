// LeetCode #623: Add One Row to Tree -- C mirror of the Kāra bench.
//
// The ★ arm's recursion with the level, on the same trees and rounds,
// each row taken out again by the same `undo`, which frees the row's
// nodes it takes out.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left, *right;
} TreeNode;

static TreeNode *node(int64_t val, TreeNode *left, TreeNode *right) {
    TreeNode *n = malloc(sizeof(TreeNode));
    n->val = val;
    n->left = left;
    n->right = right;
    return n;
}

static void insert(TreeNode *n, int64_t val, int64_t depth, int64_t level) {
    if (n == NULL) {
        return;
    }
    if (level == depth - 1) {
        n->left = node(val, n->left, NULL);
        n->right = node(val, NULL, n->right);
    } else {
        insert(n->left, val, depth, level + 1);
        insert(n->right, val, depth, level + 1);
    }
}

static TreeNode *add_one_row(TreeNode *root, int64_t val, int64_t depth) {
    if (depth == 1) {
        return node(val, root, NULL);
    }
    insert(root, val, depth, 1);
    return root;
}

static int64_t seed = 623;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static TreeNode *random_tree(int64_t size, int64_t lean) {
    TreeNode *root = node(next_random() % 201 - 100, NULL, NULL);
    for (int64_t i = 1; i < size; i++) {
        TreeNode *c = node(next_random() % 201 - 100, NULL, NULL);
        TreeNode *n = root;
        for (;;) {
            if (next_random() % 100 < lean) {
                if (n->left == NULL) {
                    n->left = c;
                    break;
                }
                n = n->left;
            } else {
                if (n->right == NULL) {
                    n->right = c;
                    break;
                }
                n = n->right;
            }
        }
    }
    return root;
}

static int64_t count = 0, checksum = 0;

static void undo(TreeNode *n, int64_t depth, int64_t level) {
    if (n == NULL) {
        return;
    }
    if (level == depth - 1) {
        TreeNode *l = n->left, *r = n->right;
        count += 2;
        checksum = (checksum * 31 + l->val + r->val + 400000) % 1000000007;
        n->left = l->left;
        n->right = r->right;
        free(l);
        free(r);
    } else {
        undo(n->left, depth, level + 1);
        undo(n->right, depth, level + 1);
    }
}

static void free_tree(TreeNode *n) {
    if (n != NULL) {
        free_tree(n->left);
        free_tree(n->right);
        free(n);
    }
}

int main(void) {
    enum { TREES = 20, ROUNDS = 4000 };
    TreeNode *all[TREES];
    for (int i = 0; i < TREES; i++) {
        int64_t lean = 30 + next_random() % 41;
        all[i] = random_tree(10000, lean);
    }
    for (int64_t r = 0; r < ROUNDS; r++) {
        int64_t depth = 2 + (r / TREES) % 20;
        TreeNode *root = add_one_row(all[r % TREES], r % 201 - 100, depth);
        undo(root, depth, 1);
    }
    printf("%d trees, %d rounds: %lld row nodes, checksum %lld\n", TREES, ROUNDS, (long long)count, (long long)checksum);
    for (int i = 0; i < TREES; i++) {
        free_tree(all[i]);
    }
    return 0;
}
