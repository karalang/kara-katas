// LeetCode #2476: Closest Nodes Queries in a Binary Search Tree -- the
// bench, the ★ arm in C: an in-order walk reads the values ascending, and
// a bisection by hand finds the first value at least each query. The
// nodes are malloc'd one by one, the values seen in an array of flags
// over 1 to 10^6.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int32_t val;
    struct TreeNode *left, *right;
} TreeNode;

static void walk(const TreeNode *node, int64_t *values, int64_t *count) {
    if (!node) return;
    walk(node->left, values, count);
    values[(*count)++] = node->val;
    walk(node->right, values, count);
}

// answers[2i] the floor and answers[2i + 1] the ceiling of queries[i]
static void closest_nodes(const TreeNode *root, int64_t size, const int64_t *queries, int64_t q, int64_t *answers) {
    int64_t *values = malloc(sizeof(int64_t) * size);
    int64_t n = 0;
    walk(root, values, &n);
    for (int64_t k = 0; k < q; k++) {
        int64_t x = queries[k], lo = 0, hi = n;
        while (lo < hi) {
            int64_t mid = (lo + hi) / 2;
            if (values[mid] < x)
                lo = mid + 1;
            else
                hi = mid;
        }
        int64_t ceiling = lo < n ? values[lo] : -1;
        int64_t floor = (lo < n && values[lo] == x) ? x : (lo > 0 ? values[lo - 1] : -1);
        answers[2 * k] = floor;
        answers[2 * k + 1] = ceiling;
    }
    free(values);
}

// ---- bench harness ---------------------------------------------------------

static int64_t seed = 2476;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide_random(void) {
    int64_t high = next_random();
    return high * 32768 + next_random();
}

static TreeNode *leaf(int64_t v) {
    TreeNode *t = malloc(sizeof(TreeNode));
    t->val = (int32_t)v;
    t->left = t->right = NULL;
    return t;
}

static char used[1000001];

// the search tree of `n` distinct random values from 1 to 10^6, inserted
// in the order drawn
static TreeNode *random_search_tree(int64_t n) {
    for (int i = 0; i <= 1000000; i++) used[i] = 0;
    TreeNode *root = NULL;
    int64_t have = 0;
    while (have < n) {
        int64_t v = 1 + wide_random() % 1000000;
        if (used[v]) continue;
        used[v] = 1;
        have++;
        if (!root) {
            root = leaf(v);
            continue;
        }
        TreeNode *at = root;
        for (;;) {
            if (v < at->val) {
                if (at->left) {
                    at = at->left;
                } else {
                    at->left = leaf(v);
                    break;
                }
            } else {
                if (at->right) {
                    at = at->right;
                } else {
                    at->right = leaf(v);
                    break;
                }
            }
        }
    }
    return root;
}

int main(void) {
    // 10 random search trees of 10^4 nodes built once; then 220 passes,
    // each asking every tree 1000 values stepped from the checksum so far,
    // folding every answer and the pass into the checksum
    TreeNode *trees[10];
    for (int t = 0; t < 10; t++) trees[t] = random_search_tree(10000);
    int64_t queries[1000], answers[2000];
    int64_t check = 0;
    for (int64_t p = 0; p < 220; p++) {
        for (int t = 0; t < 10; t++) {
            for (int64_t i = 0; i < 1000; i++) queries[i] = 1 + (check + 997 * i) % 1000000;
            closest_nodes(trees[t], 10000, queries, 1000, answers);
            for (int64_t i = 0; i < 1000; i++)
                check = (check * 31 + answers[2 * i] + answers[2 * i + 1] + 2 + p) % 1000000007;
        }
    }
    printf("220 passes over 10 trees of 10^4: checksum %lld\n", (long long)check);
    return 0;
}
