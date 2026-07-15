// Benchmark workload for LeetCode #111 — minimum depth, C mirror (*Node, read-only).
// Build 8 balanced 31-node trees once, then K reps of recursive min_depth on a data-dependent-
// selected tree, folding each min depth into a rolling hash. Read-only per-node post-order.
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
static long long min_depth(Node* n) {
    if (!n) return 0;
    long long ld = min_depth(n->left);
    long long rd = min_depth(n->right);
    if (ld == 0) return 1 + rd;
    if (rd == 0) return 1 + ld;
    return 1 + (ld < rd ? ld : rd);
}
static void free_tree(Node* n) { if (!n) return; free_tree(n->left); free_tree(n->right); free(n); }

int main(void) {
    Node* pool[8];
    for (long long t = 0; t < 8; t++) pool[t] = build_balanced(t * 100, t * 100 + 30);
    long long acc = 1;
    for (long long rep = 0; rep < 3000000; rep++) {
        long long idx = acc % 8;
        long long d = min_depth(pool[idx]);
        acc = (acc * 131 + d + 1) % MOD;
    }
    printf("%lld\n", acc);
    for (long long t = 0; t < 8; t++) free_tree(pool[t]);
    return 0;
}
