// LeetCode #1721: Swapping Nodes in a Linked List -- the bench
// (swap.kara): the kth node found, then a runner from it to the last node
// drags a second cursor from the head to the kth node from the end.

#include <stdio.h>
#include <stdlib.h>

typedef struct node {
    long val;
    struct node *next;
} node;

static node *swap_nodes(node *head, long k) {
    node *first = head;
    for (long i = 1; i < k; i++) {
        first = first->next;
    }
    node *second = head;
    node *runner = first;
    while (runner->next != NULL) {
        runner = runner->next;
        second = second->next;
    }
    long value = first->val;
    first->val = second->val;
    second->val = value;
    return head;
}

static long next_random(long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648L;
    return *seed / 65536;
}

static long wide(long *seed) {
    long hi = next_random(seed);
    return hi * 32768 + next_random(seed);
}

int main(void) {
    int count = 10;
    long rounds = 100;
    long n = 100000;
    long seed = 1721;
    node *lists[10];
    node *pools[10];
    long *values = malloc(sizeof(long) * n);
    for (int c = 0; c < count; c++) {
        for (long i = 0; i < n; i++) {
            values[i] = next_random(&seed) % 101;
        }
        pools[c] = malloc(sizeof(node) * n);
        for (long i = 0; i < n; i++) {
            pools[c][i].val = values[i];
            pools[c][i].next = i + 1 < n ? &pools[c][i + 1] : NULL;
        }
        lists[c] = &pools[c][0];
    }
    free(values);
    long *ks = malloc(sizeof(long) * count * rounds);
    for (long i = 0; i < count * rounds; i++) {
        ks[i] = wide(&seed) % n + 1;
    }
    long sum = 0, check = 0;
    for (long r = 0; r < rounds; r++) {
        for (int c = 0; c < count; c++) {
            node *head = swap_nodes(lists[c], ks[r * count + c]);
            sum += head->val;
            check = (check * 31 + head->val + r) % 1000000007;
        }
    }
    printf("%d lists of %ld nodes, %ld rounds: heads sum to %ld, checksum %ld\n", count, n, rounds, sum, check);
    for (int c = 0; c < count; c++) {
        free(pools[c]);
    }
    free(ks);
    return 0;
}
