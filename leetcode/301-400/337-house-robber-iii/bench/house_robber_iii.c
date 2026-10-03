// Benchmark workload for LeetCode #337 — C mirror of house_robber_iii.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define HOUSES 500000
#define PUNCHES 100
#define MODULUS 1073741789LL

typedef struct {
    int64_t val;
    int64_t left;
    int64_t right;
} Node;

typedef struct {
    int64_t robbed;
    int64_t skipped;
} Totals;

static int64_t max64(int64_t a, int64_t b) { return a > b ? a : b; }

static Totals visit(const Node *nodes, int64_t node) {
    if (node == -1) {
        Totals z = {0, 0};
        return z;
    }
    Totals l = visit(nodes, nodes[node].left);
    Totals r = visit(nodes, nodes[node].right);
    Totals t;
    t.robbed = nodes[node].val + l.skipped + r.skipped;
    t.skipped = max64(l.robbed, l.skipped) + max64(r.robbed, r.skipped);
    return t;
}

static int64_t rob(const Node *nodes, int64_t n) {
    if (n == 0) return 0;
    Totals t = visit(nodes, 0);
    return max64(t.robbed, t.skipped);
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
    int64_t seed = 337;
    Node *nodes = malloc(sizeof(Node) * HOUSES);
    for (int64_t i = 0; i < HOUSES; i++) {
        nodes[i].val = next(&seed) % 10001;
        nodes[i].left = -1;
        nodes[i].right = -1;
        if (i == 0) continue;
        int64_t cur = 0;
        for (;;) {
            if (next(&seed) % 2 == 0) {
                if (nodes[cur].left == -1) {
                    nodes[cur].left = i;
                    break;
                }
                cur = nodes[cur].left;
            } else {
                if (nodes[cur].right == -1) {
                    nodes[cur].right = i;
                    break;
                }
                cur = nodes[cur].right;
            }
        }
    }
    int64_t sink = 0;
    for (int64_t p = 0; p < PUNCHES; p++) {
        int64_t at = wide(&seed) % HOUSES;
        int64_t old = nodes[at].val;
        nodes[at].val = next(&seed) % 10001;
        int64_t answer = rob(nodes, HOUSES);
        nodes[at].val = old;
        sink = (sink * 1000003 + answer) % MODULUS;
    }
    printf("%lld\n", (long long)sink);
    free(nodes);
    return 0;
}
