// Benchmark workload for LeetCode #100 — same tree, C mirror (*Node, read-only).
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
static int is_same(Node* p, Node* q) {
    if (!p) return q == NULL;
    if (!q) return 0;
    return p->val == q->val && is_same(p->left, q->left) && is_same(p->right, q->right);
}
int main(void) {
    long long base[] = {16, 8, 24, 4, 12, 20, 28, 2, 6, 10, 14, 18, 22, 26, 30};
    long long bn = 15;
    Node* pool_p[8]; Node* pool_q[8];
    for (long long i = 0; i < 8; i++) {
        Node *p = NULL, *q = NULL;
        for (long long k = 0; k < bn; k++) {
            p = insert(p, base[k]);
            long long bump = ((i % 2) == 1 && k == (i % bn)) ? 1 : 0;
            q = insert(q, base[k] + bump);
        }
        pool_p[i] = p; pool_q[i] = q;
    }
    long long acc = 1;
    for (long long rep = 0; rep < 6000000; rep++) {
        long long idx = acc % 8;
        int same = is_same(pool_p[idx], pool_q[idx]);
        acc = (acc * 131 + (same ? 1 : 0) + 1) % MOD;
    }
    printf("%lld\n", acc);
    return 0;
}
