// LeetCode #2246: Longest Path With Different Adjacent Characters -- the
// benchmark's C mirror of path.kara: the child lists in one array by
// offsets (CSR), breadth-first order taken back to front, each node's
// two longest chains through children of another letter.
#include <stdint.h>
#include <stdio.h>

#define N 100000

static int64_t parent[N], start[N + 1], kids[N], fill[N], order[N], down[N];
static char s[N];

static int64_t longest_path(int64_t n) {
    for (int64_t v = 0; v <= n; v++) start[v] = 0;
    for (int64_t v = 1; v < n; v++) start[parent[v] + 1]++;
    for (int64_t v = 0; v < n; v++) start[v + 1] += start[v];
    for (int64_t v = 0; v < n; v++) fill[v] = start[v];
    for (int64_t v = 1; v < n; v++) kids[fill[parent[v]]++] = v;
    int64_t len = 1, next = 0;
    order[0] = 0;
    while (next < len) {
        int64_t v = order[next++];
        for (int64_t k = start[v]; k < start[v + 1]; k++) order[len++] = kids[k];
    }
    int64_t best = 1;
    for (int64_t i = n - 1; i >= 0; i--) {
        int64_t v = order[i], first = 0, second = 0;
        for (int64_t k = start[v]; k < start[v + 1]; k++) {
            int64_t c = kids[k];
            if (s[c] == s[v]) continue;
            if (down[c] > first) {
                second = first;
                first = down[c];
            } else if (down[c] > second) {
                second = down[c];
            }
        }
        down[v] = first + 1;
        if (first + second + 1 > best) best = first + second + 1;
    }
    return best;
}

static int64_t seed = 2246;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide_random(void) {
    int64_t high = next_random();
    return high * 32768 + next_random();
}

int main(void) {
    int64_t check = 0;
    for (int t = 0; t < 40; t++) {
        parent[0] = -1;
        for (int64_t v = 1; v < N; v++) parent[v] = wide_random() % v;
        for (int64_t v = 0; v < N; v++) s[v] = (char)('a' + next_random() % 26);
        check = (check * 31 + longest_path(N)) % 1000000007;
    }
    printf("40 trees of 100000 nodes: checksum %lld\n", (long long)check);
    return 0;
}
