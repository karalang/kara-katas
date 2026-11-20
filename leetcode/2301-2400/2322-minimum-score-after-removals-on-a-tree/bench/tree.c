// LeetCode #2322: Minimum Score After Removals on a Tree -- the bench, the
// ★ arm in C. Rooted at 0, two removals are two nodes other than the
// root; one walk gives each subtree's XOR and each node's entry and exit
// times, and the three parts follow from whether one node is the other's
// ancestor. O(n^2). The neighbours are kept as growable arrays, as the
// others keep a list per node.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t *items;
    int64_t len, cap;
} List;

static void push(List *l, int64_t v) {
    if (l->len == l->cap) {
        l->cap = l->cap ? 2 * l->cap : 4;
        l->items = realloc(l->items, l->cap * sizeof(int64_t));
    }
    l->items[l->len++] = v;
}

static void visit(int64_t node, int64_t parent, List *adjacent, const int64_t *nums, int64_t *xor, int64_t *enter, int64_t *leave, int64_t *clock) {
    enter[node] = *clock;
    *clock += 1;
    xor[node] = nums[node];
    for (int64_t k = 0; k < adjacent[node].len; k++) {
        int64_t next = adjacent[node].items[k];
        if (next != parent) {
            visit(next, node, adjacent, nums, xor, enter, leave, clock);
            xor[node] ^= xor[next];
        }
    }
    leave[node] = *clock;
}

static int64_t max3(int64_t x, int64_t y, int64_t z) { int64_t m = x > y ? x : y; return m > z ? m : z; }
static int64_t min3(int64_t x, int64_t y, int64_t z) { int64_t m = x < y ? x : y; return m < z ? m : z; }

static int64_t minimum_score(const int64_t *nums, const int64_t (*edges)[2], int64_t n) {
    List *adjacent = calloc(n, sizeof(List));
    for (int64_t e = 0; e < n - 1; e++) {
        push(&adjacent[edges[e][0]], edges[e][1]);
        push(&adjacent[edges[e][1]], edges[e][0]);
    }
    int64_t *xor = calloc(n, sizeof(int64_t)), *enter = calloc(n, sizeof(int64_t)), *leave = calloc(n, sizeof(int64_t));
    int64_t clock = 0;
    visit(0, -1, adjacent, nums, xor, enter, leave, &clock);
    int64_t whole = xor[0];
    int64_t best = INT64_MAX;
    for (int64_t a = 1; a < n; a++)
        for (int64_t b = a + 1; b < n; b++) {
            int64_t x, y, z;
            if (enter[a] <= enter[b] && leave[b] <= leave[a]) {
                x = xor[b]; y = xor[a] ^ xor[b]; z = whole ^ xor[a];
            } else if (enter[b] <= enter[a] && leave[a] <= leave[b]) {
                x = xor[a]; y = xor[b] ^ xor[a]; z = whole ^ xor[b];
            } else {
                x = xor[a]; y = xor[b]; z = whole ^ xor[a] ^ xor[b];
            }
            int64_t s = max3(x, y, z) - min3(x, y, z);
            if (s < best)
                best = s;
        }
    for (int64_t i = 0; i < n; i++)
        free(adjacent[i].items);
    free(adjacent);
    free(xor);
    free(enter);
    free(leave);
    return best;
}

static int64_t seed = 2322;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t n = 1000;
    static int64_t values[10][1000];
    static int64_t shapes[10][999][2];
    for (int k = 0; k < 10; k++) {
        for (int64_t i = 0; i < n; i++)
            values[k][i] = next_random() % 100000000 + 1;
        for (int64_t i = 1; i < n; i++) {
            shapes[k][i - 1][0] = next_random() % i;
            shapes[k][i - 1][1] = i;
        }
    }
    int64_t check = 0;
    for (int p = 0; p < 30; p++)
        for (int k = 0; k < 10; k++) {
            int64_t i = next_random() % n;
            values[k][i] = next_random() % 100000000 + 1;
            check = (check * 31 + minimum_score(values[k], (const int64_t (*)[2])shapes[k], n)) % 1000000007;
        }
    printf("30 passes over 10 trees of 1000 nodes: checksum %lld\n", (long long)check);
    return 0;
}
