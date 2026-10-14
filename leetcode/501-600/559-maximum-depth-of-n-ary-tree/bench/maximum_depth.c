// Benchmark for #559: C mirror of the ★ arm (recursion); see
// maximum_depth.kara. A node holds its children in one malloc'd array
// of nodes, as a Kāra Vec[Node] holds them inline.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int64_t val;
    struct Node *children;
    int64_t len;
} Node;

static int64_t depth(const Node *node) {
    int64_t deepest = 0;
    for (int64_t i = 0; i < node->len; i++) {
        int64_t d = depth(&node->children[i]);
        if (d > deepest) deepest = d;
    }
    return deepest + 1;
}

static int64_t max_depth(const Node *root) { return root ? depth(root) : 0; }

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
    enum { COUNT = 100, ROUNDS = 50 };
    int64_t seed = 559;
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
            int64_t d = max_depth(&trees[(round * 7 + g) % COUNT]);
            total += d;
            checksum = (checksum * 31 + d) % 1000000007;
        }
    printf("%d trees of %d nodes, %d rounds: depths sum to %lld, checksum %lld\n", COUNT, N, ROUNDS,
           (long long)total, (long long)checksum);
    return 0;
}
