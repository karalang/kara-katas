// LeetCode #1660: Correct a Binary Tree -- the bench's C mirror: the ★
// arm on 40 random trees of 100000 nodes, each broken once, all built
// first. Nodes come from one array per tree, and the values met are an
// open-addressing hash set written out here.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

enum { TREES = 40, NODES = 100000, CAP = 1 << 18 };

typedef struct Node {
    int32_t val;
    struct Node *left;
    struct Node *right;
} Node;

typedef struct {
    int32_t *slots; // value + 1; 0 is empty
} Set;

static size_t slot_of(int32_t v) {
    return ((uint64_t)(uint32_t)v * 0x9E3779B97F4A7C15ull) >> (64 - 18);
}

static int set_contains(const Set *s, int32_t v) {
    for (size_t i = slot_of(v);; i = (i + 1) & (CAP - 1)) {
        if (s->slots[i] == 0) return 0;
        if (s->slots[i] == v + 1) return 1;
    }
}

static void set_insert(Set *s, int32_t v) {
    for (size_t i = slot_of(v);; i = (i + 1) & (CAP - 1)) {
        if (s->slots[i] == 0) {
            s->slots[i] = v + 1;
            return;
        }
        if (s->slots[i] == v + 1) return;
    }
}

static Node *correct(Node *node, Set *seen) {
    if (node == NULL) return NULL;
    if (node->right != NULL && set_contains(seen, node->right->val)) return NULL;
    set_insert(seen, node->val);
    node->right = correct(node->right, seen);
    node->left = correct(node->left, seen);
    return node;
}

static Node *correct_binary_tree(Node *root) {
    Set seen;
    seen.slots = calloc(CAP, sizeof(int32_t));
    Node *r = correct(root, &seen);
    free(seen.slots);
    return r;
}

static int64_t seed = 1660;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t big(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

typedef struct {
    Node *node;
    int left;
} Slot;

static Node *random_tree(int64_t n, Node *pool) {
    int32_t *values = malloc(sizeof(int32_t) * n);
    for (int64_t i = 0; i < n; i++) values[i] = (int32_t)i;
    for (int64_t i = n - 1; i >= 1; i--) {
        int64_t j = big() % (i + 1);
        int32_t t = values[i];
        values[i] = values[j];
        values[j] = t;
    }
    for (int64_t i = 0; i < n; i++) {
        pool[i].val = values[i];
        pool[i].left = pool[i].right = NULL;
    }
    Node *root = &pool[0];
    Slot *free_slots = malloc(sizeof(Slot) * (2 * n + 2));
    size_t len = 0;
    free_slots[len++] = (Slot){root, 1};
    free_slots[len++] = (Slot){root, 0};
    for (int64_t i = 1; i < n; i++) {
        size_t k = (size_t)(big() % (int64_t)len);
        Slot s = free_slots[k];
        free_slots[k] = free_slots[--len];
        Node *child = &pool[i];
        if (s.left) s.node->left = child;
        else s.node->right = child;
        free_slots[len++] = (Slot){child, 1};
        free_slots[len++] = (Slot){child, 0};
    }
    free(free_slots);
    free(values);
    return root;
}

// the levels, left to right, laid end to end, with where each starts
static int break_tree(Node *root, int64_t n, Node **order, int64_t *starts) {
    int64_t pairs = 0, len = 0, levels = 0;
    order[len++] = root;
    int64_t begin = 0;
    while (begin < len) {
        int64_t end = len;
        starts[levels++] = begin;
        for (int64_t i = begin; i < end; i++) {
            Node *node = order[i];
            if (node->right == NULL) pairs += end - 1 - i;
            if (node->left) order[len++] = node->left;
            if (node->right) order[len++] = node->right;
        }
        begin = end;
    }
    starts[levels] = len;
    (void)n;
    if (pairs == 0) return 0;
    int64_t k = big() % pairs;
    for (int64_t l = 0; l < levels; l++) {
        int64_t b = starts[l], e = starts[l + 1];
        for (int64_t i = b; i < e; i++) {
            Node *node = order[i];
            if (node->right == NULL) {
                int64_t after = e - 1 - i;
                if (k < after) {
                    node->right = order[i + 1 + k];
                    return 1;
                }
                k -= after;
            }
        }
    }
    return 0;
}

static int64_t fold(Node *root, int64_t *check, Node **queue) {
    // a queue of nodes, NULL for a missing child
    int64_t head = 0, tail = 0, count = 0;
    queue[tail++] = root;
    while (head < tail) {
        Node *node = queue[head++];
        if (node == NULL) {
            *check = mix(*check, 0);
        } else {
            count++;
            *check = mix(*check, (int64_t)node->val + 1);
            queue[tail++] = node->left;
            queue[tail++] = node->right;
        }
    }
    return count;
}

int main(void) {
    Node *pools[TREES];
    Node **order = malloc(sizeof(Node *) * NODES);
    int64_t *starts = malloc(sizeof(int64_t) * (NODES + 2));
    int t = 0;
    Node *pool = malloc(sizeof(Node) * NODES);
    while (t < TREES) {
        Node *root = random_tree(NODES, pool);
        if (break_tree(root, NODES, order, starts)) {
            pools[t++] = pool;
            pool = malloc(sizeof(Node) * NODES);
        }
    }
    free(pool);
    Node **queue = malloc(sizeof(Node *) * (2 * NODES + 1));
    int64_t check = 0, kept = 0;
    for (int i = 0; i < TREES; i++) {
        kept += fold(correct_binary_tree(&pools[i][0]), &check, queue);
    }
    printf("40 trees of 100000 nodes: %lld nodes kept, checksum %lld\n", (long long)kept, (long long)check);
    for (int i = 0; i < TREES; i++) free(pools[i]);
    free(queue);
    free(order);
    free(starts);
    return 0;
}
