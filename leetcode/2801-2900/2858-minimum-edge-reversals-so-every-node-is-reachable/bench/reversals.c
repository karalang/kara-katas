// LeetCode #2858: Minimum Edge Reversals So Every Node Is Reachable --
// the bench: the ★ arm over 20 random trees of 10^5 nodes, LeetCode's
// most, every other one deep, labels shuffled and each edge pointing
// either way, all drawn first, then each answered 5 times.
// C builds each call's adjacency as one array of neighbours indexed by
// offsets (compressed rows) where the others keep a vector per node.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static void min_edge_reversals(int64_t n, const int64_t *eu, const int64_t *ev, int64_t *answer) {
    int64_t *start = calloc(n + 1, sizeof(int64_t));
    int64_t *to = malloc(sizeof(int64_t) * 2 * (n - 1)), *wt = malloc(sizeof(int64_t) * 2 * (n - 1));
    for (int64_t i = 0; i < n - 1; i++) {
        start[eu[i] + 1]++;
        start[ev[i] + 1]++;
    }
    for (int64_t i = 0; i < n; i++) start[i + 1] += start[i];
    int64_t *fill = malloc(sizeof(int64_t) * n);
    for (int64_t i = 0; i < n; i++) fill[i] = start[i];
    for (int64_t i = 0; i < n - 1; i++) {
        to[fill[eu[i]]] = ev[i];
        wt[fill[eu[i]]++] = 0;
        to[fill[ev[i]]] = eu[i];
        wt[fill[ev[i]]++] = 1;
    }
    int64_t *parent = malloc(sizeof(int64_t) * n), *cost = calloc(n, sizeof(int64_t));
    int64_t *order = malloc(sizeof(int64_t) * n), *stack = malloc(sizeof(int64_t) * n);
    for (int64_t i = 0; i < n; i++) parent[i] = -1;
    int64_t top = 0, len = 0, root = 0;
    stack[top++] = 0;
    parent[0] = 0;
    while (top > 0) {
        int64_t u = stack[--top];
        order[len++] = u;
        for (int64_t j = start[u]; j < start[u + 1]; j++) {
            int64_t v = to[j];
            if (parent[v] == -1) {
                parent[v] = u;
                cost[v] = wt[j];
                root += wt[j];
                stack[top++] = v;
            }
        }
    }
    answer[0] = root;
    for (int64_t i = 1; i < len; i++) {
        int64_t u = order[i];
        answer[u] = answer[parent[u]] + (cost[u] == 0 ? 1 : -1);
    }
    free(start); free(to); free(wt); free(fill); free(parent); free(cost); free(order); free(stack);
}

static int64_t seed = 2858;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}
static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

static void tree(int64_t n, int deep, int64_t *eu, int64_t *ev) {
    int64_t *label = malloc(sizeof(int64_t) * n);
    for (int64_t i = 0; i < n; i++) label[i] = i;
    for (int64_t i = n - 1; i >= 1; i--) {
        int64_t j = wide() % (i + 1);
        int64_t t = label[i];
        label[i] = label[j];
        label[j] = t;
    }
    for (int64_t i = 1; i < n; i++) {
        int64_t p = deep ? i - 1 - next_random() % (i < 3 ? i : 3) : wide() % i;
        if (next_random() % 2 == 0) {
            eu[i - 1] = label[p];
            ev[i - 1] = label[i];
        } else {
            eu[i - 1] = label[i];
            ev[i - 1] = label[p];
        }
    }
    free(label);
}

int main(void) {
    const int64_t count = 20, rounds = 5, n = 100000;
    int64_t *eu = malloc(sizeof(int64_t) * count * (n - 1)), *ev = malloc(sizeof(int64_t) * count * (n - 1));
    for (int64_t c = 0; c < count; c++) tree(n, c % 2 == 1, eu + c * (n - 1), ev + c * (n - 1));
    int64_t *answer = malloc(sizeof(int64_t) * n);
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t c = 0; c < count; c++) {
            min_edge_reversals(n, eu + c * (n - 1), ev + c * (n - 1), answer);
            for (int64_t i = 0; i < n; i++) {
                total += answer[i];
                check = (check * 31 + answer[i] + r) % 1000000007;
            }
        }
    }
    printf("%lld trees of %lld, %lld rounds: answers sum to %lld, checksum %lld\n", (long long)count, (long long)n, (long long)rounds, (long long)total, (long long)check);
    free(eu);
    free(ev);
    free(answer);
    return 0;
}
