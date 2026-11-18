// LeetCode #1609: Even Odd Tree -- the bench in C, mirroring
// even_odd.kara: breadth first, a level at a time, over a ring buffer
// queue. Each node is its own malloc.
#include <stdbool.h>
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

static bool is_even_odd_tree(Node *root) {
    Queue q = {0};
    if (root) push_back(&q, root);
    bool even = true;
    while (q.len > 0) {
        bool has_prev = false;
        int32_t prev = 0;
        int64_t width = q.len;
        for (int64_t i = 0; i < width; i++) {
            Node *node = pop_front(&q);
            int32_t v = node->val;
            bool ok = even ? v % 2 == 1 && (!has_prev || v > prev)
                           : v % 2 == 0 && (!has_prev || v < prev);
            if (!ok) {
                free(q.buf);
                return false;
            }
            has_prev = true;
            prev = v;
            if (node->left) push_back(&q, node->left);
            if (node->right) push_back(&q, node->right);
        }
        even = !even;
    }
    free(q.buf);
    return true;
}

static int64_t seed = 1609;

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
    Node **nodes = malloc(n * sizeof(Node *));
    Slot *free_slots = malloc((2 * n + 2) * sizeof(Slot));
    int64_t nfree = 0;
    nodes[0] = leaf(0);
    free_slots[nfree++] = (Slot){nodes[0], 1};
    free_slots[nfree++] = (Slot){nodes[0], 0};
    for (int64_t i = 1; i < n; i++) {
        int64_t k = big() % nfree;
        Slot s = free_slots[k];
        free_slots[k] = free_slots[--nfree];
        Node *child = leaf(0);
        if (s.left) s.parent->left = child;
        else s.parent->right = child;
        free_slots[nfree++] = (Slot){child, 1};
        free_slots[nfree++] = (Slot){child, 0};
        nodes[i] = child;
    }
    free(free_slots);
    // values level by level: even levels odd and rising, odd levels even
    // and falling
    Node **level = malloc(n * sizeof(Node *)), **below = malloc(n * sizeof(Node *));
    int64_t nlevel = 1, depth = 0;
    level[0] = nodes[0];
    while (nlevel > 0) {
        int32_t v = depth % 2 == 0 ? 1 + 2 * (int32_t)(next_random() % 5)
                                   : 1000000 - 2 * (int32_t)(next_random() % 5);
        int64_t nbelow = 0;
        for (int64_t i = 0; i < nlevel; i++) {
            Node *node = level[i];
            node->val = v;
            int32_t step = 2 * (int32_t)(next_random() % 2 + 1);
            v = depth % 2 == 0 ? v + step : v - step;
            if (node->left) below[nbelow++] = node->left;
            if (node->right) below[nbelow++] = node->right;
        }
        Node **t = level;
        level = below;
        below = t;
        nlevel = nbelow;
        depth++;
    }
    free(level);
    free(below);
    return nodes;
}

static void swap_values(Node *a, Node *b) {
    int32_t t = a->val;
    a->val = b->val;
    b->val = t;
}

int main(void) {
    Node **trees[20];
    int64_t picks[20][21][2];
    for (int t = 0; t < 20; t++) {
        trees[t] = random_tree(100000);
        picks[t][0][0] = picks[t][0][1] = 0;
        for (int k = 1; k <= 20; k++) {
            picks[t][k][0] = big() % 100000;
            picks[t][k][1] = big() % 100000;
        }
    }
    int64_t check = 0, checks = 0, even_odd = 0;
    for (int t = 0; t < 20; t++) {
        for (int k = 0; k <= 20; k++) {
            Node *a = trees[t][picks[t][k][0]], *b = trees[t][picks[t][k][1]];
            swap_values(a, b);
            bool yes = is_even_odd_tree(trees[t][0]);
            swap_values(a, b);
            if (yes) even_odd++;
            check = mix(check, yes ? 1 : 0);
            checks++;
        }
    }
    printf("20 trees of 100000 nodes: %lld checks, %lld even-odd, checksum %lld\n", (long long)checks,
           (long long)even_odd, (long long)check);
    for (int t = 0; t < 20; t++) {
        for (int64_t i = 0; i < 100000; i++) free(trees[t][i]);
        free(trees[t]);
    }
    return 0;
}
