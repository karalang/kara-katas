/* Benchmark harness for LeetCode #129 — Sum Root to Leaf Numbers.
 * Mirrors sum_numbers.kara algorithm-for-algorithm.
 *
 * Uses plain malloc'd pointer-linked nodes — C's native model. Unlike kara
 * (`shared struct`, reference counted) and the Rust mirror (Rc), this lane pays
 * NO retain/release traffic during the traversal. That asymmetry is real and is
 * documented in ../README.md rather than papered over by hand-rolling a
 * refcount C would not normally use.
 */

#include <stdio.h>
#include <stdlib.h>

#define NP 4
#define N 2047
#define ITERS 40000

typedef struct TreeNode {
    long long val;
    struct TreeNode *left;
    struct TreeNode *right;
} TreeNode;

static long long sum_dfs(const TreeNode *node, long long acc) {
    if (node == NULL) {
        return 0;
    }
    long long cur = acc * 10 + node->val;
    if (node->left == NULL && node->right == NULL) {
        return cur;
    }
    return sum_dfs(node->left, cur) + sum_dfs(node->right, cur);
}

static long long digit(long long i, long long seed) { return ((i * 7 + seed * 3) % 9) + 1; }

static TreeNode *build_balanced(long long lo, long long hi, long long seed) {
    if (lo > hi) {
        return NULL;
    }
    long long mid = (lo + hi) / 2;
    TreeNode *node = malloc(sizeof(TreeNode));
    node->val = digit(mid, seed);
    node->left = build_balanced(lo, mid - 1, seed);
    node->right = build_balanced(mid + 1, hi, seed);
    return node;
}

int main(void) {
    TreeNode *trees[NP];
    for (long long j = 0; j < NP; j++) {
        trees[j] = build_balanced(0, N - 1, j + 1);
    }

    long long sink = 0;
    for (long long it = 0; it < ITERS; it++) {
        long long idx = (it * 3) % NP;
        sink = (sink + sum_dfs(trees[idx], 0)) % 1000000007LL;
    }
    printf("%lld\n", sink);
    return 0;
}
