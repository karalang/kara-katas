// Benchmark: LeetCode #998 Maximum Binary Tree II -- the ★ arm, down the
// right spine by recursion, on maximum trees of 99 values, LeetCode's
// largest. Mirrors insert_into_max_tree.kara, .rs, .py and go-seq/.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left, *right;
} TreeNode;

static TreeNode *new_node(int64_t val, TreeNode *left, TreeNode *right) {
    TreeNode *t = malloc(sizeof(TreeNode));
    t->val = val;
    t->left = left;
    t->right = right;
    return t;
}

static TreeNode *insert_into_max_tree(TreeNode *root, int64_t val) {
    if (root == NULL) return new_node(val, NULL, NULL);
    if (val > root->val) return new_node(val, root, NULL);
    root->right = insert_into_max_tree(root->right, val);
    return root;
}

static int64_t seed = 998;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static TreeNode *build(const int64_t *a, int64_t lo, int64_t hi) {
    if (lo >= hi) return NULL;
    int64_t m = lo;
    for (int64_t i = lo + 1; i < hi; i++)
        if (a[i] > a[m]) m = i;
    TreeNode *left = build(a, lo, m);
    TreeNode *right = build(a, m + 1, hi);
    return new_node(a[m], left, right);
}

// Take val out again, from where the insert put it on the right spine,
// and return the tree as it was with how deep val sat.
static TreeNode *take_out(TreeNode *root, int64_t val, int64_t *depth) {
    if (root->val == val) {
        TreeNode *left = root->left;
        free(root);
        *depth = 0;
        return left;
    }
    TreeNode *above = root;
    int64_t d = 1;
    for (;;) {
        TreeNode *next = above->right;
        if (next->val == val) {
            above->right = next->left;
            free(next);
            *depth = d;
            return root;
        }
        above = next;
        d++;
    }
}

int main(void) {
    const int64_t rounds = 100000;
    // 20 trees of the 99 values from 1 to 100 but one: the even ones in a
    // random order, the odd ones falling, which makes a chain of 99
    TreeNode *trees[20];
    int64_t vals[20];
    for (int t = 0; t < 20; t++) {
        int64_t val = 1 + next_random() % 100, a[99];
        int n = 0;
        for (int v = 0; v < 100; v++)
            if (100 - v != val) a[n++] = 100 - v;
        if (t % 2 == 0) {
            for (int64_t i = 98; i > 0; i--) {
                int64_t j = next_random() % (i + 1), x = a[i];
                a[i] = a[j];
                a[j] = x;
            }
        }
        trees[t] = build(a, 0, 99);
        vals[t] = val;
    }
    int64_t depths = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t i = 0; i < 20; i++) {
            int64_t k = (r + i) % 20, depth;
            TreeNode *got = insert_into_max_tree(trees[k], vals[k]);
            trees[k] = take_out(got, vals[k], &depth);
            depths += depth;
            check = (check * 31 + depth + 1) % 1000000007;
        }
    }
    printf("%lld rounds over 20 trees of 99 values: depth total %lld, checksum %lld\n",
           (long long)rounds, (long long)depths, (long long)check);
    return 0;
}
