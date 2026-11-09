// LeetCode #2049: Count Nodes With the Highest Score -- C mirror of the ★
// arm's benchmark (highest.kara): the same 50 trees of 100000 nodes, the
// same explicit-stack preorder walked backwards. Each node's children are
// a growable array, as a `Vec` is.
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
        l->items = realloc(l->items, l->cap * sizeof(int64_t));
    }
    l->items[l->len++] = x;
}

static int64_t seed = 2049;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static void draw(int64_t n, int64_t reach, int64_t *parents) {
    int64_t *kids = calloc(n, sizeof(int64_t));
    parents[0] = -1;
    for (int64_t i = 1; i < n; i++) {
        int64_t span = reach < i ? reach : i;
        int64_t at = i - (next_random() % span + 1);
        while (kids[at] == 2) at++;
        parents[i] = at;
        kids[at]++;
    }
    free(kids);
}

static int64_t count_highest_score_nodes(const int64_t *parents, int64_t n) {
    List *children = calloc(n, sizeof(List));
    int64_t root = 0;
    for (int64_t v = 0; v < n; v++) {
        if (parents[v] == -1) root = v;
        else push(&children[parents[v]], v);
    }
    List order = {0}, stack = {0};
    push(&stack, root);
    while (stack.len > 0) {
        int64_t v = stack.items[--stack.len];
        push(&order, v);
        for (int64_t k = 0; k < children[v].len; k++) push(&stack, children[v].items[k]);
    }
    int64_t *size = malloc(n * sizeof(int64_t));
    for (int64_t v = 0; v < n; v++) size[v] = 1;
    for (int64_t k = order.len - 1; k >= 0; k--) {
        int64_t v = order.items[k];
        if (parents[v] != -1) size[parents[v]] += size[v];
    }
    int64_t best = 0, count = 0;
    for (int64_t v = 0; v < n; v++) {
        int64_t score = n - size[v] > 1 ? n - size[v] : 1;
        for (int64_t k = 0; k < children[v].len; k++) score *= size[children[v].items[k]];
        if (score > best) {
            best = score;
            count = 1;
        } else if (score == best) {
            count++;
        }
    }
    for (int64_t v = 0; v < n; v++) free(children[v].items);
    free(children);
    free(order.items);
    free(stack.items);
    free(size);
    return count;
}

int main(void) {
    int64_t n = 100000, sum = 0, check = 0;
    int64_t *parents = malloc(n * sizeof(int64_t));
    for (int64_t t = 0; t < 50; t++) {
        draw(n, 1 + t * 1000, parents);
        int64_t count = count_highest_score_nodes(parents, n);
        sum += count;
        check = (check * 31 + count) % 1000000007;
    }
    free(parents);
    printf("50 trees: sum %lld, checksum %lld\n", (long long)sum, (long long)check);
    return 0;
}
