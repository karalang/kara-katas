// LeetCode #2440: Create Components With Same Value -- the bench, the ★
// arm: each component count dividing the total, from `n` down, checked by
// gathering subtree sums in reverse breadth-first order. The adjacency is
// a list per node grown by doubling, as the other languages' vectors are.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t *items;
    int64_t len, cap;
} List;

static void push(List *l, int64_t v) {
    if (l->len == l->cap) {
        l->cap = l->cap ? l->cap * 2 : 4;
        l->items = realloc(l->items, l->cap * sizeof(int64_t));
    }
    l->items[l->len++] = v;
}

static bool fits(const int64_t *order, const int64_t *parent, const int64_t *nums, int64_t n, int64_t target) {
    int64_t *sum = malloc(n * sizeof(int64_t));
    memcpy(sum, nums, n * sizeof(int64_t));
    bool ok = true;
    for (int64_t i = n; i > 0;) {
        i--;
        int64_t u = order[i];
        if (sum[u] > target) { ok = false; break; }
        if (sum[u] < target) {
            if (u == 0) { ok = false; break; }
            sum[parent[u]] += sum[u];
        }
    }
    free(sum);
    return ok;
}

static int64_t component_value(const int64_t *nums, int64_t n, int64_t (*edges)[2], int64_t m) {
    List *adjacent = calloc(n, sizeof(List));
    for (int64_t j = 0; j < m; j++) {
        push(&adjacent[edges[j][0]], edges[j][1]);
        push(&adjacent[edges[j][1]], edges[j][0]);
    }
    int64_t *parent = malloc(n * sizeof(int64_t));
    int64_t *order = malloc(n * sizeof(int64_t));
    bool *seen = calloc(n, sizeof(bool));
    for (int64_t i = 0; i < n; i++) parent[i] = -1;
    int64_t len = 1, head = 0;
    order[0] = 0;
    seen[0] = true;
    while (head < len) {
        int64_t u = order[head++];
        for (int64_t j = 0; j < adjacent[u].len; j++) {
            int64_t v = adjacent[u].items[j];
            if (!seen[v]) {
                seen[v] = true;
                parent[v] = u;
                order[len++] = v;
            }
        }
    }
    int64_t total = 0;
    for (int64_t i = 0; i < n; i++) total += nums[i];
    int64_t answer = 0;
    for (int64_t k = n; k > 1; k--)
        if (total % k == 0 && fits(order, parent, nums, n, total / k)) {
            answer = k - 1;
            break;
        }
    for (int64_t i = 0; i < n; i++) free(adjacent[i].items);
    free(adjacent);
    free(parent);
    free(order);
    free(seen);
    return answer;
}

static int64_t seed = 2440;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int64_t n = 20000;
    int64_t (*trees[10])[2];
    int64_t *values[10];
    for (int c = 0; c < 10; c++) {
        trees[c] = malloc((n - 1) * sizeof(int64_t[2]));
        for (int64_t i = 1; i < n; i++) {
            trees[c][i - 1][0] = next_random() % i;
            trees[c][i - 1][1] = i;
        }
        values[c] = malloc(n * sizeof(int64_t));
        for (int64_t i = 0; i < n; i++) values[c][i] = 1 + next_random() % 50;
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 50; p++)
        for (int64_t c = 0; c < 10; c++) {
            int64_t at = (p * 7919 + c * 104729) % n;
            values[c][at] = 1 + next_random() % 50;
            check = (check * 31 + component_value(values[c], n, trees[c], n - 1) + p) % 1000000007;
        }
    printf("50 passes over 10 trees of 2 * 10^4 nodes: checksum %lld\n", (long long)check);
    for (int c = 0; c < 10; c++) {
        free(trees[c]);
        free(values[c]);
    }
    return 0;
}
