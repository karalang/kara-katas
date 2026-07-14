// Benchmark workload for LeetCode #102 — level order, C mirror (malloc *Node).
// Build 8 BSTs once, then K reps of DFS-with-depth level_order on a data-dependent-
// selected tree, folding level count + each level's size + every value into a rolling
// hash. Each rep allocates a fresh result (an array of dynamically-grown int arrays,
// one per depth) and frees it — the allocation-bound churn the benchmark measures.
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

// A growable row of values.
typedef struct { long long* data; long long len, cap; } Row;
// A growable result: rows indexed by depth.
typedef struct { Row* rows; long long len, cap; } Result;

static void row_push(Row* r, long long v) {
    if (r->len == r->cap) { r->cap = r->cap ? r->cap * 2 : 4; r->data = realloc(r->data, r->cap * sizeof(long long)); }
    r->data[r->len++] = v;
}
static void result_push_row(Result* res) {
    if (res->len == res->cap) { res->cap = res->cap ? res->cap * 2 : 4; res->rows = realloc(res->rows, res->cap * sizeof(Row)); }
    res->rows[res->len].data = NULL; res->rows[res->len].len = 0; res->rows[res->len].cap = 0;
    res->len++;
}

static void dfs(Node* node, long long depth, Result* res) {
    if (!node) return;
    if (depth == res->len) result_push_row(res);
    row_push(&res->rows[depth], node->val);
    dfs(node->left, depth + 1, res);
    dfs(node->right, depth + 1, res);
}

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
    for (long long rep = 0; rep < 1500000; rep++) {
        long long idx = acc % 8;
        Result res = { NULL, 0, 0 };
        dfs(pool[idx], 0, &res);
        acc = (acc * 131 + res.len) % MOD;
        for (long long li = 0; li < res.len; li++) {
            Row* lvl = &res.rows[li];
            acc = (acc * 131 + lvl->len) % MOD;
            for (long long vi = 0; vi < lvl->len; vi++)
                acc = (acc * 131 + lvl->data[vi]) % MOD;
            free(lvl->data);
        }
        free(res.rows);
    }
    printf("%lld\n", acc);
    return 0;
}
