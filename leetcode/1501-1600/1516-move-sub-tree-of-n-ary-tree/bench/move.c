// LeetCode #1516 bench: the ★ arm (parent walks and a splice), as
// move.kara: each node owns a growable array of child pointers.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int64_t val;
    struct Node **children;
    int64_t len, cap;
} Node;

static void push(Node *node, Node *child) {
    if (node->len == node->cap) {
        node->cap = node->cap ? node->cap * 2 : 4;
        node->children = realloc(node->children, (size_t)node->cap * sizeof(Node *));
    }
    node->children[node->len++] = child;
}

static void remove_val(Node *node, int64_t val) {
    int64_t k = 0;
    for (int64_t i = 0; i < node->len; i++)
        if (node->children[i]->val != val) node->children[k++] = node->children[i];
    node->len = k;
}

static Node *parent_of(Node *node, int64_t val) {
    for (int64_t i = 0; i < node->len; i++) {
        Node *child = node->children[i];
        if (child->val == val) return node;
        Node *found = parent_of(child, val);
        if (found) return found;
    }
    return NULL;
}

static int contains(Node *node, int64_t val) {
    if (node->val == val) return 1;
    for (int64_t i = 0; i < node->len; i++)
        if (contains(node->children[i], val)) return 1;
    return 0;
}

static Node *move_sub_tree(Node *root, Node *p, Node *q) {
    for (int64_t i = 0; i < q->len; i++)
        if (q->children[i]->val == p->val) return root;
    Node *p_parent = parent_of(root, p->val);
    if (contains(p, q->val)) {
        Node *q_parent = parent_of(root, q->val);
        remove_val(q_parent, q->val);
        push(q, p);
        if (!p_parent) return q;
        for (int64_t i = 0; i < p_parent->len; i++)
            if (p_parent->children[i]->val == p->val) {
                p_parent->children[i] = q;
                break;
            }
    } else {
        remove_val(p_parent, p->val);
        push(q, p);
    }
    return root;
}

static int64_t seed = 1516;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

static void fold(Node *node, int64_t *check) {
    *check = mix(*check, node->val);
    for (int64_t i = 0; i < node->len; i++) fold(node->children[i], check);
}

int main(void) {
    const int64_t n = 100000;
    Node *nodes = calloc((size_t)n, sizeof(Node));
    for (int64_t v = 0; v < n; v++) nodes[v].val = v;
    for (int64_t i = 1; i < n; i++) {
        int64_t a = next_random();
        int64_t parent = (a * 32768 + next_random()) % i;
        push(&nodes[parent], &nodes[i]);
    }
    Node *root = &nodes[0];
    int64_t check = 0;
    for (int r = 0; r < 1000; r++) {
        int64_t a = next_random();
        int64_t p = (a * 32768 + next_random()) % n;
        int64_t b = next_random();
        int64_t q = (p + 1 + (b * 32768 + next_random()) % (n - 1)) % n;
        root = move_sub_tree(root, &nodes[p], &nodes[q]);
        check = mix(check, root->val);
    }
    fold(root, &check);
    printf("1000 moves in a tree of 100000 nodes: checksum %lld\n", (long long)check);
    return 0;
}
