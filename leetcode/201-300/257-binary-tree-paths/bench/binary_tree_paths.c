// Benchmark workload for LeetCode #257 — Binary Tree Paths (C mirror).
// Mirrors binary_tree_paths.kara algorithm-for-algorithm.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct { long val, left, right; } Node;

static Node *nodes; static long ncount;
static char **out; static long ocount, ocap;

static void opush(char *s) {
    if (ocount == ocap) { ocap = ocap ? ocap * 2 : 1024; out = realloc(out, ocap * sizeof(char *)); }
    out[ocount++] = s;
}

static void walk(long node, const char *prefix, long plen) {
    long left = nodes[node].left, right = nodes[node].right;
    if (left == -1 && right == -1) {
        char *d = malloc(plen + 1);
        memcpy(d, prefix, plen + 1);
        opush(d);
        return;
    }
    if (left != -1) {
        char buf[32];
        int m = snprintf(buf, sizeof buf, "->%ld", nodes[left].val);
        char *next = malloc(plen + m + 1);
        memcpy(next, prefix, plen);
        memcpy(next + plen, buf, m + 1);
        walk(left, next, plen + m);
        free(next);
    }
    if (right != -1) {
        char buf[32];
        int m = snprintf(buf, sizeof buf, "->%ld", nodes[right].val);
        char *next = malloc(plen + m + 1);
        memcpy(next, prefix, plen);
        memcpy(next + plen, buf, m + 1);
        walk(right, next, plen + m);
        free(next);
    }
}

int main(void) {
    long n = 150000, rounds = 5;
    nodes = malloc(n * sizeof(Node));
    long *open = malloc(n * sizeof(long)); long ocnt = 0;
    long state = 257257;

    state = (state * 1103515245L + 12345L) & 2147483647L;
    nodes[0].val = (state / 65536L) % 100L - 50L; nodes[0].left = -1; nodes[0].right = -1;
    ncount = 1; open[ocnt++] = 0;

    while (ncount < n) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long wd0 = state / 65536L;
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long pick = (wd0 * 32768L + state / 65536L) % ocnt;
        long parent = open[pick];
        state = (state * 1103515245L + 12345L) & 2147483647L;
        nodes[ncount].val = (state / 65536L) % 100L - 50L;
        nodes[ncount].left = -1; nodes[ncount].right = -1;
        long child = ncount++;
        if (nodes[parent].left == -1) nodes[parent].left = child;
        else { nodes[parent].right = child; open[pick] = open[ocnt - 1]; ocnt--; }
        open[ocnt++] = child;
    }

    long sink = 0;
    for (long r = 0; r < rounds; r++) {
        ocount = 0;
        char root[32];
        int rl = snprintf(root, sizeof root, "%ld", nodes[0].val);
        walk(0, root, rl);

        long h = 1;
        for (long i = 0; i < ocount; i++) {
            for (const unsigned char *p = (const unsigned char *)out[i]; *p; p++)
                h = (h * 1000003L + (long)*p) % 1000000007L;
            h = (h * 31L + 7L) % 1000000007L;
            free(out[i]);
        }
        sink = (sink * 131L + h) % 1000000007L;
    }
    printf("%ld\n", sink);
    free(nodes); free(open); free(out);
    return 0;
}
