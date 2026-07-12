// Benchmark workload for LeetCode #99 — recover BST, C mirror (malloc pointer tree).
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
static void collect(Node* node, Node** arr, long long* cnt) {
    if (!node) return;
    collect(node->left, arr, cnt);
    arr[(*cnt)++] = node;
    collect(node->right, arr, cnt);
}
static void sum_inorder(Node* node, long long* acc) {
    if (!node) return;
    sum_inorder(node->left, acc);
    *acc = (*acc * 131 + node->val) % MOD;
    sum_inorder(node->right, acc);
}
static void recover(Node* root, long long n) {
    Node** buf = malloc((size_t)n * sizeof(Node*));
    long long cnt = 0;
    collect(root, buf, &cnt);
    long long fi = -1, si = -1;
    for (long long i = 1; i < cnt; i++)
        if (buf[i - 1]->val > buf[i]->val) { if (fi < 0) fi = i - 1; si = i; }
    if (fi >= 0) { long long t = buf[fi]->val; buf[fi]->val = buf[si]->val; buf[si]->val = t; }
    free(buf);
}
static void corrupt2(Node* root, long long a, long long b, long long n) {
    Node** buf = malloc((size_t)n * sizeof(Node*));
    long long cnt = 0;
    collect(root, buf, &cnt);
    if (a != b) { long long t = buf[a]->val; buf[a]->val = buf[b]->val; buf[b]->val = t; }
    free(buf);
}
int main(void) {
    long long vals[] = {16, 8, 24, 4, 12, 20, 28, 2, 6, 10, 14, 18, 22, 26, 30, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31};
    long long n = 31;
    Node* root = NULL;
    for (long long i = 0; i < n; i++) root = insert(root, vals[i]);
    long long acc = 1;
    for (long long rep = 0; rep < 700000; rep++) {
        long long a = acc % n, b = (acc * 7 + 3) % n;
        corrupt2(root, a, b, n);
        long long cs = 0;
        sum_inorder(root, &cs);
        acc = (acc * 131 + cs) % MOD;
        recover(root, n);
    }
    printf("%lld\n", acc);
    return 0;
}
