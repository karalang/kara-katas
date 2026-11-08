// LeetCode #1530: Number of Good Leaf Nodes Pairs -- bench: the ★ arm
// over 1000 random trees of 1 to 1024 nodes, built once and answered 10
// times, each with its own distance from 1 to 10. Each node's counts are
// a fresh `malloc`, as the other languages allocate a list per node.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left;
    struct TreeNode *right;
} TreeNode;

static int64_t *leaves_below(const TreeNode *node, int64_t distance, int64_t *pairs) {
    int64_t *counts = calloc((size_t)distance, sizeof(int64_t));
    if (node) {
        if (!node->left && !node->right) {
            counts[0] = 1;
        } else {
            int64_t *l = leaves_below(node->left, distance, pairs);
            int64_t *r = leaves_below(node->right, distance, pairs);
            for (int64_t i = 0; i < distance; i++) {
                for (int64_t j = 0; j < distance - i - 1; j++) {
                    *pairs += l[i] * r[j];
                }
            }
            for (int64_t i = 0; i < distance - 1; i++) {
                counts[i + 1] = l[i] + r[i];
            }
            free(l);
            free(r);
        }
    }
    return counts;
}

static int64_t count_pairs(const TreeNode *root, int64_t distance) {
    int64_t pairs = 0;
    free(leaves_below(root, distance, &pairs));
    return pairs;
}

static TreeNode *make(int64_t at, const int64_t *vals, const int64_t *left, const int64_t *right) {
    if (at < 0) {
        return NULL;
    }
    TreeNode *n = malloc(sizeof(TreeNode));
    n->val = vals[at];
    n->left = make(left[at], vals, left, right);
    n->right = make(right[at], vals, left, right);
    return n;
}

static void release(TreeNode *n) {
    if (n) {
        release(n->left);
        release(n->right);
        free(n);
    }
}

static int64_t seed = 1530;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) {
    return (check * 31 + x + 1) % 1000000007;
}

static TreeNode *random_tree(int64_t most) {
    int64_t n = next_random() % most + 1;
    int64_t *vals = malloc((size_t)n * sizeof(int64_t));
    int64_t *left = malloc((size_t)n * sizeof(int64_t));
    int64_t *right = malloc((size_t)n * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) {
        vals[i] = next_random() % 100 + 1;
        left[i] = -1;
        right[i] = -1;
        if (i > 0) {
            int64_t at = next_random() % i;
            for (;;) {
                if (next_random() % 2 == 0) {
                    if (left[at] < 0) {
                        left[at] = i;
                        break;
                    }
                    at = left[at];
                } else {
                    if (right[at] < 0) {
                        right[at] = i;
                        break;
                    }
                    at = right[at];
                }
            }
        }
    }
    TreeNode *root = make(0, vals, left, right);
    free(vals);
    free(left);
    free(right);
    return root;
}

int main(void) {
    enum { COUNT = 1000 };
    static TreeNode *roots[COUNT];
    static int64_t dist[COUNT];
    for (int c = 0; c < COUNT; c++) {
        roots[c] = random_tree(1024);
        dist[c] = next_random() % 10 + 1;
    }
    int64_t check = 0;
    for (int pass = 0; pass < 10; pass++) {
        for (int c = 0; c < COUNT; c++) {
            check = mix(check, count_pairs(roots[c], dist[c]));
        }
    }
    printf("10 passes over 1000 trees of up to 1024 nodes: checksum %lld\n", (long long)check);
    for (int c = 0; c < COUNT; c++) {
        release(roots[c]);
    }
    return 0;
}
