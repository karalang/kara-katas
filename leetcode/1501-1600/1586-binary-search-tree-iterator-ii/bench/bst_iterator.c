// LeetCode #1586: Binary Search Tree Iterator II -- the bench in C,
// mirroring bst_iterator.kara: the lazy in-order stack and the list of
// values met. Each node is its own malloc; the stack, the list and the
// answers are growable arrays allocated per call.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int32_t val;
    struct Node *left, *right;
} Node;

typedef struct {
    Node **spine;
    int64_t spine_len, spine_cap;
    int32_t *seen;
    int64_t seen_len, seen_cap;
    int64_t at;
} Iter;

static void push_left(Iter *it, Node *node) {
    while (node) {
        if (it->spine_len == it->spine_cap) {
            it->spine_cap = it->spine_cap ? it->spine_cap * 2 : 4;
            it->spine = realloc(it->spine, it->spine_cap * sizeof(Node *));
        }
        it->spine[it->spine_len++] = node;
        node = node->left;
    }
}

static void iter_new(Iter *it, Node *root) {
    it->spine = NULL;
    it->spine_len = it->spine_cap = 0;
    it->seen = NULL;
    it->seen_len = it->seen_cap = 0;
    it->at = -1;
    push_left(it, root);
}

static int has_next(Iter *it) { return it->at + 1 < it->seen_len || it->spine_len > 0; }

static int32_t next(Iter *it) {
    it->at += 1;
    if (it->at == it->seen_len) {
        Node *n = it->spine[--it->spine_len];
        if (it->seen_len == it->seen_cap) {
            it->seen_cap = it->seen_cap ? it->seen_cap * 2 : 4;
            it->seen = realloc(it->seen, it->seen_cap * sizeof(int32_t));
        }
        it->seen[it->seen_len++] = n->val;
        push_left(it, n->right);
    }
    return it->seen[it->at];
}

static int has_prev(Iter *it) { return it->at > 0; }

static int32_t prev(Iter *it) {
    it->at -= 1;
    return it->seen[it->at];
}

static Node *leaf(int32_t v) {
    Node *n = malloc(sizeof(Node));
    n->val = v;
    n->left = n->right = NULL;
    return n;
}

static int insert(Node *root, int32_t v) {
    Node *node = root;
    for (;;) {
        if (v == node->val) return 0;
        Node **child = v < node->val ? &node->left : &node->right;
        if (*child) {
            node = *child;
        } else {
            *child = leaf(v);
            return 1;
        }
    }
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

static int64_t *draw_calls(int64_t n, int64_t count, int64_t *seed) {
    int64_t at = -1;
    int64_t *calls = malloc(count * sizeof(int64_t));
    for (int64_t i = 0; i < count; i++) {
        int64_t r = next_random(seed) % 6;
        if (r >= 2 && r <= 4 && at + 1 < n) {
            at += 1;
            calls[i] = 1;
        } else if (r == 5 && at > 0) {
            at -= 1;
            calls[i] = 3;
        } else {
            calls[i] = r % 2 * 2;
        }
    }
    return calls;
}

static int64_t *drive(Node *root, const int64_t *calls, int64_t count) {
    Iter it;
    iter_new(&it, root);
    int64_t *out = malloc(count * sizeof(int64_t));
    for (int64_t i = 0; i < count; i++) {
        switch (calls[i]) {
        case 0: out[i] = has_next(&it); break;
        case 1: out[i] = next(&it); break;
        case 2: out[i] = has_prev(&it); break;
        default: out[i] = prev(&it); break;
        }
    }
    free(it.spine);
    free(it.seen);
    return out;
}

int main(void) {
    int64_t seed = 1586;
    Node *roots[20];
    int64_t *calls[20];
    int64_t nodes = 0;
    int32_t *values = malloc(100000 * sizeof(int32_t));
    for (int k = 0; k < 20; k++) {
        for (int i = 0; i < 100000; i++) {
            int64_t a = next_random(&seed);
            int64_t b = next_random(&seed);
            values[i] = (int32_t)((a * 32768 + b) % 1000000);
        }
        Node *root = leaf(values[0]);
        int64_t n = 1;
        for (int i = 1; i < 100000; i++) n += insert(root, values[i]);
        roots[k] = root;
        nodes += n;
        calls[k] = draw_calls(n, 300000, &seed);
    }
    int64_t check = 0;
    for (int k = 0; k < 20; k++) {
        int64_t *answers = drive(roots[k], calls[k], 300000);
        for (int64_t i = 0; i < 300000; i++) check = mix(check, answers[i]);
        free(answers);
    }
    printf("20 trees of 100000 values: %lld nodes, 6000000 calls, checksum %lld\n", (long long)nodes, (long long)check);
    return 0;
}
