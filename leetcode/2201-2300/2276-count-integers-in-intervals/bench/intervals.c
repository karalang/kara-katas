// LeetCode #2276: Count Integers in Intervals -- the bench, the ★ arm.
// C has no ordered map, so the disjoint intervals live in a treap keyed
// by start, with `floor` and removal by key.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int64_t key, value;
    uint32_t prio;
    struct Node *left, *right;
} Node;

static uint32_t prio_state = 2463534242u;

static uint32_t next_prio(void) {
    prio_state ^= prio_state << 13;
    prio_state ^= prio_state >> 17;
    prio_state ^= prio_state << 5;
    return prio_state;
}

// splits into keys < key and keys >= key
static void split(Node *t, int64_t key, Node **l, Node **r) {
    if (!t) {
        *l = *r = NULL;
    } else if (t->key < key) {
        split(t->right, key, &t->right, r);
        *l = t;
    } else {
        split(t->left, key, l, &t->left);
        *r = t;
    }
}

static Node *merge(Node *l, Node *r) {
    if (!l) return r;
    if (!r) return l;
    if (l->prio > r->prio) {
        l->right = merge(l->right, r);
        return l;
    }
    r->left = merge(l, r->left);
    return r;
}

static Node *insert(Node *t, int64_t key, int64_t value) {
    Node *n = malloc(sizeof(Node));
    n->key = key;
    n->value = value;
    n->prio = next_prio();
    n->left = n->right = NULL;
    Node *l, *r;
    split(t, key, &l, &r);
    return merge(merge(l, n), r);
}

static Node *erase(Node *t, int64_t key) {
    if (!t) return NULL;
    if (t->key == key) {
        Node *m = merge(t->left, t->right);
        free(t);
        return m;
    }
    if (key < t->key) t->left = erase(t->left, key);
    else t->right = erase(t->right, key);
    return t;
}

static Node *floor_node(Node *t, int64_t key) {
    Node *best = NULL;
    while (t) {
        if (t->key <= key) {
            best = t;
            t = t->right;
        } else {
            t = t->left;
        }
    }
    return best;
}

static void destroy(Node *t) {
    if (!t) return;
    destroy(t->left);
    destroy(t->right);
    free(t);
}

typedef struct {
    Node *spans;
    int64_t total;
} CountIntervals;

static void add(CountIntervals *c, int64_t left, int64_t right) {
    int64_t l = left, r = right;
    for (;;) {
        Node *f = floor_node(c->spans, r);
        if (!f) break;
        int64_t a = f->key, b = f->value;
        if (b < l) break;
        if (a < l) l = a;
        if (b > r) r = b;
        c->total -= b - a + 1;
        c->spans = erase(c->spans, a);
    }
    c->total += r - l + 1;
    c->spans = insert(c->spans, l, r);
}

// ---- bench harness ---------------------------------------------------------

static int64_t seed = 2276;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t wide_random(void) {
    int64_t high = next_random();
    return high * 32768 + next_random();
}

int main(void) {
    int64_t check = 0;
    for (int t = 0; t < 10; t++) {
        int64_t span = t % 2 == 0 ? 1000000000 : 1000000;
        CountIntervals c = {NULL, 0};
        for (int i = 0; i < 100000; i++) {
            if (next_random() % 3 == 0) {
                check = (check * 31 + c.total) % 1000000007;
            } else {
                int64_t left = wide_random() % span + 1;
                int64_t right = left + wide_random() % 1000;
                if (right > 1000000000) right = 1000000000;
                add(&c, left, right);
            }
        }
        destroy(c.spans);
    }
    printf("10 runs of 10^5: checksum %lld\n", (long long)check);
    return 0;
}
