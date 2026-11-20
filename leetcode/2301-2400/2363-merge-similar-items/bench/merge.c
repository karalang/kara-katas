// LeetCode #2363: Merge Similar Items -- the bench, the ★ arm in C: every
// item of both lists added into a sorted map from value to total weight,
// which walks out in order of value. C has no ordered map, so the totals
// live in a treap keyed by value, with insert-or-add and an in-order walk.

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

static Node *rotate_right(Node *t) {
    Node *l = t->left;
    t->left = l->right;
    l->right = t;
    return l;
}

static Node *rotate_left(Node *t) {
    Node *r = t->right;
    t->right = r->left;
    r->left = t;
    return r;
}

// adds weight to key's total, inserting key at 0 first if it is missing
static Node *add(Node *t, int64_t key, int64_t weight) {
    if (!t) {
        Node *n = malloc(sizeof(Node));
        n->key = key;
        n->value = weight;
        n->prio = next_prio();
        n->left = n->right = NULL;
        return n;
    }
    if (key == t->key) {
        t->value += weight;
    } else if (key < t->key) {
        t->left = add(t->left, key, weight);
        if (t->left->prio > t->prio) {
            t = rotate_right(t);
        }
    } else {
        t->right = add(t->right, key, weight);
        if (t->right->prio > t->prio) {
            t = rotate_left(t);
        }
    }
    return t;
}

// writes the pairs in order of key and frees the tree
static void walk(Node *t, int64_t *out, int64_t *len) {
    if (!t) {
        return;
    }
    walk(t->left, out, len);
    out[2 * *len] = t->key;
    out[2 * *len + 1] = t->value;
    (*len)++;
    walk(t->right, out, len);
    free(t);
}

// merged pairs into out (value, weight, value, weight, ...); returns how many
static int64_t merge_similar_items(const int64_t *items1, int64_t n, const int64_t *items2, int64_t m, int64_t *out) {
    Node *totals = NULL;
    for (int64_t i = 0; i < n; i++) {
        totals = add(totals, items1[2 * i], items1[2 * i + 1]);
    }
    for (int64_t i = 0; i < m; i++) {
        totals = add(totals, items2[2 * i], items2[2 * i + 1]);
    }
    int64_t len = 0;
    walk(totals, out, &len);
    return len;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t *random_items(int64_t *seed, int64_t count) {
    // count distinct values from 1 to 1000 in a shuffled order, each with
    // a weight of 1 to 1000
    int64_t values[1000];
    for (int64_t i = 0; i < 1000; i++) {
        values[i] = i + 1;
    }
    for (int64_t i = 999; i >= 1; i--) {
        int64_t j = next_random(seed) % (i + 1);
        int64_t t = values[i];
        values[i] = values[j];
        values[j] = t;
    }
    int64_t *items = malloc(2 * count * sizeof(int64_t));
    for (int64_t i = 0; i < count; i++) {
        items[2 * i] = values[i];
        items[2 * i + 1] = 1 + next_random(seed) % 1000;
    }
    return items;
}

int main(void) {
    // pair a: lists of 100 (a + 1) and 1000 - 50 a items
    int64_t seed = 2363;
    int64_t *first[10], *second[10];
    int64_t n[10], m[10];
    for (int64_t a = 0; a < 10; a++) {
        n[a] = 100 * (a + 1);
        m[a] = 1000 - 50 * a;
        first[a] = random_items(&seed, n[a]);
        second[a] = random_items(&seed, m[a]);
    }
    int64_t *out = malloc(2 * 2000 * sizeof(int64_t));
    int64_t check = 0;
    for (int64_t p = 0; p < 400; p++) {
        for (int a = 0; a < 10; a++) {
            int64_t len = merge_similar_items(first[a], n[a], second[a], m[a], out);
            check = (check * 31 + len * 1009 + out[2 * (len - 1) + 1] + p) % 1000000007;
        }
    }
    printf("400 passes over 10 pairs of lists: checksum %lld\n", (long long)check);
    free(out);
    for (int a = 0; a < 10; a++) {
        free(first[a]);
        free(second[a]);
    }
    return 0;
}
