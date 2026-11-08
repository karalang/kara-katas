// LeetCode #1519 bench: the ★ arm (counts returned up a recursive walk),
// as labels.kara: each walk returns a fresh array of 26 counts.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t *items;
    int64_t len, cap;
} List;

static void push(List *l, int64_t x) {
    if (l->len == l->cap) {
        l->cap = l->cap ? l->cap * 2 : 4;
        l->items = realloc(l->items, (size_t)l->cap * sizeof(int64_t));
    }
    l->items[l->len++] = x;
}

static int64_t *walk(int64_t node, int64_t parent, const List *adjacent, const char *labels, int64_t *answer) {
    int64_t *counts = calloc(26, sizeof(int64_t));
    for (int64_t i = 0; i < adjacent[node].len; i++) {
        int64_t next = adjacent[node].items[i];
        if (next != parent) {
            int64_t *below = walk(next, node, adjacent, labels, answer);
            for (int c = 0; c < 26; c++) counts[c] += below[c];
            free(below);
        }
    }
    int64_t mine = labels[node] - 97;
    counts[mine] += 1;
    answer[node] = counts[mine];
    return counts;
}

static int64_t *count_sub_trees(int64_t n, const int64_t (*edges)[2], const char *labels) {
    List *adjacent = calloc((size_t)n, sizeof(List));
    for (int64_t i = 0; i < n - 1; i++) {
        push(&adjacent[edges[i][0]], edges[i][1]);
        push(&adjacent[edges[i][1]], edges[i][0]);
    }
    int64_t *answer = calloc((size_t)n, sizeof(int64_t));
    free(walk(0, -1, adjacent, labels, answer));
    for (int64_t i = 0; i < n; i++) free(adjacent[i].items);
    free(adjacent);
    return answer;
}

static int64_t seed = 1519;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t n = 200000;
    int64_t (*edges)[2] = malloc((size_t)(n - 1) * sizeof *edges);
    for (int64_t i = 1; i < n; i++) {
        int64_t a = next_random();
        edges[i - 1][0] = (a * 32768 + next_random()) % i;
        edges[i - 1][1] = i;
    }
    char *labels = malloc((size_t)n + 1);
    for (int64_t i = 0; i < n; i++) labels[i] = (char)(97 + next_random() % 26);
    labels[n] = 0;
    int64_t check = 0;
    for (int r = 0; r < 5; r++) {
        int64_t *answer = count_sub_trees(n, (const int64_t (*)[2])edges, labels);
        for (int64_t i = 0; i < n; i++) check = (check * 31 + answer[i] + 1) % 1000000007;
        free(answer);
    }
    printf("5 passes over a tree of 200000 nodes: checksum %lld\n", (long long)check);
    return 0;
}
