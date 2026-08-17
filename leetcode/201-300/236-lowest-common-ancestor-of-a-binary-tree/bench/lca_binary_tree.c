/* Benchmark harness for LeetCode #236 — LCA of a Binary Tree.
 * Mirrors lca_binary_tree.kara algorithm-for-algorithm, including the
 * index-pool tree and the recursive post-order search.
 */

#include <stdio.h>

#define N 100000
#define ITERS 600

typedef struct {
    long long val;
    long long left;
    long long right;
} Node;

static Node nodes[N];

static long long lca(const Node *ns, long long cur, long long p, long long q) {
    if (cur == -1) {
        return -1;
    }
    if (ns[cur].val == p || ns[cur].val == q) {
        return cur;
    }
    long long l = lca(ns, ns[cur].left, p, q);
    long long r = lca(ns, ns[cur].right, p, q);
    if (l != -1 && r != -1) {
        return cur;
    }
    if (l != -1) {
        return l;
    }
    return r;
}

int main(void) {
    for (long long i = 0; i < N; i++) {
        long long lc = 2 * i + 1;
        long long rc = 2 * i + 2;
        nodes[i].val = i;
        nodes[i].left = lc < N ? lc : -1;
        nodes[i].right = rc < N ? rc : -1;
    }

    long long sink = 0;
    long long y = 2024;
    for (long long it = 0; it < ITERS; it++) {
        y = (y * 1103515245 + 12345) % 2147483648LL;
        long long wd1 = y / 65536;
        y = (y * 1103515245 + 12345) % 2147483648LL;
        long long p = (wd1 * 32768 + y / 65536) % N;
        y = (y * 1103515245 + 12345) % 2147483648LL;
        long long wd0 = y / 65536;
        y = (y * 1103515245 + 12345) % 2147483648LL;
        long long q = (wd0 * 32768 + y / 65536) % N;
        long long ans = lca(nodes, 0, p, q);
        long long v = ans == -1 ? -1 : nodes[ans].val;
        sink = (sink + v) % 1000000007LL;
    }
    printf("%lld\n", sink);
    return 0;
}
