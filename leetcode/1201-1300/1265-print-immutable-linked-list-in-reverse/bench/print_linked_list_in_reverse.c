// LeetCode #1265 bench, in C: the ★ arm (by recursion: a node prints after
// everything after it has, every call through the node's table of function
// pointers, as a trait object's) on 100 random lists of 1000 nodes built
// once, 300 rounds; everything each round prints folded into a checksum.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct Node Node;

// The interface: a node prints its value, and hands out the node after it.
typedef struct {
    void (*print_value)(const Node *);
    const Node *(*get_next)(const Node *);
} ImmutableListNode;

typedef struct {
    int64_t *values;
    size_t len, cap;
} Printed;

struct Node {
    const ImmutableListNode *vt;
    int64_t val;
    const Node *next;
    Printed *printed;
};

static void node_print_value(const Node *n) {
    Printed *p = n->printed;
    if (p->len == p->cap) {
        p->cap = p->cap ? 2 * p->cap : 16;
        p->values = realloc(p->values, p->cap * sizeof(int64_t));
    }
    p->values[p->len++] = n->val;
}

static const Node *node_get_next(const Node *n) { return n->next; }

static const ImmutableListNode NODE_VT = {node_print_value, node_get_next};

static void print_linked_list_in_reverse(const Node *head) {
    const Node *next = head->vt->get_next(head);
    if (next) print_linked_list_in_reverse(next);
    head->vt->print_value(head);
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    Printed printed = {NULL, 0, 0};
    int64_t seed = 1265;
    Node *heads[100];
    for (int h = 0; h < 100; h++) {
        Node *head = NULL;
        for (int i = 0; i < 1000; i++) {
            Node *n = malloc(sizeof(Node));
            *n = (Node){&NODE_VT, next_random(&seed) % 2001 - 1000, head, &printed};
            head = n;
        }
        heads[h] = head;
    }
    int64_t check = 0;
    for (int64_t round = 0; round < 300; round++)
        for (int h = 0; h < 100; h++) {
            printed.len = 0;
            print_linked_list_in_reverse(heads[h]);
            check = (check + round) % 1000000007;
            for (size_t i = 0; i < printed.len; i++) check = (check * 131 + printed.values[i] + 1000) % 1000000007;
        }
    printf("300 rounds of 100 lists of 1000 nodes: checksum %lld\n", (long long)check);
    return 0;
}
