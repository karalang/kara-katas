// Benchmark workload for LeetCode #109 — sorted list to BST, C mirror (malloc *Node).
// Build 8 sorted linked lists once (kept alive across reps), then K reps of the array-
// conversion sorted_list_to_bst on a data-dependent-selected list: walk the list into a local
// array, build a fresh balanced tree by middle-pick, fold its serialization, free the tree.
#include <stdio.h>
#include <stdlib.h>
#define MOD 1000000007LL

typedef struct LNode { long long val; struct LNode* next; } LNode;
typedef struct TNode { long long val; struct TNode *left, *right; } TNode;

static LNode* build_list(long long len, long long off) {
    LNode* head = NULL;
    for (long long i = len - 1; i >= 0; i--) {
        LNode* n = malloc(sizeof(LNode));
        n->val = off + 1 + i;
        n->next = head;
        head = n;
    }
    return head;
}
static TNode* build_from_arr(const long long* arr, long long lo, long long hi) {
    if (lo > hi) return NULL;
    long long mid = (lo + hi) / 2;
    TNode* n = malloc(sizeof(TNode));
    n->val = arr[mid];
    n->left  = build_from_arr(arr, lo, mid - 1);
    n->right = build_from_arr(arr, mid + 1, hi);
    return n;
}
static TNode* sorted_list_to_bst(LNode* head) {
    long long arr[64];
    long long n = 0;
    for (LNode* c = head; c; c = c->next) arr[n++] = c->val;
    return build_from_arr(arr, 0, n - 1);
}
static long long ser(TNode* n, long long acc) {
    if (!n) return (acc * 131 + 1) % MOD;
    acc = (acc * 131 + (n->val + 2)) % MOD;
    acc = ser(n->left, acc);
    acc = ser(n->right, acc);
    return acc;
}
static void free_tree(TNode* n) { if (!n) return; free_tree(n->left); free_tree(n->right); free(n); }
static void free_list(LNode* h) { while (h) { LNode* nx = h->next; free(h); h = nx; } }

int main(void) {
    LNode* pool[8];
    for (long long t = 0; t < 8; t++) pool[t] = build_list(15, t * 100);
    long long acc = 1;
    for (long long rep = 0; rep < 1000000; rep++) {
        long long idx = acc % 8;
        TNode* root = sorted_list_to_bst(pool[idx]);
        long long s = ser(root, 0);
        free_tree(root);
        acc = (acc * 131 + s) % MOD;
    }
    printf("%lld\n", acc);
    for (long long t = 0; t < 8; t++) free_list(pool[t]);
    return 0;
}
