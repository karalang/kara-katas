// Benchmark workload for LeetCode #110 — balanced binary tree, C mirror (*Node, read-only).
// Build 8 balanced 31-node trees once, then K reps of bottom-up single-pass is_balanced on a
// data-dependent-selected tree, folding each verdict into a rolling hash. Read-only per-node
// post-order traversal, no allocation.
#include <stdio.h>
#include <stdlib.h>
#define MOD 1000000007LL

typedef struct Node { long long val; struct Node *left, *right; } Node;

static Node* build_balanced(long long lo, long long hi) {
    if (lo > hi) return NULL;
    long long mid = (lo + hi) / 2;
    Node* n = malloc(sizeof(Node));
    n->val = mid;
    n->left  = build_balanced(lo, mid - 1);
    n->right = build_balanced(mid + 1, hi);
    return n;
}
static long long check(Node* n) {
    if (!n) return 0;
    long long lh = check(n->left);
    if (lh == -1) return -1;
    long long rh = check(n->right);
    if (rh == -1) return -1;
    long long diff = lh - rh;
    if ((diff < 0 ? -diff : diff) > 1) return -1;
    return 1 + (lh > rh ? lh : rh);
}
static int is_balanced(Node* root) { return check(root) != -1; }
static void free_tree(Node* n) { if (!n) return; free_tree(n->left); free_tree(n->right); free(n); }

int main(void) {
    Node* pool[8];
    for (long long t = 0; t < 8; t++) pool[t] = build_balanced(t * 100, t * 100 + 30);
    long long acc = 1;
    for (long long rep = 0; rep < 3000000; rep++) {
        long long idx = acc % 8;
        int bal = is_balanced(pool[idx]);
        acc = (acc * 131 + (bal ? 1 : 0) + 1) % MOD;
    }
    printf("%lld\n", acc);
    for (long long t = 0; t < 8; t++) free_tree(pool[t]);
    return 0;
}
