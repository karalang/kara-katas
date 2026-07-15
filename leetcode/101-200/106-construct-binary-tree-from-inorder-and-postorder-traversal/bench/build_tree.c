// Benchmark workload for LeetCode #106 — construct binary tree (inorder+postorder), C mirror.
// Build 8 (inorder, postorder) input pairs once, then K reps of the recursive index-bounds
// reconstruction on a data-dependent-selected pair, folding the rebuilt tree's shape+value
// serialization into a rolling hash. Each rep mallocs a fresh 15-node tree and frees it.
// Linear inorder scan (O(n^2)) for parity.
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
static long long find_in(const long long* in, long long lo, long long hi, long long target) {
    for (long long i = lo; i <= hi; i++) if (in[i] == target) return i;
    return -1;
}
static Node* build(const long long* post, const long long* in,
                   long long plo, long long phi, long long ilo, long long ihi) {
    if (plo > phi) return NULL;
    long long rv = post[phi];
    long long mid = find_in(in, ilo, ihi, rv);
    long long lsize = mid - ilo;
    Node* n = malloc(sizeof(Node));
    n->val = rv;
    n->left  = build(post, in, plo, plo + lsize - 1, ilo, mid - 1);
    n->right = build(post, in, plo + lsize, phi - 1, mid + 1, ihi);
    return n;
}
static long long ser(Node* n, long long acc) {
    if (!n) return (acc * 131 + 1) % MOD;
    acc = (acc * 131 + (n->val + 2)) % MOD;
    acc = ser(n->left, acc);
    acc = ser(n->right, acc);
    return acc;
}
static void free_tree(Node* n) { if (!n) return; free_tree(n->left); free_tree(n->right); free(n); }
static void inorder_of(Node* n, long long* out, long long* k) { if (!n) return; inorder_of(n->left, out, k); out[(*k)++] = n->val; inorder_of(n->right, out, k); }
static void postorder_of(Node* n, long long* out, long long* k) { if (!n) return; postorder_of(n->left, out, k); postorder_of(n->right, out, k); out[(*k)++] = n->val; }

int main(void) {
    long long base[] = {8, 4, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15};
    long long bn = 15;
    long long inos[8][15], posts[8][15];
    for (long long t = 0; t < 8; t++) {
        Node* root = NULL;
        for (long long k = 0; k < bn; k++) root = insert(root, base[(k + t) % bn]);
        long long ki = 0, kp = 0;
        inorder_of(root, inos[t], &ki);
        postorder_of(root, posts[t], &kp);
        free_tree(root);
    }
    long long acc = 1;
    for (long long rep = 0; rep < 800000; rep++) {
        long long idx = acc % 8;
        Node* rebuilt = build(posts[idx], inos[idx], 0, bn - 1, 0, bn - 1);
        long long s = ser(rebuilt, 0);
        free_tree(rebuilt);
        acc = (acc * 131 + s) % MOD;
    }
    printf("%lld\n", acc);
    return 0;
}
