// LeetCode #1305 bench in C: the ★ arm (each tree read in order into its
// own array, then the two merged into a fresh `malloc`) on the same 20 pairs
// of search trees and 100 passes.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int val;
    struct TreeNode *left;
    struct TreeNode *right;
} TreeNode;

typedef struct {
    int *data;
    size_t len;
    size_t cap;
} IntVec;

static void push(IntVec *v, int x) {
    if (v->len == v->cap) {
        v->cap = v->cap ? v->cap * 2 : 4;
        v->data = realloc(v->data, sizeof(int) * v->cap);
    }
    v->data[v->len++] = x;
}

static void in_order(TreeNode *node, IntVec *out) {
    if (node) {
        in_order(node->left, out);
        push(out, node->val);
        in_order(node->right, out);
    }
}

static IntVec get_all_elements(TreeNode *root1, TreeNode *root2) {
    IntVec a = {0}, b = {0}, out = {0};
    in_order(root1, &a);
    in_order(root2, &b);
    size_t i = 0, j = 0;
    while (i < a.len || j < b.len) {
        if (j == b.len || (i < a.len && a.data[i] <= b.data[j])) {
            push(&out, a.data[i++]);
        } else {
            push(&out, b.data[j++]);
        }
    }
    free(a.data);
    free(b.data);
    return out;
}

static int64_t seed = 1305;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static TreeNode *new_node(int v) {
    TreeNode *t = malloc(sizeof(TreeNode));
    t->val = v;
    t->left = NULL;
    t->right = NULL;
    return t;
}

static void insert(TreeNode *root, int v) {
    TreeNode *at = root;
    for (;;) {
        if (v == at->val) return;
        TreeNode **next = v < at->val ? &at->left : &at->right;
        if (!*next) {
            *next = new_node(v);
            return;
        }
        at = *next;
    }
}

static TreeNode *random_bst(int n) {
    TreeNode *root = new_node((int)(next_random() % 200001 - 100000));
    for (int k = 1; k < n; k++) insert(root, (int)(next_random() % 200001 - 100000));
    return root;
}

int main(void) {
    TreeNode *firsts[20], *seconds[20];
    for (int p = 0; p < 20; p++) {
        firsts[p] = random_bst(4900);
        seconds[p] = random_bst(4900);
    }
    int64_t check = 0;
    for (int64_t pass = 0; pass < 100; pass++) {
        for (int p = 0; p < 20; p++) {
            insert(firsts[p], (int)(check % 200001 - 100000));
            IntVec got = get_all_elements(firsts[p], seconds[p]);
            int64_t x = got.data[check % (int64_t)got.len];
            check = (check * 31 + x + 100000 + (int64_t)got.len + pass) % 1000000007;
            free(got.data);
        }
    }
    printf("100 passes over 20 pairs of trees: checksum %lld\n", (long long)check);
    return 0;
}
