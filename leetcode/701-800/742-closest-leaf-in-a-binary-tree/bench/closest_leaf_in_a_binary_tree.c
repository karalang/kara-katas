// LeetCode #742: Closest Leaf in a Binary Tree -- breadth first from k.
// Benchmark mirror of the Kara star arm: treat the tree as an undirected
// graph, each node's neighbours its children and its parent, and search
// outward from k a layer at a time; the first layer holding a leaf holds
// the nearest ones, and the smallest value of those is returned. The
// parent table, the seen marks and the layers are growable arrays made
// afresh in each call, as in the Kara arm.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t val, left, right;
} Node;

typedef struct {
    int64_t *data;
    int64_t len, cap;
} Vec;

static void push(Vec *v, int64_t x) {
    if (v->len == v->cap) {
        v->cap = v->cap ? v->cap * 2 : 4;
        v->data = realloc(v->data, v->cap * sizeof(int64_t));
    }
    v->data[v->len++] = x;
}

static int64_t find_closest_leaf(const Node *nodes, int64_t n, int64_t k) {
    Vec parent = {0, 0, 0};
    int64_t start = 0;
    for (int64_t i = 0; i < n; i++) {
        push(&parent, -1);
        if (nodes[i].val == k) start = i;
    }
    for (int64_t i = 0; i < n; i++) {
        if (nodes[i].left != -1) parent.data[nodes[i].left] = i;
        if (nodes[i].right != -1) parent.data[nodes[i].right] = i;
    }
    bool *seen = NULL;
    int64_t seen_len = 0, seen_cap = 0;
    for (int64_t i = 0; i < n; i++) {
        if (seen_len == seen_cap) {
            seen_cap = seen_cap ? seen_cap * 2 : 4;
            seen = realloc(seen, seen_cap * sizeof(bool));
        }
        seen[seen_len++] = false;
    }
    seen[start] = true;
    Vec layer = {0, 0, 0};
    push(&layer, start);
    int64_t result;
    for (;;) {
        int64_t best = -1;
        for (int64_t j = 0; j < layer.len; j++) {
            const Node *node = &nodes[layer.data[j]];
            if (node->left == -1 && node->right == -1 && (best == -1 || node->val < best)) best = node->val;
        }
        if (best != -1) {
            result = best;
            break;
        }
        Vec next = {0, 0, 0};
        for (int64_t j = 0; j < layer.len; j++) {
            int64_t x = layer.data[j];
            int64_t around[3] = {nodes[x].left, nodes[x].right, parent.data[x]};
            for (int t = 0; t < 3; t++) {
                int64_t y = around[t];
                if (y != -1 && !seen[y]) {
                    seen[y] = true;
                    push(&next, y);
                }
            }
        }
        free(layer.data);
        layer = next;
    }
    free(layer.data);
    free(seen);
    free(parent.data);
    return result;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 742, n = 1000;
    int64_t *values = malloc(n * sizeof(int64_t));
    for (int64_t v = 0; v < n; v++) values[v] = v + 1;
    for (int64_t i = 0; i < n; i++) {
        int64_t j = i + next_random(&seed) % (n - i);
        int64_t t = values[i];
        values[i] = values[j];
        values[j] = t;
    }
    Node *nodes = malloc(n * sizeof(Node));
    nodes[0] = (Node){values[0], -1, -1};
    for (int64_t i = 1; i < n; i++) {
        for (;;) {
            int64_t p = next_random(&seed) % i;
            if (next_random(&seed) % 2 == 0) {
                if (nodes[p].left == -1) {
                    nodes[p].left = i;
                    break;
                }
            } else if (nodes[p].right == -1) {
                nodes[p].right = i;
                break;
            }
        }
        nodes[i] = (Node){values[i], -1, -1};
    }
    int64_t total = 0;
    for (int r = 0; r < 60; r++) {
        int64_t a = next_random(&seed) % n;
        int64_t b = next_random(&seed) % n;
        int64_t t = nodes[a].val;
        nodes[a].val = nodes[b].val;
        nodes[b].val = t;
        for (int64_t k = 1; k <= n; k++) total += find_closest_leaf(nodes, n, k);
    }
    printf("60 rounds of 1000 queries on a 1000-node tree: answers sum to %lld\n", (long long)total);
    free(nodes);
    free(values);
    return 0;
}
