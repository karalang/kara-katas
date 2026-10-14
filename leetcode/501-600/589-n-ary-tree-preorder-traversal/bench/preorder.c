// Benchmark for #589: C mirror of the ★ arm (recursion); see
// preorder.kara. A node holds its children in one malloc'd array of
// nodes, as a Kāra Vec[Node] holds them inline, and each call returns a
// fresh array that doubles as it fills, as a Kāra Vec grows.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int64_t val;
    struct Node *children;
    int64_t len;
} Node;

typedef struct {
    int64_t *data;
    int64_t len, cap;
} List;

static void push(List *out, int64_t v) {
    if (out->len == out->cap) {
        out->cap = out->cap ? out->cap * 2 : 4;
        out->data = realloc(out->data, out->cap * sizeof(int64_t));
    }
    out->data[out->len++] = v;
}

static void walk(const Node *node, List *out) {
    push(out, node->val);
    for (int64_t i = 0; i < node->len; i++) walk(&node->children[i], out);
}

static List preorder(const Node *root) {
    List out = {NULL, 0, 0};
    if (root) walk(root, &out);
    return out;
}

// ---- benchmark --------------------------------------------------------------

#define N 10000
static int64_t vals[N], parent[N], nkids[N], start[N], order[N];

static void build_random(int64_t i, Node *out) {
    out->val = vals[i];
    out->len = nkids[i];
    out->children = nkids[i] ? malloc(nkids[i] * sizeof(Node)) : NULL;
    for (int64_t k = 0; k < nkids[i]; k++) build_random(order[start[i] + k], &out->children[k]);
}

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    enum { COUNT = 100, ROUNDS = 30 };
    int64_t seed = 589;
    static Node trees[COUNT];
    for (int t = 0; t < COUNT; t++) {
        int64_t reach = 2 + step(&seed) % 1000;
        for (int64_t i = 0; i < N; i++) {
            vals[i] = step(&seed) % 10001;
            nkids[i] = 0;
            if (i > 0) {
                int64_t m = i < reach ? i : reach;
                parent[i] = i - (1 + step(&seed) % m);
                nkids[parent[i]]++;
            }
        }
        // Children in the order they were added, as the Kāra lists are.
        int64_t at = 0;
        for (int64_t i = 0; i < N; i++) {
            start[i] = at;
            at += nkids[i];
            nkids[i] = 0;
        }
        for (int64_t i = 1; i < N; i++) order[start[parent[i]] + nkids[parent[i]]++] = i;
        build_random(0, &trees[t]);
    }
    int64_t total = 0, checksum = 0;
    for (int round = 0; round < ROUNDS; round++)
        for (int g = 0; g < COUNT; g++) {
            List got = preorder(&trees[(round * 7 + g) % COUNT]);
            total += got.len;
            for (int64_t i = 0; i < got.len; i++) checksum = (checksum * 31 + got.data[i]) % 1000000007;
            free(got.data);
        }
    printf("%d trees of %d nodes, %d rounds: %lld values listed, checksum %lld\n", COUNT, N, ROUNDS,
           (long long)total, (long long)checksum);
    return 0;
}
