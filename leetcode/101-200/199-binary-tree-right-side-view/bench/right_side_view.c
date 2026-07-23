#include <stdio.h>
#include <stdlib.h>

typedef struct {
    long val;
    long left;
    long right;
} Node;

/* Returns the number of visible values and writes them into out[]. */
static long right_view(const Node *nodes, long root, long *out) {
    long count = 0;
    if (root == -1) {
        return 0;
    }
    long capacity = 16;
    long *level = malloc((size_t)capacity * sizeof(long));
    long level_len = 0;
    level[level_len++] = root;
    while (level_len > 0) {
        out[count++] = nodes[level[level_len - 1]].val;
        long *nxt = malloc((size_t)(level_len * 2 + 1) * sizeof(long));
        long nxt_len = 0;
        for (long j = 0; j < level_len; j++) {
            long idx = level[j];
            if (nodes[idx].left != -1) {
                nxt[nxt_len++] = nodes[idx].left;
            }
            if (nodes[idx].right != -1) {
                nxt[nxt_len++] = nodes[idx].right;
            }
        }
        free(level);
        level = nxt;
        level_len = nxt_len;
    }
    free(level);
    return count;
}

int main(void) {
    long n = 8191;
    long passes = 40000;

    Node *nodes = malloc((size_t)n * sizeof(Node));
    long state = 12345;
    for (long i = 0; i < n; i++) {
        state = (state * 1103515245 + 12345) & 2147483647;
        long v = (state >> 16) % 1000;
        long li = 2 * i + 1;
        long ri = 2 * i + 2;
        nodes[i].val = v;
        nodes[i].left = li < n ? li : -1;
        nodes[i].right = ri < n ? ri : -1;
    }

    long *out = malloc((size_t)n * sizeof(long));
    long sink = 0;
    for (long p = 0; p < passes; p++) {
        state = (state * 1103515245 + 12345) & 2147483647;
        long idx = state % n;
        nodes[idx].val = (state >> 16) % 1000;
        long vn = right_view(nodes, 0, out);
        for (long k = 0; k < vn; k++) {
            sink += out[k];
        }
    }
    printf("%ld\n", sink);
    free(out);
    free(nodes);
    return 0;
}
