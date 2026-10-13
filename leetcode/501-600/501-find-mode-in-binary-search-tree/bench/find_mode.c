// Benchmark for #501: C mirror of the ★ arm (in-order with a running
// count); see find_mode.kara. Each traversal collects its modes into a
// fresh array grown by doubling, as the ★ arm pushes onto `Vec.new()`.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left, *right;
} TreeNode;

typedef struct {
    int64_t prev, run, best;
    int64_t *modes;
    int64_t len, cap;
} Walk;

static void push(Walk *w, int64_t v) {
    if (w->len == w->cap) {
        w->cap = w->cap ? w->cap * 2 : 4;
        w->modes = realloc(w->modes, w->cap * sizeof(int64_t));
    }
    w->modes[w->len++] = v;
}

static void visit(const TreeNode *n, Walk *w) {
    if (!n) return;
    visit(n->left, w);
    if (w->run > 0 && n->val == w->prev) {
        w->run++;
    } else {
        w->prev = n->val;
        w->run = 1;
    }
    if (w->run > w->best) {
        w->best = w->run;
        w->len = 0;
        push(w, n->val);
    } else if (w->run == w->best) {
        push(w, n->val);
    }
    visit(n->right, w);
}

static Walk find_mode(const TreeNode *root) {
    Walk w = {0, 0, 0, NULL, 0, 0};
    visit(root, &w);
    return w;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static TreeNode *fresh(int64_t v) {
    TreeNode *n = malloc(sizeof(TreeNode));
    n->val = v;
    n->left = n->right = NULL;
    return n;
}

static TreeNode *build(const int64_t *values, int64_t len, int64_t *seed) {
    TreeNode *root = fresh(values[0]);
    for (int64_t i = 1; i < len; i++) {
        int64_t v = values[i];
        TreeNode *node = root;
        for (;;) {
            if (v < node->val || (v == node->val && next_random(seed) % 2 == 0)) {
                if (node->left) {
                    node = node->left;
                } else {
                    node->left = fresh(v);
                    break;
                }
            } else {
                if (node->right) {
                    node = node->right;
                } else {
                    node->right = fresh(v);
                    break;
                }
            }
        }
    }
    return root;
}

int main(void) {
    // 100 random search trees of 10,000 values, drawn from 1 to 10
    // values, 1,000 values, or the whole range -100,000 to 100,000 in
    // turn, built once. Then the modes of each tree are found 30 times.
    int64_t trees = 100;
    int64_t seed = 501;
    TreeNode **all = malloc(trees * sizeof(TreeNode *));
    int64_t *values = malloc(10000 * sizeof(int64_t));
    for (int64_t t = 0; t < trees; t++) {
        int64_t range = t % 3 == 0 ? 1 + next_random(&seed) % 10 : t % 3 == 1 ? 1000 : 200001;
        for (int64_t k = 0; k < 10000; k++) {
            int64_t v = next_random(&seed) * 7 % range;
            values[k] = range == 200001 ? v - 100000 : v;
        }
        all[t] = build(values, 10000, &seed);
    }
    int64_t modes = 0, checksum = 0;
    for (int r = 0; r < 30; r++) {
        for (int64_t t = 0; t < trees; t++) {
            Walk w = find_mode(all[t]);
            for (int64_t i = 0; i < w.len; i++) {
                modes++;
                checksum = (checksum * 31 + w.modes[i] + 100000) % 1000000007;
            }
            free(w.modes);
        }
    }
    printf("%lld trees of 10000 values, 30 times each: %lld modes, checksum %lld\n",
           (long long)trees, (long long)modes, (long long)checksum);
    return 0;
}
