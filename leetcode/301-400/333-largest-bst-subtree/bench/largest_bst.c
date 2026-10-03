// Benchmark workload for LeetCode #333 — C mirror of largest_bst.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define NODES 100000
#define PUNCHES 200
#define MODULUS 1073741789LL

typedef struct {
    int64_t val;
    int64_t left;
    int64_t right;
} Node;

typedef struct {
    int bst;
    int64_t size;
    int64_t lo;
    int64_t hi;
} Info;

static Info visit(const Node *nodes, int64_t node, int64_t *best) {
    int64_t val = nodes[node].val;
    int64_t left = nodes[node].left;
    int64_t right = nodes[node].right;
    int bst = 1;
    int64_t size = 1, lo = val, hi = val;
    if (left != -1) {
        Info l = visit(nodes, left, best);
        if (l.bst && l.hi < val) {
            size += l.size;
            lo = l.lo;
        } else {
            bst = 0;
        }
    }
    if (right != -1) {
        Info r = visit(nodes, right, best);
        if (r.bst && r.lo > val) {
            size += r.size;
            hi = r.hi;
        } else {
            bst = 0;
        }
    }
    if (bst && size > *best) *best = size;
    Info out = {bst, size, lo, hi};
    return out;
}

static int64_t largest_bst_subtree(const Node *nodes, int64_t n) {
    if (n == 0) return 0;
    int64_t best = 0;
    (void)visit(nodes, 0, &best);
    return best;
}

static int64_t next(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t wide(int64_t *seed) {
    int64_t hi = next(seed);
    return hi * 32768 + next(seed);
}

int main(void) {
    int64_t seed = 333;
    int64_t *vals = malloc(sizeof(int64_t) * NODES);
    for (int64_t i = 0; i < NODES; i++) vals[i] = i * 2;
    for (int64_t i = 0; i < NODES; i++) {
        int64_t j = i + wide(&seed) % (NODES - i);
        int64_t t = vals[i];
        vals[i] = vals[j];
        vals[j] = t;
    }
    Node *nodes = malloc(sizeof(Node) * NODES);
    int64_t n = 0;
    for (int64_t k = 0; k < NODES; k++) {
        int64_t v = vals[k];
        nodes[n].val = v;
        nodes[n].left = -1;
        nodes[n].right = -1;
        int64_t id = n++;
        int64_t cur = 0;
        while (cur != id) {
            if (v < nodes[cur].val) {
                if (nodes[cur].left == -1) nodes[cur].left = id;
                cur = nodes[cur].left;
            } else {
                if (nodes[cur].right == -1) nodes[cur].right = id;
                cur = nodes[cur].right;
            }
        }
    }
    int64_t sink = 0;
    for (int p = 0; p < PUNCHES; p++) {
        int64_t at = wide(&seed) % NODES;
        int64_t old = nodes[at].val;
        nodes[at].val = wide(&seed) % (2 * NODES);
        int64_t answer = largest_bst_subtree(nodes, n);
        nodes[at].val = old;
        sink = (sink * 1000003 + answer) % MODULUS;
    }
    printf("%lld\n", (long long)sink);
    free(nodes);
    free(vals);
    return 0;
}
