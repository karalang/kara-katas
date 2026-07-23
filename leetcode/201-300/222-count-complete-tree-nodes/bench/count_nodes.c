#include <stdio.h>
#include <stdlib.h>

typedef struct {
    long val;
    long left;
    long right;
} Node;

static Node *build(long n) {
    Node *nodes = malloc(n * sizeof(Node));
    for (long i = 0; i < n; i++) {
        long l = 2 * i + 1;
        long r = 2 * i + 2;
        nodes[i].val = i;
        nodes[i].left = l < n ? l : -1;
        nodes[i].right = r < n ? r : -1;
    }
    return nodes;
}

static long left_height(const Node *nodes, long idx) {
    long h = 0;
    long cur = idx;
    while (cur != -1) {
        h++;
        cur = nodes[cur].left;
    }
    return h;
}

static long right_height(const Node *nodes, long idx) {
    long h = 0;
    long cur = idx;
    while (cur != -1) {
        h++;
        cur = nodes[cur].right;
    }
    return h;
}

static long count_nodes(const Node *nodes, long idx) {
    if (idx == -1) return 0;
    long lh = left_height(nodes, idx);
    long rh = right_height(nodes, idx);
    if (lh == rh) {
        return (1L << lh) - 1;
    }
    return 1 + count_nodes(nodes, nodes[idx].left) + count_nodes(nodes, nodes[idx].right);
}

int main(void) {
    long n = 2000000;
    long passes = 2000000;
    long top_span = 2048;
    long modulus = 1000000007;

    Node *nodes = build(n);

    long sink = 0;
    for (long p = 0; p < passes; p++) {
        long start = p % top_span;
        sink = (sink + count_nodes(nodes, start)) % modulus;
    }
    printf("%ld\n", sink);
    free(nodes);
    return 0;
}
