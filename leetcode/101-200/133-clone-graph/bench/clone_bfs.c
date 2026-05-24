/*
 * LeetCode 133 — BFS clone of a 10-regular ring, bench mirror in C.
 *
 * Algorithmic mirror of bench/clone_bfs.{kara,rs,py}. N=2000, HALF_DEG=5,
 * K=500 clones. Stdout sink: 500.
 *
 * Open-addressing hash map (no libc hash table) keyed by node val.
 * black_box_root keeps LLVM from hoisting clone_graph out of the K loop.
 *
 * See ../README.md § Benchmarks for what the numbers mean.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>

#define N_NODES 2000
#define HALF_DEG 5
#define K_CLONES 500
#define MAP_CAP 4096

typedef struct Node {
    int64_t val;
    struct Node **neighbors;
    size_t n_neighbors;
    size_t cap_neighbors;
} Node;

static int64_t map_keys[MAP_CAP];
static Node *map_vals[MAP_CAP];
static bool map_used[MAP_CAP];

static inline size_t hash_key(int64_t k) {
    uint64_t x = (uint64_t)k;
    x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9ULL;
    x = (x ^ (x >> 27)) * 0x94d049bb133111ebULL;
    x = x ^ (x >> 31);
    return (size_t)(x & (MAP_CAP - 1));
}

static void map_reset(void) {
    memset(map_used, 0, sizeof map_used);
}

static Node *map_get(int64_t k) {
    size_t h = hash_key(k);
    for (;;) {
        if (!map_used[h]) {
            return NULL;
        }
        if (map_keys[h] == k) {
            return map_vals[h];
        }
        h = (h + 1) & (MAP_CAP - 1);
    }
}

static void map_insert(int64_t k, Node *v) {
    size_t h = hash_key(k);
    for (;;) {
        if (!map_used[h]) {
            map_used[h] = true;
            map_keys[h] = k;
            map_vals[h] = v;
            return;
        }
        if (map_keys[h] == k) {
            map_vals[h] = v;
            return;
        }
        h = (h + 1) & (MAP_CAP - 1);
    }
}

static Node *make_node(int64_t val, size_t neighbor_cap) {
    Node *n = (Node *)malloc(sizeof(Node));
    if (!n) {
        return NULL;
    }
    n->val = val;
    n->cap_neighbors = neighbor_cap;
    n->n_neighbors = 0;
    n->neighbors = (Node **)malloc(neighbor_cap * sizeof(Node *));
    if (!n->neighbors) {
        free(n);
        return NULL;
    }
    return n;
}

static void push_neighbor(Node *n, Node *nb) {
    if (n->n_neighbors >= n->cap_neighbors) {
        size_t new_cap = n->cap_neighbors * 2;
        Node **nn = (Node **)realloc(n->neighbors, new_cap * sizeof(Node *));
        if (!nn) {
            return;
        }
        n->neighbors = nn;
        n->cap_neighbors = new_cap;
    }
    n->neighbors[n->n_neighbors++] = nb;
}

static Node *black_box_root(Node *p) {
#if defined(__GNUC__) || defined(__clang__)
    __asm__ volatile("" : "+r"(p) :: "memory");
#endif
    return p;
}

static Node *clone_graph(Node *root) {
    map_reset();
    int64_t root_val = root->val;
    Node *root_clone = make_node(root_val, 16);
    map_insert(root_val, root_clone);

    Node **queue = (Node **)malloc(N_NODES * sizeof(Node *));
    if (!queue) {
        return root_clone;
    }
    size_t q_head = 0, q_tail = 0;
    queue[q_tail++] = root;

    while (q_head < q_tail) {
        Node *curr = queue[q_head++];
        int64_t curr_val = curr->val;
        Node *curr_clone = map_get(curr_val);
        for (size_t i = 0; i < curr->n_neighbors; i++) {
            Node *nb = curr->neighbors[i];
            int64_t nb_val = nb->val;
            if (map_get(nb_val) == NULL) {
                map_insert(nb_val, make_node(nb_val, 16));
                queue[q_tail++] = nb;
            }
            push_neighbor(curr_clone, map_get(nb_val));
        }
    }

    free(queue);
    return map_get(root_val);
}

int main(void) {
    Node **nodes = (Node **)malloc(N_NODES * sizeof(Node *));
    if (!nodes) {
        fprintf(stderr, "malloc failed\n");
        return 1;
    }
    for (int i = 0; i < N_NODES; i++) {
        nodes[i] = make_node((int64_t)(i + 1), 10);
        if (!nodes[i]) {
            fprintf(stderr, "malloc failed\n");
            return 1;
        }
    }
    for (int i = 0; i < N_NODES; i++) {
        for (int d = 1; d <= HALF_DEG; d++) {
            int j = (i + d) % N_NODES;
            push_neighbor(nodes[i], nodes[j]);
            push_neighbor(nodes[j], nodes[i]);
        }
    }

    int64_t sum = 0;
    for (int k = 0; k < K_CLONES; k++) {
        Node *c = clone_graph(black_box_root(nodes[0]));
        sum += c->val;
    }
    printf("%lld\n", (long long)sum);
    return 0;
}
