// LeetCode #114 bench — flatten, C mirror (raw *Node, iterative Morris rewiring).
#include <stdio.h>
#include <stdlib.h>
#define MOD 1000000007L
typedef struct Node { long val; struct Node *left, *right; } Node;
static Node* build_balanced(long lo, long hi) {
    if (lo > hi) return NULL;
    long mid = (lo+hi)/2;
    Node* n = malloc(sizeof(Node));
    n->val = mid; n->left = build_balanced(lo, mid-1); n->right = build_balanced(mid+1, hi);
    return n;
}
static void flatten(Node* root) {
    Node* curr = root;
    while (curr) {
        if (curr->left) {
            Node* prev = curr->left;
            while (prev->right) prev = prev->right;
            prev->right = curr->right; curr->right = curr->left; curr->left = NULL;
        }
        curr = curr->right;
    }
}
static long spine_hash(Node* root) {
    long h = 1; for (Node* c = root; c; c = c->right) h = (h*131 + c->val + 1000) % MOD; return h;
}
static void free_spine(Node* root) { while (root) { Node* nx = root->right; free(root); root = nx; } }
int main(void) {
    long acc = 1;
    for (long rep=0; rep<200000; rep++) {
        long base = acc % 100;
        Node* root = build_balanced(base, base+62);
        flatten(root);
        long h = spine_hash(root);
        acc = (acc*1000003 + h + 1) % MOD;
        free_spine(root);
    }
    printf("%ld\n", acc);
    return 0;
}
