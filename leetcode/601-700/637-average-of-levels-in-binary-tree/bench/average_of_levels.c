// Benchmark mirror for #637: the same workload and algorithm as
// average_of_levels.kara (breadth first, one level at a time). The queue
// is a ring buffer of node pointers that grows by doubling.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int64_t val;
    struct Node *left, *right;
} Node;

typedef struct {
    Node **items;
    int64_t head, len, cap;
} Queue;

static void push(Queue *q, Node *n) {
    if (q->len == q->cap) {
        int64_t cap = q->cap ? q->cap * 2 : 16;
        Node **items = malloc(cap * sizeof(Node *));
        for (int64_t i = 0; i < q->len; i++) items[i] = q->items[(q->head + i) % q->cap];
        free(q->items);
        q->items = items;
        q->head = 0;
        q->cap = cap;
    }
    q->items[(q->head + q->len) % q->cap] = n;
    q->len++;
}

static Node *pop(Queue *q) {
    Node *n = q->items[q->head];
    q->head = (q->head + 1) % q->cap;
    q->len--;
    return n;
}

// Writes the averages to `out` and returns how many.
static int64_t average_of_levels(Node *root, double *out) {
    Queue q = {0};
    int64_t levels = 0;
    if (root) push(&q, root);
    while (q.len > 0) {
        int64_t count = q.len, sum = 0;
        for (int64_t i = 0; i < count; i++) {
            Node *n = pop(&q);
            sum += n->val;
            if (n->left) push(&q, n->left);
            if (n->right) push(&q, n->right);
        }
        out[levels++] = (double)sum / (double)count;
    }
    free(q.items);
    return levels;
}

static int64_t seed = 637;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t random_value(void) {
    int64_t high = next_random() % 65536;
    int64_t low = next_random() % 65536;
    return high * 65536 + low - 2147483648LL;
}

static Node *random_tree(int64_t size) {
    Node *root = NULL;
    for (int64_t k = 0; k < size; k++) {
        Node *c = calloc(1, sizeof(Node));
        c->val = random_value();
        if (!root) {
            root = c;
            continue;
        }
        Node *node = root;
        for (;;) {
            if (next_random() % 2 == 0) {
                if (node->left) node = node->left;
                else { node->left = c; break; }
            } else {
                if (node->right) node = node->right;
                else { node->right = c; break; }
            }
        }
    }
    return root;
}

static void free_tree(Node *n) {
    if (!n) return;
    free_tree(n->left);
    free_tree(n->right);
    free(n);
}

int main(void) {
    Node *trees[10];
    for (int i = 0; i < 10; i++) trees[i] = random_tree(10000);
    double averages[10001];
    int64_t levels = 0;
    double total = 0.0;
    for (int r = 0; r < 4000; r++) {
        int64_t k = average_of_levels(trees[r % 10], averages);
        for (int64_t i = 0; i < k; i++) {
            levels++;
            total += averages[i];
        }
    }
    printf("10 trees of 10000 nodes, 4000 rounds: %lld levels, sum of averages %.3f\n", (long long)levels, total);
    for (int i = 0; i < 10; i++) free_tree(trees[i]);
    return 0;
}
