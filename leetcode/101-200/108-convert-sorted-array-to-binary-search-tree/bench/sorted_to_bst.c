// Benchmark workload for LeetCode #108 — sorted array to BST, C mirror (malloc *Node).
// Build 8 sorted arrays once, then K reps of recursive middle-pick sorted_to_bst on a
// data-dependent-selected array, folding the built tree's shape+value serialization into a
// rolling hash. Each rep mallocs a fresh 15-node balanced tree and frees it.
#include <stdio.h>
#include <stdlib.h>
#define MOD 1000000007LL

typedef struct Node { long long val; struct Node *left, *right; } Node;

static Node* build(const long long* arr, long long lo, long long hi) {
    if (lo > hi) return NULL;
    long long mid = (lo + hi) / 2;
    Node* n = malloc(sizeof(Node));
    n->val = arr[mid];
    n->left  = build(arr, lo, mid - 1);
    n->right = build(arr, mid + 1, hi);
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

int main(void) {
    long long arrs[8][15];
    for (long long t = 0; t < 8; t++)
        for (long long i = 0; i < 15; i++) arrs[t][i] = t * 100 + i;
    long long acc = 1;
    for (long long rep = 0; rep < 1200000; rep++) {
        long long idx = acc % 8;
        Node* root = build(arrs[idx], 0, 14);
        long long s = ser(root, 0);
        free_tree(root);
        acc = (acc * 131 + s) % MOD;
    }
    printf("%lld\n", acc);
    return 0;
}
