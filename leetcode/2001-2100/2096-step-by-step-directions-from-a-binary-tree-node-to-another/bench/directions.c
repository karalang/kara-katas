// LeetCode #2096: Step-By-Step Directions From a Binary Tree Node to
// Another -- C mirror of the ★ arm's benchmark (directions.kara): the same
// random tree of 100000 `malloc`'d nodes and 1000 questions, each answered
// by the same two depth-first searches into growable `char` buffers.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left, *right;
} TreeNode;

typedef struct { char *v; int64_t len, cap; } Buf;

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t wide_random(int64_t *seed) {
    int64_t hi = next_random(seed);
    return hi * 32768 + next_random(seed);
}

static void push(Buf *b, char c) {
    if (b->len == b->cap) {
        b->cap = b->cap ? b->cap * 2 : 16;
        b->v = realloc(b->v, b->cap);
    }
    b->v[b->len++] = c;
}

static int way_to(TreeNode *n, int64_t target, Buf *way) {
    if (n == NULL) return 0;
    if (n->val == target) return 1;
    push(way, 'L');
    if (way_to(n->left, target, way)) return 1;
    way->len--;
    push(way, 'R');
    if (way_to(n->right, target, way)) return 1;
    way->len--;
    return 0;
}

static Buf get_directions(TreeNode *root, int64_t start_value, int64_t dest_value) {
    Buf a = {0}, b = {0}, out = {0};
    way_to(root, start_value, &a);
    way_to(root, dest_value, &b);
    int64_t common = 0;
    while (common < a.len && common < b.len && a.v[common] == b.v[common]) common++;
    for (int64_t i = common; i < a.len; i++) push(&out, 'U');
    for (int64_t i = common; i < b.len; i++) push(&out, b.v[i]);
    free(a.v);
    free(b.v);
    return out;
}

int main(void) {
    int64_t seed = 2096, n = 100000;
    int64_t *values = malloc(n * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) values[i] = i + 1;
    for (int64_t i = n - 1; i >= 1; i--) {
        int64_t j = wide_random(&seed) % (i + 1);
        int64_t t = values[i];
        values[i] = values[j];
        values[j] = t;
    }
    TreeNode *nodes = malloc(n * sizeof(TreeNode));
    for (int64_t i = 0; i < n; i++) nodes[i] = (TreeNode){values[i], NULL, NULL};
    for (int64_t k = 1; k < n; k++) {
        TreeNode *at = &nodes[wide_random(&seed) % k];
        for (;;) {
            if (next_random(&seed) % 2 == 0) {
                if (at->left) at = at->left;
                else { at->left = &nodes[k]; break; }
            } else {
                if (at->right) at = at->right;
                else { at->right = &nodes[k]; break; }
            }
        }
    }
    int64_t steps = 0, check = 0;
    for (int q = 0; q < 1000; q++) {
        int64_t s = wide_random(&seed) % n + 1;
        int64_t t = (s + wide_random(&seed) % (n - 1)) % n + 1;
        Buf way = get_directions(&nodes[0], s, t);
        steps += way.len;
        for (int64_t i = 0; i < way.len; i++) check = (check * 31 + way.v[i]) % 1000000007;
        free(way.v);
    }
    printf("1000 answers: %lld steps, checksum %lld\n", (long long)steps, (long long)check);
    free(nodes);
    free(values);
    return 0;
}
