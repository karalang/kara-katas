// Benchmark workload for LeetCode #103 — zigzag level order, C mirror (malloc *Node).
// Build 8 BSTs once, then K reps of DFS-with-depth zigzag on a data-dependent-selected tree,
// folding level count + each level's size + every value into a rolling hash. Each rep
// allocates a fresh result (array of dynamically-grown int rows, odd rows emitted reversed)
// and frees it — the allocation-bound churn the benchmark measures.
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

typedef struct { long long* data; long long len, cap; } Row;
typedef struct { Row* rows; long long len, cap; } Rows;

static void row_push(Row* r, long long v) {
    if (r->len == r->cap) { r->cap = r->cap ? r->cap * 2 : 4; r->data = realloc(r->data, r->cap * sizeof(long long)); }
    r->data[r->len++] = v;
}
static void rows_push_row(Rows* rs) {
    if (rs->len == rs->cap) { rs->cap = rs->cap ? rs->cap * 2 : 4; rs->rows = realloc(rs->rows, rs->cap * sizeof(Row)); }
    rs->rows[rs->len].data = NULL; rs->rows[rs->len].len = 0; rs->rows[rs->len].cap = 0;
    rs->len++;
}
static void free_tree(Node* n) { if (!n) return; free_tree(n->left); free_tree(n->right); free(n); }
static void dfs(Node* node, long long depth, Rows* rs) {
    if (!node) return;
    if (depth == rs->len) rows_push_row(rs);
    row_push(&rs->rows[depth], node->val);
    dfs(node->left, depth + 1, rs);
    dfs(node->right, depth + 1, rs);
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
    for (long long rep = 0; rep < 600000; rep++) {
        long long idx = acc % 8;
        Rows rs = { NULL, 0, 0 };
        dfs(pool[idx], 0, &rs);
        // Build the zigzag output as a fresh Rows: even rows copied, odd rows reversed
        // (mirrors the kara `out` allocation), then fold it left-to-right.
        Rows out = { NULL, 0, 0 };
        for (long long d = 0; d < rs.len; d++) {
            Row* r = &rs.rows[d];
            rows_push_row(&out);
            if (d % 2 == 0) {
                for (long long i = 0; i < r->len; i++) row_push(&out.rows[d], r->data[i]);
            } else {
                for (long long i = r->len - 1; i >= 0; i--) row_push(&out.rows[d], r->data[i]);
            }
            free(r->data);
        }
        free(rs.rows);
        acc = (acc * 131 + out.len) % MOD;
        for (long long d = 0; d < out.len; d++) {
            Row* r = &out.rows[d];
            acc = (acc * 131 + r->len) % MOD;
            for (long long i = 0; i < r->len; i++) acc = (acc * 131 + r->data[i]) % MOD;
            free(r->data);
        }
        free(out.rows);
    }
    printf("%lld\n", acc);
    for (long long t = 0; t < 8; t++) free_tree(pool[t]);
    return 0;
}
