/* LeetCode #133 — C pthreads-parallel mirror (par-lane BARE-METAL FLOOR, clone_bfs).
 * Same BFS clone of a 10-regular ring (N=2000) as clone_bfs.c; the K=500 clone
 * reduction split across a fixed pool of _SC_NPROCESSORS_ONLN pthreads (spawn
 * once, chunk, join+merge). Raw OS threads, no runtime — the ceiling the kara
 * hand-written `par {}` is measured against.
 *
 * The seq clone_bfs.c keyed every clone through a single GLOBAL open-addressing
 * map — not reentrant. Here the map is a per-thread `Map` context (clone_graph
 * takes a `Map *`), so each worker has its own. The input ring is built once in
 * main and shared read-only across workers: C pointers are freely shareable, so
 * — unlike the rayon mirror, which must rebuild the graph per worker because
 * Rust's `Rc` is not `Send` — no per-worker graph rebuild is needed. Cloned
 * nodes are malloc'd and never freed, exactly as the seq mirror does (the K=500
 * clones of a 2000-node ring are bounded; a benchmark mirror need not reclaim).
 * Sink = 500 (K × root clone val 1). black_box_root keeps clone_graph in the K
 * loop. Build: clang -O3 clone_bfs_par.c -o … -lpthread */
#include <pthread.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

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

/* Per-thread open-addressing map (replaces the seq mirror's file-global one). */
typedef struct {
    int64_t keys[MAP_CAP];
    Node *vals[MAP_CAP];
    bool used[MAP_CAP];
} Map;

static inline size_t hash_key(int64_t k) {
    uint64_t x = (uint64_t)k;
    x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9ULL;
    x = (x ^ (x >> 27)) * 0x94d049bb133111ebULL;
    x = x ^ (x >> 31);
    return (size_t)(x & (MAP_CAP - 1));
}

static void map_reset(Map *m) {
    memset(m->used, 0, sizeof m->used);
}

static Node *map_get(Map *m, int64_t k) {
    size_t h = hash_key(k);
    for (;;) {
        if (!m->used[h]) {
            return NULL;
        }
        if (m->keys[h] == k) {
            return m->vals[h];
        }
        h = (h + 1) & (MAP_CAP - 1);
    }
}

static void map_insert(Map *m, int64_t k, Node *v) {
    size_t h = hash_key(k);
    for (;;) {
        if (!m->used[h]) {
            m->used[h] = true;
            m->keys[h] = k;
            m->vals[h] = v;
            return;
        }
        if (m->keys[h] == k) {
            m->vals[h] = v;
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

static Node *clone_graph(Map *m, Node *root) {
    map_reset(m);
    int64_t root_val = root->val;
    Node *root_clone = make_node(root_val, 16);
    map_insert(m, root_val, root_clone);

    Node **queue = (Node **)malloc(N_NODES * sizeof(Node *));
    if (!queue) {
        return root_clone;
    }
    size_t q_head = 0, q_tail = 0;
    queue[q_tail++] = root;

    while (q_head < q_tail) {
        Node *curr = queue[q_head++];
        int64_t curr_val = curr->val;
        Node *curr_clone = map_get(m, curr_val);
        for (size_t i = 0; i < curr->n_neighbors; i++) {
            Node *nb = curr->neighbors[i];
            int64_t nb_val = nb->val;
            if (map_get(m, nb_val) == NULL) {
                map_insert(m, nb_val, make_node(nb_val, 16));
                queue[q_tail++] = nb;
            }
            push_neighbor(curr_clone, map_get(m, nb_val));
        }
    }

    free(queue);
    return map_get(m, root_val);
}

typedef struct {
    Node **nodes; /* shared read-only ring */
    long start, end;
    int64_t partial;
} Work;

static void *worker(void *arg) {
    Work *w = (Work *)arg;
    Map *m = (Map *)malloc(sizeof(Map)); /* per-thread map context */
    int64_t s = 0;
    for (long k = w->start; k < w->end; k++) {
        Node *c = clone_graph(m, black_box_root(w->nodes[0]));
        s += c->val;
    }
    free(m);
    w->partial = s;
    return NULL;
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

    long nworkers = sysconf(_SC_NPROCESSORS_ONLN);
    if (nworkers < 1) {
        nworkers = 1;
    }
    if (nworkers > K_CLONES) {
        nworkers = K_CLONES;
    }
    pthread_t *threads = malloc((size_t)nworkers * sizeof(pthread_t));
    Work *works = malloc((size_t)nworkers * sizeof(Work));
    long chunk = K_CLONES / nworkers;
    for (long w = 0; w < nworkers; w++) {
        works[w].nodes = nodes;
        works[w].start = w * chunk;
        works[w].end = (w == nworkers - 1) ? K_CLONES : (w + 1) * chunk;
        works[w].partial = 0;
        pthread_create(&threads[w], NULL, worker, &works[w]);
    }
    int64_t sum = 0;
    for (long w = 0; w < nworkers; w++) {
        pthread_join(threads[w], NULL);
        sum += works[w].partial;
    }
    printf("%lld\n", (long long)sum);
    free(threads);
    free(works);
    return 0;
}
