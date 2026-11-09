// LeetCode #2045: Second Minimum Time to Reach Destination -- the ★ arm in
// C, the same algorithm and workload as second.kara: a breadth-first search
// keeping each vertex's two smallest walk lengths, then the lights. The
// adjacency is rebuilt every call (degrees counted, then filled), as the
// Kāra arm builds its lists, and the generator's set of edges seen is an
// open-addressing hash set.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t travel(int64_t steps, int64_t time, int64_t change) {
    int64_t t = 0;
    for (int64_t i = 0; i < steps; i++) {
        if (t / change % 2 == 1) t = (t / change + 1) * change;
        t += time;
    }
    return t;
}

static int64_t second_minimum(int64_t n, const int64_t (*edges)[2], int64_t m, int64_t time, int64_t change) {
    int64_t *start = calloc(n + 2, sizeof(int64_t));
    for (int64_t i = 0; i < m; i++) { start[edges[i][0] + 1]++; start[edges[i][1] + 1]++; }
    for (int64_t v = 0; v <= n; v++) start[v + 1] += start[v];
    int64_t *fill = malloc(sizeof(int64_t) * (n + 1));
    memcpy(fill, start, sizeof(int64_t) * (n + 1));
    int64_t *adj = malloc(sizeof(int64_t) * 2 * m);
    for (int64_t i = 0; i < m; i++) {
        adj[fill[edges[i][0]]++] = edges[i][1];
        adj[fill[edges[i][1]]++] = edges[i][0];
    }
    int64_t *first = malloc(sizeof(int64_t) * (n + 1));
    int64_t *second = malloc(sizeof(int64_t) * (n + 1));
    for (int64_t v = 0; v <= n; v++) first[v] = second[v] = -1;
    int64_t *qv = malloc(sizeof(int64_t) * 2 * (n + 1));
    int64_t *qd = malloc(sizeof(int64_t) * 2 * (n + 1));
    int64_t head = 0, tail = 0;
    first[1] = 0;
    qv[tail] = 1; qd[tail++] = 0;
    while (head < tail) {
        int64_t u = qv[head], d = qd[head++];
        for (int64_t k = start[u]; k < start[u + 1]; k++) {
            int64_t v = adj[k];
            if (first[v] == -1) { first[v] = d + 1; qv[tail] = v; qd[tail++] = d + 1; }
            else if (second[v] == -1 && first[v] < d + 1) { second[v] = d + 1; qv[tail] = v; qd[tail++] = d + 1; }
        }
    }
    int64_t answer = travel(second[n], time, change);
    free(start); free(fill); free(adj); free(first); free(second); free(qv); free(qd);
    return answer;
}

static int64_t seed = 2045;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

#define SET_SIZE (1 << 16)
static int64_t set_keys[SET_SIZE];
static int set_has(int64_t key) {
    uint64_t h = (uint64_t)key * 0x9E3779B97F4A7C15ULL >> 48;
    while (set_keys[h] != 0) { if (set_keys[h] == key) return 1; h = (h + 1) & (SET_SIZE - 1); }
    return 0;
}
static void set_add(int64_t key) {
    uint64_t h = (uint64_t)key * 0x9E3779B97F4A7C15ULL >> 48;
    while (set_keys[h] != 0) { if (set_keys[h] == key) return; h = (h + 1) & (SET_SIZE - 1); }
    set_keys[h] = key;
}

static int64_t graph(int64_t n, int64_t reach, int64_t extra, int64_t (*edges)[2]) {
    memset(set_keys, 0, sizeof set_keys);
    int64_t m = 0;
    for (int64_t v = 2; v <= n; v++) {
        int64_t lim = reach < v - 1 ? reach : v - 1;
        int64_t u = v - 1 - next_random() % lim;
        edges[m][0] = u; edges[m][1] = v; m++;
        set_add(u * (n + 1) + v);
    }
    int64_t tries = 0;
    while (m < n - 1 + extra && tries < 4 * extra) {
        tries++;
        int64_t a = next_random() % n + 1;
        int64_t b = next_random() % n + 1;
        int64_t u = a < b ? a : b, v = a < b ? b : a;
        if (u != v && !set_has(u * (n + 1) + v)) {
            set_add(u * (n + 1) + v);
            edges[m][0] = u; edges[m][1] = v; m++;
        }
    }
    return m;
}

int main(void) {
    static int64_t edges[4][20000][2];
    int64_t counts[4];
    const int64_t reaches[4] = {10000, 3, 2, 1};
    for (int r = 0; r < 4; r++) counts[r] = graph(10000, reaches[r], 10001, edges[r]);
    int64_t calls = 0, sum = 0, check = 0;
    for (int64_t round = 0; round < 250; round++) {
        for (int64_t r = 0; r < 4; r++) {
            int64_t time = (round * 7 + r) % 1000 + 1;
            int64_t change = (round * 13 + r * 5) % 1000 + 1;
            int64_t answer = second_minimum(10000, (const int64_t (*)[2])edges[r], counts[r], time, change);
            calls++;
            sum += answer;
            check = (check * 31 + answer) % 1000000007;
        }
    }
    printf("%lld calls: sum %lld, checksum %lld\n", (long long)calls, (long long)sum, (long long)check);
    return 0;
}
