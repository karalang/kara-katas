// Benchmark: LeetCode #951 Flip Equivalent Binary Trees -- the ★ arm,
// both pairings tried, on pairs of trees of 100 nodes, LeetCode's
// largest. Mirrors flip_equiv.kara, .rs, .py and go-seq/.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 100
#define COUNT 20

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left, *right;
} TreeNode;

static bool flip_equiv(const TreeNode *a, const TreeNode *b) {
    if (a == NULL && b == NULL) return true;
    if (a == NULL || b == NULL) return false;
    return a->val == b->val &&
           ((flip_equiv(a->left, b->left) && flip_equiv(a->right, b->right)) ||
            (flip_equiv(a->left, b->right) && flip_equiv(a->right, b->left)));
}

static int64_t seed = 951;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static TreeNode *new_node(int64_t val, TreeNode *left, TreeNode *right) {
    TreeNode *t = malloc(sizeof(TreeNode));
    t->val = val;
    t->left = left;
    t->right = right;
    return t;
}

static TreeNode *random_tree(const int64_t *values, int64_t n) {
    TreeNode *root = new_node(values[0], NULL, NULL);
    for (int64_t i = 1; i < n; i++) {
        TreeNode *node = new_node(values[i], NULL, NULL);
        TreeNode *cur = root;
        for (;;) {
            if (next_random() % 2 == 0) {
                if (cur->left) cur = cur->left;
                else { cur->left = node; break; }
            } else {
                if (cur->right) cur = cur->right;
                else { cur->right = node; break; }
            }
        }
    }
    return root;
}

static TreeNode *flipped_copy(const TreeNode *t, const int64_t *rename) {
    if (t == NULL) return NULL;
    TreeNode *l = flipped_copy(t->left, rename);
    TreeNode *r = flipped_copy(t->right, rename);
    if (next_random() % 2 == 0) return new_node(rename[t->val], l, r);
    return new_node(rename[t->val], r, l);
}

static void free_tree(TreeNode *t) {
    if (t == NULL) return;
    free_tree(t->left);
    free_tree(t->right);
    free(t);
}

int main(void) {
    const int64_t rounds = 50000, count = COUNT, n = N;
    TreeNode *firsts[COUNT], *seconds[COUNT];
    for (int64_t c = 0; c < count; c++) {
        int64_t values[N], rename[N];
        for (int64_t i = 0; i < n; i++) values[i] = i;
        for (int64_t i = 0; i < n; i++) {
            int64_t j = i + next_random() % (n - i);
            int64_t tmp = values[i];
            values[i] = values[j];
            values[j] = tmp;
        }
        TreeNode *t = random_tree(values, n);
        for (int64_t i = 0; i < n; i++) rename[i] = i;
        if (c % 2 == 1) {
            int64_t a = next_random() % n;
            int64_t b = next_random() % n;
            rename[a] = b;
            rename[b] = a;
        }
        seconds[c] = flipped_copy(t, rename);
        firsts[c] = t;
    }
    int64_t yes = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t i = 0; i < count; i++) {
            int64_t k = (r + i) % count;
            int64_t bit = flip_equiv(firsts[k], seconds[k]) ? 1 : 0;
            yes += bit;
            check = (check * 31 + bit + k) % 1000000007;
        }
    }
    printf("%lld rounds over %lld pairs of trees of %lld nodes: %lld flip equivalent, checksum %lld\n",
           (long long)rounds, (long long)count, (long long)n, (long long)yes, (long long)check);
    for (int64_t c = 0; c < count; c++) {
        free_tree(firsts[c]);
        free_tree(seconds[c]);
    }
    return 0;
}
