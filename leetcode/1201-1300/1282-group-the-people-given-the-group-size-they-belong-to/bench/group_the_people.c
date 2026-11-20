// LeetCode #1282 bench, in C: the ★ arm (one open group per size, handed
// out when full) on 50 problems of 10000 people, built once, 500 rounds,
// every group folded into a checksum.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct { int64_t *v; int64_t len, cap; } Vec;

static void push(Vec *a, int64_t x) {
    if (a->len == a->cap) {
        a->cap = a->cap ? a->cap * 2 : 4;
        a->v = realloc(a->v, a->cap * sizeof(int64_t));
    }
    a->v[a->len++] = x;
}

typedef struct { Vec *g; int64_t len, cap; } Groups;

static Groups group_the_people(const int64_t *sizes, int64_t n) {
    Vec *open = calloc(n + 1, sizeof(Vec));
    Groups out = {0, 0, 0};
    for (int64_t person = 0; person < n; person++) {
        int64_t size = sizes[person];
        push(&open[size], person);
        if (open[size].len == size) {
            Vec copy = {malloc(size * sizeof(int64_t)), size, size};
            memcpy(copy.v, open[size].v, size * sizeof(int64_t));
            if (out.len == out.cap) {
                out.cap = out.cap ? out.cap * 2 : 4;
                out.g = realloc(out.g, out.cap * sizeof(Vec));
            }
            out.g[out.len++] = copy;
            open[size].len = 0;
        }
    }
    for (int64_t s = 0; s <= n; s++) free(open[s].v);
    free(open);
    return out;
}

static int64_t seed;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t *problem(int64_t n) {
    int64_t *sizes = malloc(n * sizeof(int64_t)), len = 0;
    while (len < n) {
        int64_t left = n - len;
        int64_t cap = next_random() % 4 == 0 ? (left < 1000 ? left : 1000) : (left < 8 ? left : 8);
        int64_t s = next_random() % cap + 1;
        for (int64_t k = 0; k < s; k++) sizes[len++] = s;
    }
    for (int64_t i = n - 1; i > 0; i--) {
        int64_t j = next_random() % (i + 1);
        int64_t t = sizes[i]; sizes[i] = sizes[j]; sizes[j] = t;
    }
    return sizes;
}

int main(void) {
    seed = 1282;
    int64_t *problems[50];
    for (int k = 0; k < 50; k++) problems[k] = problem(10000);
    int64_t check = 0;
    for (int64_t round = 0; round < 500; round++) {
        for (int k = 0; k < 50; k++) {
            Groups gs = group_the_people(problems[k], 10000);
            for (int64_t i = 0; i < gs.len; i++) {
                for (int64_t j = 0; j < gs.g[i].len; j++)
                    check = (check * 131 + gs.g[i].v[j] + round) % 1000000007;
                check = (check * 131 + 7) % 1000000007;
                free(gs.g[i].v);
            }
            free(gs.g);
        }
    }
    printf("500 rounds of 50 problems of 10000 people: checksum %lld\n", (long long)check);
    return 0;
}
