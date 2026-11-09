// Benchmark: LeetCode #1080 Insufficient Nodes in Root to Leaf Paths --
// the ★ arm. Mirrors sufficient_subset.kara, .rs, .py and go-seq/. Each
// node is malloc'd as it is built and freed when it is cut or, for what
// is left, after the count, as the reference-counted arms drop them.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int val;
    struct TreeNode *left, *right;
} TreeNode;

static void release(TreeNode *t) {
    if (!t) return;
    release(t->left);
    release(t->right);
    free(t);
}

static TreeNode *prune(TreeNode *n, int64_t need) {
    if (!n) return NULL;
    if (!n->left && !n->right) {
        if (n->val >= need) return n;
        free(n);
        return NULL;
    }
    n->left = prune(n->left, need - n->val);
    n->right = prune(n->right, need - n->val);
    if (!n->left && !n->right) {
        free(n);
        return NULL;
    }
    return n;
}

static TreeNode *sufficient_subset(TreeNode *root, int64_t limit) { return prune(root, limit); }

static int64_t seed = 1080;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

#define SHAPES 200
#define N 1000
static int val[SHAPES][N];
static int64_t lft[SHAPES][N], rgt[SHAPES][N];

static void random_shape(int s) {
    for (int64_t k = 0; k < N; k++) {
        val[s][k] = (int)(next_random() % 201 - 100);
        lft[s][k] = -1;
        rgt[s][k] = -1;
        if (k > 0) {
            int64_t at = 0;
            for (;;) {
                if (next_random() % 2 == 0) {
                    if (lft[s][at] < 0) { lft[s][at] = k; break; }
                    at = lft[s][at];
                } else {
                    if (rgt[s][at] < 0) { rgt[s][at] = k; break; }
                    at = rgt[s][at];
                }
            }
        }
    }
}

static TreeNode *build(int s, int64_t k) {
    if (k < 0) return NULL;
    TreeNode *n = malloc(sizeof *n);
    n->val = val[s][k];
    n->left = build(s, lft[s][k]);
    n->right = build(s, rgt[s][k]);
    return n;
}

static int64_t count(TreeNode *t) { return t ? 1 + count(t->left) + count(t->right) : 0; }

int main(void) {
    int64_t rounds = 100;
    for (int s = 0; s < SHAPES; s++) random_shape(s);
    int64_t kept = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t i = 0; i < SHAPES; i++) {
            int64_t limit = (r * 37 + i * 11) % 401 - 200;
            TreeNode *t = sufficient_subset(build((int)i, 0), limit);
            int64_t k = count(t);
            release(t);
            kept += k;
            check = (check * 31 + k + i) % 1000000007;
        }
    }
    printf("%lld rounds over 200 trees of 1000 nodes: %lld nodes kept, checksum %lld\n", (long long)rounds,
           (long long)kept, (long long)check);
    return 0;
}
