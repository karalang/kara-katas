#include <stdio.h>
#include <stdlib.h>

typedef struct {
    long val;
    long next;
} Node;

static long reverse(Node *nodes, long head) {
    long prev = -1;
    long cur = head;
    while (cur != -1) {
        long nxt = nodes[cur].next;
        nodes[cur].next = prev;
        prev = cur;
        cur = nxt;
    }
    return prev;
}

static int is_palindrome(Node *nodes, long head) {
    if (head == -1) return 1;

    long slow = head;
    long fast = head;
    while (nodes[fast].next != -1 && nodes[nodes[fast].next].next != -1) {
        slow = nodes[slow].next;
        fast = nodes[nodes[fast].next].next;
    }

    long second = reverse(nodes, nodes[slow].next);
    long p1 = head;
    long p2 = second;
    while (p2 != -1) {
        if (nodes[p1].val != nodes[p2].val) {
            return 0;
        }
        p1 = nodes[p1].next;
        p2 = nodes[p2].next;
    }
    return 1;
}

int main(void) {
    long l = 50000;
    long passes = 1800;
    long half = (l + 1) / 2;

    long *fh = malloc(half * sizeof(long));
    long state = 12345;
    for (long i = 0; i < half; i++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        fh[i] = state % 1000;
    }

    Node *nodes = malloc(l * sizeof(Node));
    for (long j = 0; j < l; j++) {
        nodes[j].val = (j < half) ? fh[j] : fh[l - 1 - j];
        nodes[j].next = (j + 1 < l) ? j + 1 : -1;
    }

    long head = 0;
    long mid = l / 2 - 1;
    long base_mid = nodes[mid].val;

    long sink = 0;
    for (long p = 0; p < passes; p++) {
        for (long k = 0; k < l; k++) {
            nodes[k].next = (k + 1 < l) ? k + 1 : -1;
        }
        nodes[mid].val = base_mid + (p % 2);
        if (is_palindrome(nodes, head)) {
            sink += 1;
        }
    }
    printf("%ld\n", sink);
    free(fh);
    free(nodes);
    return 0;
}
