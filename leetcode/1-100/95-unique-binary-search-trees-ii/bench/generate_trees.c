// LeetCode #95: Unique Binary Search Trees II — recursive divide & conquer.
// C mirror of generate_trees.kara. Same algorithm: for each root value i in
// [lo, hi], take the cross product of every left subtree (lo..i-1) and every
// right subtree (i+1..hi). Kara shares subtree instances via RC; C owns its
// trees outright, so each (left, right) pair is DEEP-COPIED into the new root —
// the same set of trees, the same canonical preorder serialization ("#," null /
// "val," node) and the same fold, so stdout is byte-identical.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MOD 1000000007LL

typedef struct Node {
    long long val;
    struct Node *left, *right;
} Node;

typedef struct { Node **data; long long len, cap; } Vec;

static void vec_push(Vec *v, Node *n) {
    if (v->len == v->cap) {
        v->cap = v->cap ? v->cap * 2 : 4;
        v->data = realloc(v->data, (size_t)v->cap * sizeof(Node *));
    }
    v->data[v->len++] = n;
}

static Node *node_new(long long val, Node *left, Node *right) {
    Node *n = malloc(sizeof(Node));
    n->val = val; n->left = left; n->right = right;
    return n;
}

static Node *node_copy(const Node *n) {
    if (!n) return NULL;
    return node_new(n->val, node_copy(n->left), node_copy(n->right));
}

static void node_free(Node *n) {
    if (!n) return;
    node_free(n->left); node_free(n->right);
    free(n);
}

// Every BST over the contiguous value range [lo, hi].
static Vec build_all(long long lo, long long hi) {
    Vec result = {0};
    if (lo > hi) { vec_push(&result, NULL); return result; }
    for (long long i = lo; i <= hi; i++) {
        Vec lefts = build_all(lo, i - 1);
        Vec rights = build_all(i + 1, hi);
        for (long long li = 0; li < lefts.len; li++)
            for (long long ri = 0; ri < rights.len; ri++)
                vec_push(&result, node_new(i, node_copy(lefts.data[li]), node_copy(rights.data[ri])));
        for (long long li = 0; li < lefts.len; li++) node_free(lefts.data[li]);
        for (long long ri = 0; ri < rights.len; ri++) node_free(rights.data[ri]);
        free(lefts.data); free(rights.data);
    }
    return result;
}

// Canonical preorder serialization with '#' null markers, appended to buf.
static void serialize(const Node *n, char **buf, size_t *len, size_t *cap) {
    char tmp[32];
    int w = n ? snprintf(tmp, sizeof tmp, "%lld,", n->val)
              : snprintf(tmp, sizeof tmp, "#,");
    if (*len + (size_t)w + 1 > *cap) {
        *cap = (*cap ? *cap * 2 : 64);
        while (*len + (size_t)w + 1 > *cap) *cap *= 2;
        *buf = realloc(*buf, *cap);
    }
    memcpy(*buf + *len, tmp, (size_t)w); *len += (size_t)w;
    if (n) { serialize(n->left, buf, len, cap); serialize(n->right, buf, len, cap); }
}

// Benchmark workload: 250 repeats of building every BST over 1..8, folding each
// tree's canonical preorder serialization into a rolling hash. Same fold as the
// kata; heavier iteration count so the wall-clock is measurable. See ../README.md.
static void bench_report(long long n, long long *acc) {
    Vec trees = build_all(1, n);
    long long count = trees.len;
    long long a = (*acc * 131 + (count + 1)) % MOD;
    for (long long t = 0; t < count; t++) {
        char *buf = NULL; size_t len = 0, cap = 0;
        serialize(trees.data[t], &buf, &len, &cap);
        for (size_t j = 0; j < len; j++)
            a = (a * 131 + (unsigned char)buf[j]) % MOD;
        a = (a * 131 + 7) % MOD;
        free(buf);
    }
    for (long long t = 0; t < count; t++) node_free(trees.data[t]);
    free(trees.data);
    *acc = a;
}

int main(void) {
    long long acc = 0;
    for (long long rep = 0; rep < 250; rep++)
        for (long long n = 1; n <= 8; n++) bench_report(n, &acc);
    printf("%lld\n", acc);
    return 0;
}
