// Benchmark for #513: C mirror of the ★ arm (level by level); see
// find_bottom_left_value.kara. The queue is a fresh ring buffer for
// every call, grown by doubling, as the ★ arm's `VecDeque.new()`.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int64_t val;
    struct TreeNode *left, *right;
} TreeNode;

typedef struct {
    TreeNode **buf;
    int64_t head, len, cap;
} Queue;

static void push_back(Queue *q, TreeNode *n) {
    if (q->len == q->cap) {
        int64_t cap = q->cap ? q->cap * 2 : 4;
        TreeNode **buf = malloc(cap * sizeof(TreeNode *));
        for (int64_t i = 0; i < q->len; i++) buf[i] = q->buf[(q->head + i) % q->cap];
        free(q->buf);
        q->buf = buf;
        q->head = 0;
        q->cap = cap;
    }
    q->buf[(q->head + q->len) % q->cap] = n;
    q->len++;
}

static TreeNode *pop_front(Queue *q) {
    TreeNode *n = q->buf[q->head];
    q->head = (q->head + 1) % q->cap;
    q->len--;
    return n;
}

static int64_t find_bottom_left_value(TreeNode *root) {
    Queue q = {NULL, 0, 0, 0};
    push_back(&q, root);
    int64_t leftmost = root->val;
    while (q.len > 0) {
        leftmost = q.buf[q.head]->val;
        int64_t width = q.len;
        for (int64_t i = 0; i < width; i++) {
            TreeNode *node = pop_front(&q);
            if (node->left) push_back(&q, node->left);
            if (node->right) push_back(&q, node->right);
        }
    }
    free(q.buf);
    return leftmost;
}

// ---- benchmark --------------------------------------------------------------

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static TreeNode *build(const int64_t *values, int64_t lo, int64_t hi, int64_t *seed) {
    if (lo >= hi) return NULL;
    int64_t mid = lo + next_random(seed) % (hi - lo);
    TreeNode *left = build(values, lo, mid, seed);
    TreeNode *right = build(values, mid + 1, hi, seed);
    TreeNode *n = malloc(sizeof(TreeNode));
    n->val = values[mid];
    n->left = left;
    n->right = right;
    return n;
}

int main(void) {
    // 100 random trees of 10,000 nodes, the values from the whole range
    // -2^31 to 2^31 - 1, built once. Then each is solved 50 times.
    int64_t trees = 100;
    int64_t seed = 513;
    TreeNode **all = malloc(trees * sizeof(TreeNode *));
    int64_t *values = malloc(10000 * sizeof(int64_t));
    for (int64_t t = 0; t < trees; t++) {
        for (int64_t k = 0; k < 10000; k++) {
            int64_t a = next_random(&seed);
            int64_t b = next_random(&seed);
            int64_t c = next_random(&seed);
            values[k] = a * 65536 + b * 2 + c % 2 - 2147483648;
        }
        all[t] = build(values, 0, 10000, &seed);
    }
    int64_t checksum = 0;
    for (int r = 0; r < 50; r++) {
        for (int64_t t = 0; t < trees; t++) {
            checksum = (checksum * 31 + find_bottom_left_value(all[t]) + 2147483648) % 1000000007;
        }
    }
    printf("%lld trees of 10000 nodes, 50 times each: checksum %lld\n", (long long)trees, (long long)checksum);
    return 0;
}
