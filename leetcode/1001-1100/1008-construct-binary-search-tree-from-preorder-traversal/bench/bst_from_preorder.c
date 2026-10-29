// LeetCode #1008 bench: the ★ arm (recursion with an upper bound) over 50
// preorders of 100 values, drawn once; each of 4000 rounds builds every
// tree, starting from a different preorder, folds it into a checksum and
// frees it.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left, *right;
} TreeNode;

static TreeNode *build(const int64_t *pre, int64_t n, int64_t *next, int64_t bound) {
    if (*next == n || pre[*next] >= bound) return NULL;
    int64_t val = pre[*next];
    *next += 1;
    TreeNode *left = build(pre, n, next, val);
    TreeNode *right = build(pre, n, next, bound);
    TreeNode *node = malloc(sizeof(TreeNode));
    node->val = val;
    node->left = left;
    node->right = right;
    return node;
}

static TreeNode *bst_from_preorder(const int64_t *pre, int64_t n) {
    int64_t next = 0;
    return build(pre, n, &next, INT64_MAX);
}

static int64_t fold(const TreeNode *node, int64_t depth) {
    if (!node) return 0;
    return (node->val * depth + fold(node->left, depth + 1) * 3 + fold(node->right, depth + 1) * 7) % 1000000007;
}

static void release(TreeNode *node) {
    if (!node) return;
    release(node->left);
    release(node->right);
    free(node);
}

static int64_t seed = 1008;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static void random_preorder(int64_t n, int64_t most, int64_t *out) {
    char *seen = calloc(most + 1, 1);
    int64_t *vals = malloc(n * sizeof(int64_t));
    int64_t *left = malloc(n * sizeof(int64_t));
    int64_t *right = malloc(n * sizeof(int64_t));
    int64_t len = 0;
    while (len < n) {
        int64_t v = 1 + next_random() % most;
        if (seen[v]) continue;
        seen[v] = 1;
        vals[len] = v;
        left[len] = -1;
        right[len] = -1;
        int64_t me = len++;
        if (me > 0) {
            int64_t at = 0;
            for (;;) {
                if (v < vals[at]) {
                    if (left[at] == -1) { left[at] = me; break; }
                    at = left[at];
                } else {
                    if (right[at] == -1) { right[at] = me; break; }
                    at = right[at];
                }
            }
        }
    }
    int64_t *stack = malloc(n * sizeof(int64_t));
    int64_t top = 0, k = 0;
    stack[top++] = 0;
    while (top > 0) {
        int64_t at = stack[--top];
        out[k++] = vals[at];
        if (right[at] != -1) stack[top++] = right[at];
        if (left[at] != -1) stack[top++] = left[at];
    }
    free(seen); free(vals); free(left); free(right); free(stack);
}

int main(void) {
    enum { COUNT = 50, ROUNDS = 4000, N = 100 };
    static int64_t pre[COUNT][N];
    for (int k = 0; k < COUNT; k++) random_preorder(N, 1000, pre[k]);
    int64_t check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int64_t k = 0; k < COUNT; k++) {
            TreeNode *tree = bst_from_preorder(pre[(r + k) % COUNT], N);
            check = (check * 31 + fold(tree, 1)) % 1000000007;
            release(tree);
        }
    }
    printf("%d rounds over %d preorders of 100 values: checksum %lld\n", ROUNDS, COUNT, (long long)check);
    return 0;
}
