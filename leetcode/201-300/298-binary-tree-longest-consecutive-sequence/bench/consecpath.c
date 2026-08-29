/* LeetCode 298 benchmark lane — C mirror of consecpath.kara.
 *
 * Same tree, same passes, same sink: build one perfect depth-20 tree, then 40
 * full traversals with steps 1..40. See the .kara file's header for the
 * workload rationale. */
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    long long val;
    struct Node *left, *right;
} Node;

static Node *build(int depth, long long parent_val, long long *state) {
    if (depth <= 0) return NULL;
    *state = (*state * 1103515245LL + 12345LL) & 0x7fffffffLL;
    long long v = parent_val + *state % 3 - 1;
    /* Children are allocated BEFORE the parent, matching the Rust, Go, Kara and
     * Python mirrors — all four construct a node from already-built children,
     * so the parent is necessarily the last allocation in its subtree.
     *
     * This is not a stylistic choice. Allocating the parent FIRST (the obvious
     * C spelling) lays a node out adjacent to its left child and is worth 1.7x
     * on this workload, measured: 0.34 s parent-first against 0.58 s
     * children-first, same binary otherwise. Benchmarking that against four
     * children-first mirrors would have been comparing allocation orders, not
     * implementations. See ../README.md § "The C mirror was 1.7x faster for a
     * reason that had nothing to do with C". */
    Node *l = build(depth - 1, v, state);
    Node *r = build(depth - 1, v, state);
    Node *n = (Node *)malloc(sizeof(Node));
    n->val = v;
    n->left = l;
    n->right = r;
    return n;
}

static void free_tree(Node *t) {
    if (!t) return;
    free_tree(t->left);
    free_tree(t->right);
    free(t);
}

static long long down(const Node *t, long long step, long long *best) {
    if (!t) return 0;
    long long l = down(t->left, step, best);
    long long r = down(t->right, step, best);
    long long run = 1;
    if (t->left && t->left->val == t->val + step && l + 1 > run) run = l + 1;
    if (t->right && t->right->val == t->val + step && r + 1 > run) run = r + 1;
    if (run > *best) *best = run;
    return run;
}

static long long longest_with_step(const Node *t, long long step) {
    long long best = 0;
    down(t, step, &best);
    return best;
}

int main(void) {
    const int depth = 20;
    const int passes = 40;

    long long state = 12345;
    Node *tree = build(depth, 0, &state);

    long long checksum = 0;
    for (int d = 1; d <= passes; d++)
        checksum = (checksum * 31 + longest_with_step(tree, d)) % 1000000007LL;

    printf("depth %d passes %d checksum %lld\n", depth, passes, checksum);
    free_tree(tree);
    return 0;
}
