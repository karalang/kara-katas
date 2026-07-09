/*
 * Benchmark workload — Validate Binary Search Tree (LeetCode #98).
 * C mirror of bench/validate_bst.kara. Each iteration builds a fresh 63-node
 * balanced BST (malloc per node), runs the ★'s recursive (lo,hi)-bounds
 * validator, folds shift+valid into a rolling polynomial hash, then frees the
 * tree — the C analogue of Kāra's per-iteration RC tree build/validate/drop.
 * See ../README.md § Benchmarks.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

typedef struct Node { int64_t val; struct Node *l, *r; } Node;

static Node *build(int64_t lo, int64_t hi, int64_t shift) {
    if (lo > hi) return NULL;
    int64_t mid = lo + (hi - lo) / 2;
    Node *n = (Node *)malloc(sizeof(Node));
    n->val = shift + mid;
    n->l = build(lo, mid - 1, shift);
    n->r = build(mid + 1, hi, shift);
    return n;
}

/* has_lo / has_hi model the Option[i64] bounds (None = no bound on that side). */
static int is_valid(Node *n, int64_t lo, int has_lo, int64_t hi, int has_hi) {
    if (!n) return 1;
    if (has_lo && n->val <= lo) return 0;
    if (has_hi && n->val >= hi) return 0;
    return is_valid(n->l, lo, has_lo, n->val, 1) && is_valid(n->r, n->val, 1, hi, has_hi);
}

static void free_tree(Node *n) {
    if (!n) return;
    free_tree(n->l);
    free_tree(n->r);
    free(n);
}

int main(void) {
    const int64_t total = 200000;
    const int64_t modulus = 1000000007;
    const int64_t size = 63;

    int64_t acc = 0;
    for (int64_t k = 0; k < total; k++) {
        int64_t shift = k % 1000;
        Node *root = build(0, size - 1, shift);
        int64_t bit = is_valid(root, 0, 0, 0, 0);
        acc = (acc * 131 + shift + bit) % modulus;
        free_tree(root);
    }

    printf("%lld\n", (long long)acc);
    return 0;
}
