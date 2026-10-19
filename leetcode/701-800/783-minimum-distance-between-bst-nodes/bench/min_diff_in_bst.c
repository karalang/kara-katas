// LeetCode 783 — Minimum Distance Between BST Nodes: the bench, in C.
// Mirrors min_diff_in_bst.kara: ancestor bounds over the same 64 trees.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left, *right;
} TreeNode;

static int64_t min64(int64_t a, int64_t b) { return a < b ? a : b; }

static int64_t closest(const TreeNode *n, int64_t low, int64_t high) {
    if (!n) return INT64_MAX;
    int64_t best = INT64_MAX;
    if (low != -1) best = min64(best, n->val - low);
    if (high != -1) best = min64(best, high - n->val);
    best = min64(best, closest(n->left, low, n->val));
    return min64(best, closest(n->right, n->val, high));
}

static int64_t min_diff_in_bst(const TreeNode *root) { return closest(root, -1, -1); }

static int64_t seed = 783;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static TreeNode *node(int64_t v) {
    TreeNode *n = malloc(sizeof *n);
    n->val = v;
    n->left = n->right = NULL;
    return n;
}

static TreeNode *insert(TreeNode *root, int64_t v) {
    if (!root) return node(v);
    TreeNode *at = root;
    for (;;) {
        if (v < at->val) {
            if (at->left) at = at->left;
            else { at->left = node(v); break; }
        } else {
            if (at->right) at = at->right;
            else { at->right = node(v); break; }
        }
    }
    return root;
}

static void middle_first(const int64_t *ordered, int64_t lo, int64_t hi, int64_t *out, int *len) {
    if (lo > hi) return;
    int64_t mid = (lo + hi) / 2;
    out[(*len)++] = ordered[mid];
    middle_first(ordered, lo, mid - 1, out, len);
    middle_first(ordered, mid + 1, hi, out, len);
}

static int cmp(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

int main(void) {
    TreeNode *trees[64];
    static char taken[100001];
    for (int t = 0; t < 64; t++) {
        int64_t values[100];
        int count = 0;
        for (int i = 0; i <= 100000; i++) taken[i] = 0;
        while (count < 100) {
            int64_t hi = next_random();
            int64_t v = (hi * 32768 + next_random()) % 100001;
            if (!taken[v]) {
                taken[v] = 1;
                values[count++] = v;
            }
        }
        if (t % 4 >= 2) qsort(values, 100, sizeof values[0], cmp);
        if (t % 4 == 2) {
            int64_t order[100];
            int len = 0;
            middle_first(values, 0, 99, order, &len);
            for (int i = 0; i < 100; i++) values[i] = order[i];
        }
        TreeNode *root = NULL;
        for (int i = 0; i < 100; i++) root = insert(root, values[i]);
        trees[t] = root;
    }
    const int64_t rounds = 2000000;
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t answer = min_diff_in_bst(trees[r % 64]);
        total += answer;
        check = (check * 31 + answer) % 1000000007;
    }
    printf("%lld rounds of 100-value trees: gaps sum to %lld, checksum %lld\n",
           (long long)rounds, (long long)total, (long long)check);
    return 0;
}
