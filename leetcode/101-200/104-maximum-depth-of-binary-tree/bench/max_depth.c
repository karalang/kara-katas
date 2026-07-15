// Benchmark workload for LeetCode #104 — max depth, C mirror (*Node, read-only).
// Build 8 BSTs once, then K reps of recursive max_depth on a data-dependent-selected tree,
// folding each depth into a rolling hash. Read-only per-node traversal, no allocation.
#include <stdio.h>
#include <stdlib.h>
#define MOD 1000000007LL

typedef struct Node { long long val; struct Node *left, *right; } Node;

static Node* insert(Node* root, long long v) {
    if (!root) { Node* n = malloc(sizeof(Node)); n->val = v; n->left = n->right = NULL; return n; }
    if (v < root->val) root->left = insert(root->left, v);
    else root->right = insert(root->right, v);
    return root;
}
static long long max_depth(Node* n) {
    if (!n) return 0;
    long long lh = max_depth(n->left);
    long long rh = max_depth(n->right);
    return 1 + (lh > rh ? lh : rh);
}
static void free_tree(Node* n) { if (!n) return; free_tree(n->left); free_tree(n->right); free(n); }

int main(void) {
    long long base[] = {16, 8, 24, 4, 12, 20, 28, 2, 6, 10, 14, 18, 22, 26, 30};
    long long bn = 15;
    Node* pool[8];
    for (long long t = 0; t < 8; t++) {
        Node* root = NULL;
        for (long long k = 0; k < bn; k++) root = insert(root, base[(k + t) % bn]);
        pool[t] = root;
    }
    long long acc = 1;
    for (long long rep = 0; rep < 4000000; rep++) {
        long long idx = acc % 8;
        long long d = max_depth(pool[idx]);
        acc = (acc * 131 + d + 1) % MOD;
    }
    printf("%lld\n", acc);
    for (long long t = 0; t < 8; t++) free_tree(pool[t]);
    return 0;
}
