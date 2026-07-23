/* Benchmark workload for LeetCode #138 — Copy List with Random Pointer.
 *
 * Pointer-graph mirror of copy_random_list.kara: N heap Node structs (a linear
 * `next` chain plus one `random` edge each) are built once; the graph is
 * deep-copied K times, one `random` edge repointed before each copy (the punch)
 * so nothing hoists. Each copy mallocs N fresh nodes and frees them after the
 * checksum — matching Kāra's per-pass alloc + RC reclaim. `random` is a raw
 * (non-owning / weak-equivalent) pointer; ownership lives in the node array.
 * Sink = running total of a checksum over each copy's (val, next-id, random-id).
 */
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    long val, id;
    struct Node *next;
    struct Node *random; /* weak: non-owning */
} Node;

static Node **build(const long *vals, const long *rnd, long n) {
    Node **nodes = malloc(n * sizeof(Node *));
    for (long i = 0; i < n; i++) {
        Node *nd = malloc(sizeof(Node));
        nd->val = vals[i];
        nd->id = i;
        nd->next = NULL;
        nd->random = NULL;
        nodes[i] = nd;
    }
    for (long i = 0; i < n; i++) {
        if (i + 1 < n) nodes[i]->next = nodes[i + 1];
        if (rnd[i] >= 0) nodes[i]->random = nodes[rnd[i]];
    }
    return nodes;
}

static Node **deep_copy(Node **orig, long n) {
    Node **copies = malloc(n * sizeof(Node *));
    for (long i = 0; i < n; i++) {
        Node *nd = malloc(sizeof(Node));
        nd->val = orig[i]->val;
        nd->id = orig[i]->id;
        nd->next = NULL;
        nd->random = NULL;
        copies[i] = nd;
    }
    for (long i = 0; i < n; i++) {
        if (i + 1 < n) copies[i]->next = copies[i + 1];
        if (orig[i]->random) copies[i]->random = copies[orig[i]->random->id];
    }
    return copies;
}

static long checksum(Node **copies, long n) {
    long s = 0;
    for (long i = 0; i < n; i++) {
        long next_id = copies[i]->next ? copies[i]->next->id : -1;
        long rand_id = copies[i]->random ? copies[i]->random->id : -1;
        s += copies[i]->val + next_id * 7 + rand_id * 13;
    }
    return s;
}

static void free_nodes(Node **nodes, long n) {
    for (long i = 0; i < n; i++) free(nodes[i]);
    free(nodes);
}

int main(void) {
    long n = 3000, k = 4000;

    long *vals = malloc(n * sizeof(long));
    long *rnd = malloc(n * sizeof(long));
    long state = 12345;
    for (long i = 0; i < n; i++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        vals[i] = (state >> 16) % 1000;
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long r = state >> 16;
        rnd[i] = (r % 4 == 0) ? -1 : (r % n); /* ~25% null randoms */
    }

    Node **orig = build(vals, rnd, n);

    long sink = 0;
    for (long p = 0; p < k; p++) {
        long ii = p % n;
        long target = (p * 37 + 11) % n;
        orig[ii]->random = orig[target]; /* punch */
        Node **copies = deep_copy(orig, n);
        sink += checksum(copies, n);
        free_nodes(copies, n);
    }
    printf("%ld\n", sink);
    free_nodes(orig, n);
    free(vals);
    free(rnd);
    return 0;
}
