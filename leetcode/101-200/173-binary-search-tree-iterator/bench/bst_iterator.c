#include <stdio.h>
#include <stdlib.h>

typedef struct {
    long val;
    long left;
    long right;
} Node;

static Node *nodes;
static long node_count;

static long insert(long root, long val) {
    if (root == -1) {
        nodes[node_count].val = val;
        nodes[node_count].left = -1;
        nodes[node_count].right = -1;
        return node_count++;
    }
    if (val < nodes[root].val) {
        long li = nodes[root].left;
        nodes[root].left = insert(li, val);
    } else {
        long ri = nodes[root].right;
        nodes[root].right = insert(ri, val);
    }
    return root;
}

int main(void) {
    long n = 4000, passes = 30000;
    nodes = malloc(n * sizeof(Node));
    node_count = 0;
    long root = -1;
    long state = 12345;
    for (long i = 0; i < n; i++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long v = state % 1000;
        root = insert(root, v);
    }

    long *stack = malloc(n * sizeof(long));
    long sink = 0;
    for (long p = 0; p < passes; p++) {
        long idx = (p * 1315423911L + 7L) % n;
        nodes[idx].val = (nodes[idx].val + 1) % 1000;

        long sp = 0;
        long cur = root;
        while (cur != -1) {
            stack[sp++] = cur;
            cur = nodes[cur].left;
        }
        long pos = 1;
        while (sp > 0) {
            long top = stack[--sp];
            sink += pos * nodes[top].val;
            pos++;
            long r = nodes[top].right;
            while (r != -1) {
                stack[sp++] = r;
                r = nodes[r].left;
            }
        }
    }
    printf("%ld\n", sink);
    free(stack); free(nodes);
    return 0;
}
