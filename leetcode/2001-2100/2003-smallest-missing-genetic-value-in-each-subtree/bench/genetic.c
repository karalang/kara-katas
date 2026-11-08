// LeetCode #2003: Smallest Missing Genetic Value in Each Subtree -- the
// benchmark's C twin, the same algorithm as genetic.kara here. Children as
// growable arrays per node, allocated per call as the Kāra program does.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct { int64_t *a; int64_t len, cap; } Vec;

static void push(Vec *v, int64_t x) {
    if (v->len == v->cap) {
        v->cap = v->cap ? v->cap * 2 : 4;
        v->a = realloc(v->a, v->cap * sizeof(int64_t));
    }
    v->a[v->len++] = x;
}

static void mark(int64_t u, const Vec *children, const int64_t *nums, bool *seen, int64_t seen_len, bool *visited) {
    visited[u] = true;
    if (nums[u] < seen_len) seen[nums[u]] = true;
    for (int64_t k = 0; k < children[u].len; k++) {
        int64_t c = children[u].a[k];
        if (!visited[c]) mark(c, children, nums, seen, seen_len, visited);
    }
}

static int64_t *smallest_missing(const int64_t *parents, const int64_t *nums, int64_t n) {
    int64_t *answer = malloc(n * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) answer[i] = 1;
    int64_t one = -1;
    for (int64_t i = 0; i < n; i++) if (nums[i] == 1) { one = i; break; }
    if (one == -1) return answer;
    Vec *children = calloc(n, sizeof(Vec));
    for (int64_t i = 1; i < n; i++) push(&children[parents[i]], i);
    bool *seen = calloc(n + 2, 1);
    bool *visited = calloc(n, 1);
    int64_t missing = 1;
    for (int64_t u = one; u != -1; u = parents[u]) {
        mark(u, children, nums, seen, n + 2, visited);
        while (seen[missing]) missing++;
        answer[u] = missing;
    }
    for (int64_t i = 0; i < n; i++) free(children[i].a);
    free(children);
    free(seen);
    free(visited);
    return answer;
}

static int64_t seed = 2003;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    // 40 trees of 20000 nodes built once, then the ★ arm on each, 25 rounds
    enum { T = 40, N = 20000 };
    static int64_t parents[T][N], nums[T][N];
    static int64_t values[N + 1];
    const int64_t widths[4] = {2, 5, 50, 20000};
    for (int a = 0; a < T; a++) {
        int64_t width = widths[a % 4], extra = a % 2;
        parents[a][0] = -1;
        for (int64_t i = 1; i < N; i++) {
            int64_t lo = i - width > 0 ? i - width : 0;
            parents[a][i] = lo + next_random() % (i - lo);
        }
        int64_t m = N + extra;
        for (int64_t i = 0; i < m; i++) values[i] = i + 1;
        for (int64_t i = m - 1; i >= 1; i--) {
            int64_t j = next_random() % (i + 1);
            int64_t t = values[i]; values[i] = values[j]; values[j] = t;
        }
        for (int64_t i = 0; i < N; i++) nums[a][i] = values[i];
    }
    int64_t calls = 0, sum = 0, check = 0;
    for (int r = 0; r < 25; r++) {
        for (int a = 0; a < T; a++) {
            int64_t *answer = smallest_missing(parents[a], nums[a], N);
            calls++;
            for (int64_t i = 0; i < N; i++) {
                sum += answer[i];
                check = (check * 31 + answer[i]) % 1000000007;
            }
            free(answer);
        }
    }
    printf("%lld calls: sum %lld, checksum %lld\n", (long long)calls, (long long)sum, (long long)check);
    return 0;
}
