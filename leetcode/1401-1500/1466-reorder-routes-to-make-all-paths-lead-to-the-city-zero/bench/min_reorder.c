// LeetCode #1466 bench in C: the ★ arm (a breadth-first search out of city
// 0 over the roads taken both ways) on the same 10 trees of 50000 cities
// and 20 passes. Each city's roads are a growable array, as the other
// implementations' lists of lists are.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int next, away;
} Road;

typedef struct {
    Road *items;
    int len, cap;
} Roads;

static void push(Roads *r, int next, int away) {
    if (r->len == r->cap) {
        r->cap = r->cap ? r->cap * 2 : 4;
        r->items = realloc(r->items, sizeof(Road) * r->cap);
    }
    r->items[r->len++] = (Road){next, away};
}

static int min_reorder(int n, int (*connections)[2], int m) {
    Roads *roads = calloc(n, sizeof(Roads));
    for (int i = 0; i < m; i++) {
        push(&roads[connections[i][0]], connections[i][1], 1);
        push(&roads[connections[i][1]], connections[i][0], 0);
    }
    bool *seen = calloc(n, sizeof(bool));
    int *queue = malloc(sizeof(int) * n);
    int head = 0, tail = 0;
    seen[0] = true;
    queue[tail++] = 0;
    int turned = 0;
    while (head < tail) {
        int city = queue[head++];
        for (int i = 0; i < roads[city].len; i++) {
            Road r = roads[city].items[i];
            if (!seen[r.next]) {
                seen[r.next] = true;
                turned += r.away;
                queue[tail++] = r.next;
            }
        }
    }
    for (int i = 0; i < n; i++) free(roads[i].items);
    free(roads);
    free(seen);
    free(queue);
    return turned;
}

static int64_t seed = 1466;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    enum { N = 50000, TREES = 10 };
    int (*trees)[N - 1][2] = malloc(sizeof(int) * TREES * (N - 1) * 2);
    int *label = malloc(sizeof(int) * N);
    for (int t = 0; t < TREES; t++) {
        for (int c = 0; c < N; c++) label[c] = c;
        for (int64_t i = N - 1; i >= 1; i--) {
            int64_t j = next_random() % (i + 1);
            int x = label[i];
            label[i] = label[j];
            label[j] = x;
        }
        for (int64_t i = 1; i < N; i++) {
            int64_t p = next_random() % i;
            if (next_random() % 2 == 0) {
                trees[t][i - 1][0] = label[i];
                trees[t][i - 1][1] = label[p];
            } else {
                trees[t][i - 1][0] = label[p];
                trees[t][i - 1][1] = label[i];
            }
        }
    }
    int64_t check = 0;
    for (int64_t pass = 0; pass < 20; pass++) {
        for (int t = 0; t < TREES; t++) {
            int k = (int)(check % (N - 1));
            int x = trees[t][k][0];
            trees[t][k][0] = trees[t][k][1];
            trees[t][k][1] = x;
            int got = min_reorder(N, trees[t], N - 1);
            check = (check * 31 + got + pass) % 1000000007;
        }
    }
    printf("20 passes over 10 trees of 50000 cities: checksum %lld\n", (long long)check);
    free(trees);
    free(label);
    return 0;
}
