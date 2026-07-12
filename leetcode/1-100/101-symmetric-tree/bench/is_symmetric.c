// Benchmark workload for LeetCode #101 — symmetric tree, C mirror (*Node, read-only).
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
static Node* mirror(Node* n) {
    if (!n) return NULL;
    Node* m = malloc(sizeof(Node)); m->val = n->val; m->left = mirror(n->right); m->right = mirror(n->left); return m;
}
static Node* copy_tree(Node* n) {
    if (!n) return NULL;
    Node* m = malloc(sizeof(Node)); m->val = n->val; m->left = copy_tree(n->left); m->right = copy_tree(n->right); return m;
}
static int is_mirror(Node* a, Node* b) {
    if (!a) return b == NULL;
    if (!b) return 0;
    return a->val == b->val && is_mirror(a->left, b->right) && is_mirror(a->right, b->left);
}
static int is_symmetric(Node* root) {
    if (!root) return 1;
    return is_mirror(root->left, root->right);
}
int main(void) {
    long long base[] = {8, 4, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15};
    long long bn = 15;
    Node* pool[8];
    for (long long i = 0; i < 8; i++) {
        Node* sub = NULL;
        for (long long k = 0; k < bn; k++) sub = insert(sub, base[(k + i) % bn]);
        Node* root = malloc(sizeof(Node)); root->val = 0;
        root->left = sub;
        root->right = ((i % 2) == 0) ? mirror(sub) : copy_tree(sub);
        pool[i] = root;
    }
    long long acc = 1;
    for (long long rep = 0; rep < 8000000; rep++) {
        long long idx = acc % 8;
        int sym = is_symmetric(pool[idx]);
        acc = (acc * 131 + (sym ? 1 : 0) + 1) % MOD;
    }
    printf("%lld\n", acc);
    return 0;
}
