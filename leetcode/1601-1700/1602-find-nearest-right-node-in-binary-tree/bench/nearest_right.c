// LeetCode #1602: Find Nearest Right Node in Binary Tree -- the bench in
// C, mirroring nearest_right.kara: breadth first, a level at a time, over
// a ring buffer queue. Each node is its own malloc.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int32_t val;
    struct Node *left, *right;
} Node;

typedef struct {
    Node **buf;
    int64_t cap, head, len;
} Queue;

static void push_back(Queue *q, Node *n) {
    if (q->len == q->cap) {
        int64_t cap = q->cap ? q->cap * 2 : 8;
        Node **buf = malloc(cap * sizeof(Node *));
        for (int64_t i = 0; i < q->len; i++) buf[i] = q->buf[(q->head + i) % q->cap];
        free(q->buf);
        q->buf = buf;
        q->cap = cap;
        q->head = 0;
    }
    q->buf[(q->head + q->len) % q->cap] = n;
    q->len++;
}

static Node *pop_front(Queue *q) {
    Node *n = q->buf[q->head];
    q->head = (q->head + 1) % q->cap;
    q->len--;
    return n;
}

static Node *find_nearest_right_node(Node *root, Node *u) {
    Queue q = {0};
    Node *result = NULL;
    if (root) push_back(&q, root);
    while (q.len > 0) {
        int64_t width = q.len;
        for (int64_t i = 0; i < width; i++) {
            Node *node = pop_front(&q);
            if (node == u) {
                result = i + 1 < width ? pop_front(&q) : NULL;
                free(q.buf);
                return result;
            }
            if (node->left) push_back(&q, node->left);
            if (node->right) push_back(&q, node->right);
        }
    }
    free(q.buf);
    return NULL;
}

static int64_t seed = 1602;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t big(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

static Node *leaf(int32_t v) {
    Node *n = malloc(sizeof(Node));
    n->val = v;
    n->left = n->right = NULL;
    return n;
}

typedef struct {
    Node *parent;
    int left;
} Slot;

static Node **random_tree(int64_t n) {
    int32_t *values = malloc(n * sizeof(int32_t));
    for (int64_t i = 0; i < n; i++) values[i] = (int32_t)(i + 1);
    for (int64_t i = n - 1; i >= 1; i--) {
        int64_t j = big() % (i + 1);
        int32_t t = values[i];
        values[i] = values[j];
        values[j] = t;
    }
    Node **nodes = malloc(n * sizeof(Node *));
    Slot *free_slots = malloc((2 * n + 2) * sizeof(Slot));
    int64_t nfree = 0;
    nodes[0] = leaf(values[0]);
    free_slots[nfree++] = (Slot){nodes[0], 1};
    free_slots[nfree++] = (Slot){nodes[0], 0};
    for (int64_t i = 1; i < n; i++) {
        int64_t k = big() % nfree;
        Slot s = free_slots[k];
        free_slots[k] = free_slots[--nfree];
        Node *child = leaf(values[i]);
        if (s.left) s.parent->left = child;
        else s.parent->right = child;
        free_slots[nfree++] = (Slot){child, 1};
        free_slots[nfree++] = (Slot){child, 0};
        nodes[i] = child;
    }
    free(values);
    free(free_slots);
    return nodes;
}

int main(void) {
    Node **trees[10];
    int64_t picks[10][100];
    for (int t = 0; t < 10; t++) {
        trees[t] = random_tree(100000);
        for (int k = 0; k < 100; k++) picks[t][k] = big() % 100000;
    }
    int64_t check = 0, found = 0;
    for (int t = 0; t < 10; t++) {
        for (int k = 0; k < 100; k++) {
            Node *a = find_nearest_right_node(trees[t][0], trees[t][picks[t][k]]);
            int64_t v = a ? a->val : 0;
            if (v > 0) found++;
            check = mix(check, v);
        }
    }
    printf("10 trees of 100000 nodes: 1000 queries, %lld found, checksum %lld\n", (long long)found, (long long)check);
    for (int t = 0; t < 10; t++) {
        for (int64_t i = 0; i < 100000; i++) free(trees[t][i]);
        free(trees[t]);
    }
    return 0;
}
