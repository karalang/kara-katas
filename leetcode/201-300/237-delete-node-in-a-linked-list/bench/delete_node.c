/* Benchmark workload for LeetCode #237 — Delete Node in a Linked List (C mirror). */
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    long val;
    long next;
} Node;

int main(void) {
    long n = 8000, cycles = 7000;
    Node *nodes = malloc(n * sizeof(Node));
    long state = 12345;
    for (long i = 0; i < n; i++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        nodes[i].val = state % 50;
        nodes[i].next = -1;
    }

    long sink = 0;
    for (long c = 0; c < cycles; c++) {
        for (long r = 0; r < n; r++) {
            nodes[r].next = (r + 1 < n) ? r + 1 : -1;
        }
        while (nodes[0].next != -1) {
            long cur = 0;
            while (cur != -1 && nodes[cur].next != -1) {
                long s = nodes[cur].next;
                nodes[cur].val = nodes[s].val;
                nodes[cur].next = nodes[s].next;
                cur = nodes[cur].next;
            }
            long pass = 0;
            for (long k = 0; k != -1; k = nodes[k].next) {
                pass += nodes[k].val;
            }
            sink = (sink * 31 + pass) & 1073741823L;
        }
    }
    printf("%ld\n", sink);
    free(nodes);
    return 0;
}
