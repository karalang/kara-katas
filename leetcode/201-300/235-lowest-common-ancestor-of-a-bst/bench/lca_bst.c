/* Benchmark harness for LeetCode #235 — Lowest Common Ancestor of a BST.
 * Mirrors lca_bst.kara algorithm-for-algorithm, including the index-pool tree
 * (struct array with i64 child indices, -1 = null) rather than malloc'd
 * pointer-linked nodes, so pointer-chasing behaviour matches the other lanes.
 */

#include <stdio.h>
#include <stdlib.h>

#define N 200000
#define ITERS 8000000

typedef struct {
    long long val;
    long long left;
    long long right;
} Node;

static long long vals[N];
static Node nodes[N];

static long long lca(const Node *ns, long long root, long long p, long long q) {
    long long cur = root;
    while (cur != -1) {
        long long v = ns[cur].val;
        if (p < v && q < v) {
            cur = ns[cur].left;
        } else if (p > v && q > v) {
            cur = ns[cur].right;
        } else {
            return v;
        }
    }
    return -1;
}

int main(void) {
    long long x = 7;
    for (long long i = 0; i < N; i++) {
        x = (x * 1103515245 + 12345) % 2147483648LL;
        long long hi = x / 65536;
        x = (x * 1103515245 + 12345) % 2147483648LL;
        vals[i] = (hi * 32768 + x / 65536) % 1000000;
    }

    long long nn = 0;
    long long root = -1;
    for (long long b = 0; b < N; b++) {
        long long v = vals[b];
        if (root == -1) {
            nodes[nn].val = v;
            nodes[nn].left = -1;
            nodes[nn].right = -1;
            root = nn;
            nn++;
        } else {
            long long cur = root;
            for (;;) {
                if (v < nodes[cur].val) {
                    long long l = nodes[cur].left;
                    if (l == -1) {
                        nodes[nn].val = v;
                        nodes[nn].left = -1;
                        nodes[nn].right = -1;
                        nodes[cur].left = nn;
                        nn++;
                        break;
                    }
                    cur = l;
                } else {
                    long long r = nodes[cur].right;
                    if (r == -1) {
                        nodes[nn].val = v;
                        nodes[nn].left = -1;
                        nodes[nn].right = -1;
                        nodes[cur].right = nn;
                        nn++;
                        break;
                    }
                    cur = r;
                }
            }
        }
    }

    long long sink = 0;
    long long y = 99;
    for (long long it = 0; it < ITERS; it++) {
        y = (y * 1103515245 + 12345) % 2147483648LL;
        long long phi = y / 65536;
        y = (y * 1103515245 + 12345) % 2147483648LL;
        long long pi = (phi * 32768 + y / 65536) % N;
        y = (y * 1103515245 + 12345) % 2147483648LL;
        long long qhi = y / 65536;
        y = (y * 1103515245 + 12345) % 2147483648LL;
        long long qi = (qhi * 32768 + y / 65536) % N;
        long long a = lca(nodes, root, vals[pi], vals[qi]);
        sink = (sink + a) % 1000000007LL;
    }
    printf("%lld\n", sink);
    return 0;
}
