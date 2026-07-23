#include <stdio.h>
#include <stdlib.h>

typedef struct {
    long val;
    long left;
    long right;
} Node;

static Node *nodes;
static long node_count;

static long insert(long root, long v) {
    if (root == -1) {
        long idx = node_count;
        nodes[idx].val = v;
        nodes[idx].left = -1;
        nodes[idx].right = -1;
        node_count += 1;
        return idx;
    }
    if (v < nodes[root].val) {
        long l = insert(nodes[root].left, v);
        nodes[root].left = l;
    } else {
        long r = insert(nodes[root].right, v);
        nodes[root].right = r;
    }
    return root;
}

static long kth_smallest(long root, long k, long cap) {
    long *stack = malloc(cap * sizeof(long));
    long top = 0;
    long cur = root;
    long count = 0;
    long result = -1;
    while (cur != -1 || top > 0) {
        while (cur != -1) {
            stack[top++] = cur;
            cur = nodes[cur].left;
        }
        long node = stack[--top];
        count += 1;
        if (count == k) {
            result = nodes[node].val;
            break;
        }
        cur = nodes[node].right;
    }
    free(stack);
    return result;
}

int main(void) {
    long n = 3000;
    long queries = 140000;

    nodes = malloc(n * sizeof(Node));
    node_count = 0;

    long root = -1;
    long state = 12345;
    for (long i = 0; i < n; i++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        root = insert(root, state);
    }

    long sink = 0;
    for (long q = 0; q < queries; q++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long k = 1 + (state % n);
        sink += kth_smallest(root, k, n);
    }
    printf("%ld\n", sink);
    free(nodes);
    return 0;
}
