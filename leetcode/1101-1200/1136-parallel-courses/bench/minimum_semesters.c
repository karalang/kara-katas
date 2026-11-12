// LeetCode #1136: Parallel Courses -- the bench, the ★ arm's algorithm:
// Kahn's algorithm a semester at a time.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t *p;
    int64_t len, cap;
} Vec;

static void push(Vec *v, int64_t x) {
    if (v->len == v->cap) {
        v->cap = v->cap ? v->cap * 2 : 4;
        v->p = realloc(v->p, v->cap * sizeof(int64_t));
    }
    v->p[v->len++] = x;
}

static int64_t minimum_semesters(int64_t n, int64_t **relations, int64_t m) {
    Vec *after = calloc(n + 1, sizeof(Vec));
    int64_t *need = calloc(n + 1, sizeof(int64_t));
    for (int64_t i = 0; i < m; i++) {
        push(&after[relations[i][0]], relations[i][1]);
        need[relations[i][1]] += 1;
    }
    Vec now = {0};
    for (int64_t c = 1; c <= n; c++)
        if (need[c] == 0) push(&now, c);
    int64_t semesters = 0, taken = 0;
    while (now.len > 0) {
        semesters += 1;
        taken += now.len;
        Vec upcoming = {0};
        for (int64_t i = 0; i < now.len; i++) {
            Vec *a = &after[now.p[i]];
            for (int64_t k = 0; k < a->len; k++) {
                int64_t d = a->p[k];
                need[d] -= 1;
                if (need[d] == 0) push(&upcoming, d);
            }
        }
        free(now.p);
        now = upcoming;
    }
    free(now.p);
    for (int64_t c = 0; c <= n; c++) free(after[c].p);
    free(after);
    free(need);
    return taken == n ? semesters : -1;
}

static int64_t seed = 1136;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t n = 5000, m = n - 1;
    int64_t **plans[8];
    for (int j = 0; j < 8; j++) {
        plans[j] = malloc(m * sizeof(int64_t *));
        for (int64_t c = 2; c <= n; c++) {
            int64_t *r = malloc(2 * sizeof(int64_t));
            r[0] = next_random() % (c - 1) + 1;
            r[1] = c;
            plans[j][c - 2] = r;
        }
    }
    int64_t total = 0, check = 0;
    for (int64_t round = 0; round < 300; round++) {
        for (int64_t j = 0; j < 8; j++) {
            int64_t at = (round * 7919 + j * 104729) % (n - 1);
            int64_t c = plans[j][at][1];
            plans[j][at][0] = next_random() % (c - 1) + 1;
            int64_t r = minimum_semesters(n, plans[j], m);
            total += r;
            check = (check * 31 + r + 1) % 1000000007;
        }
    }
    printf("300 rounds over 8 plans of 5000 courses and 4999 relations: semesters total %lld, checksum %lld\n",
           (long long)total, (long long)check);
    return 0;
}
