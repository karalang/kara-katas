// LeetCode #913: Cat and Mouse -- bench: C mirror of the retrograde
// analysis with a queue in cat_mouse_game.kara.

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t n;
    int64_t *degree;
    int64_t **near;
} Graph;

static int64_t cat_mouse_game(const Graph *g) {
    int64_t n = g->n;
    int64_t *result = calloc(n * n * 2, sizeof(int64_t));
    int64_t *left = calloc(n * n * 2, sizeof(int64_t));
    for (int64_t m = 0; m < n; m++) {
        for (int64_t c = 1; c < n; c++) {
            left[(m * n + c) * 2] = g->degree[m];
            int64_t moves = 0;
            for (int64_t k = 0; k < g->degree[c]; k++) {
                if (g->near[c][k] != 0)
                    moves += 1;
            }
            left[(m * n + c) * 2 + 1] = moves;
        }
    }
    int64_t *queue = malloc(sizeof(int64_t) * n * n * 2);
    int64_t tail = 0;
    for (int64_t c = 1; c < n; c++) {
        for (int64_t t = 0; t < 2; t++) {
            result[c * 2 + t] = 1;
            queue[tail++] = c * 2 + t;
            result[(c * n + c) * 2 + t] = 2;
            queue[tail++] = (c * n + c) * 2 + t;
        }
    }
    int64_t head = 0;
    while (head < tail) {
        int64_t s = queue[head++];
        int64_t t = s % 2;
        int64_t c = s / 2 % n;
        int64_t m = s / 2 / n;
        int64_t won = result[s];
        if (t == 1) {
            for (int64_t k = 0; k < g->degree[m]; k++) {
                int64_t p = (g->near[m][k] * n + c) * 2;
                if (result[p] == 0) {
                    if (won == 1) {
                        result[p] = 1;
                        queue[tail++] = p;
                    } else if (--left[p] == 0) {
                        result[p] = 2;
                        queue[tail++] = p;
                    }
                }
            }
        } else {
            for (int64_t k = 0; k < g->degree[c]; k++) {
                int64_t pc = g->near[c][k];
                if (pc != 0) {
                    int64_t p = (m * n + pc) * 2 + 1;
                    if (result[p] == 0) {
                        if (won == 2) {
                            result[p] = 2;
                            queue[tail++] = p;
                        } else if (--left[p] == 0) {
                            result[p] = 1;
                            queue[tail++] = p;
                        }
                    }
                }
            }
        }
    }
    int64_t answer = result[(n + 2) * 2];
    free(result);
    free(left);
    free(queue);
    return answer;
}

static int64_t seed = 913;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static Graph random_graph(int64_t n, int64_t per) {
    bool *adj = calloc(n * n, sizeof(bool));
    for (int64_t u = 0; u < n; u++) {
        for (int64_t v = u + 1; v < n; v++) {
            int64_t chance = u == 0 ? per / 4 : per;
            if (next_random() % 1000 < chance) {
                adj[u * n + v] = true;
                adj[v * n + u] = true;
            }
        }
    }
    for (int64_t v = 1; v < n; v++) {
        bool alone = true;
        for (int64_t u = 1; u < n; u++) {
            if (adj[v * n + u])
                alone = false;
        }
        if (alone) {
            int64_t u = 1 + next_random() % (n - 2);
            if (u >= v)
                u += 1;
            adj[u * n + v] = true;
            adj[v * n + u] = true;
        }
    }
    bool hole_alone = true;
    for (int64_t u = 1; u < n; u++) {
        if (adj[u])
            hole_alone = false;
    }
    if (hole_alone) {
        int64_t u = 1 + next_random() % (n - 1);
        adj[u] = true;
        adj[u * n] = true;
    }
    Graph g = {n, malloc(sizeof(int64_t) * n), malloc(sizeof(int64_t *) * n)};
    for (int64_t v = 0; v < n; v++) {
        g.near[v] = malloc(sizeof(int64_t) * n);
        g.degree[v] = 0;
        for (int64_t u = 0; u < n; u++) {
            if (adj[v * n + u])
                g.near[v][g.degree[v]++] = u;
        }
    }
    free(adj);
    return g;
}

int main(void) {
    int64_t rounds = 4000;
    int64_t wins[3] = {0, 0, 0};
    int64_t check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t per = r % 4 == 0 ? 20 : r % 4 == 1 ? 60 : r % 4 == 2 ? 150 : 400;
        Graph g = random_graph(50, per);
        int64_t outcome = cat_mouse_game(&g);
        wins[outcome] += 1;
        check = (check * 7 + outcome) % 1000000007;
        for (int64_t v = 0; v < g.n; v++)
            free(g.near[v]);
        free(g.near);
        free(g.degree);
    }
    printf("%lld graphs of 50 nodes: %lld draws, %lld mouse wins, %lld cat wins, checksum %lld\n", (long long)rounds,
           (long long)wins[0], (long long)wins[1], (long long)wins[2], (long long)check);
    return 0;
}
