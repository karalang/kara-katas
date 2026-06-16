/* LeetCode #22 — C pthreads-parallel mirror (par-lane BARE-METAL FLOOR, backtracking).
 * Same owned-snapshot recursive backtracking (each child malloc's a copy of the
 * prefix plus one bracket; strings materialized into a growing pointer array and
 * fully freed each iter); the K=150 iter reduction split across a fixed pool of
 * _SC_NPROCESSORS_ONLN pthreads (spawn once, chunk, join+merge). Raw OS threads,
 * no runtime — the ceiling auto-par is measured against. Sink matches the
 * kara/rust/c/go mirrors (50,388,000).
 * Build: clang -O3 backtracking_par.c -o … -lpthread */
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <unistd.h>

#define N 10
#define ITERS 150

typedef struct {
    char **data;
    size_t len;
    size_t cap;
} StrVec;

static void sv_push(StrVec *v, char *s) {
    if (v->len == v->cap) {
        v->cap = v->cap ? v->cap * 2 : 4;
        v->data = realloc(v->data, v->cap * sizeof(char *));
    }
    v->data[v->len++] = s;
}

static void backtrack(char *cur, size_t cur_len, long open, long close, long n, StrVec *out) {
    if (close == n) {
        sv_push(out, cur);
        return;
    }
    if (open < n) {
        char *child = malloc(cur_len + 2);
        memcpy(child, cur, cur_len);
        child[cur_len] = '(';
        child[cur_len + 1] = '\0';
        backtrack(child, cur_len + 1, open + 1, close, n, out);
    }
    if (close < open) {
        char *child = malloc(cur_len + 2);
        memcpy(child, cur, cur_len);
        child[cur_len] = ')';
        child[cur_len + 1] = '\0';
        backtrack(child, cur_len + 1, open, close + 1, n, out);
    }
    free(cur);
}

static StrVec generate_parenthesis(long n) {
    StrVec out = {0};
    char *root = malloc(1);
    root[0] = '\0';
    backtrack(root, 0, 0, 0, n, &out);
    return out;
}

typedef struct {
    long start, end;
    uint64_t partial;
} Work;

static void *worker(void *arg) {
    Work *wk = (Work *)arg;
    uint64_t s = 0;
    for (long k = wk->start; k < wk->end; k++) {
        StrVec combos = generate_parenthesis(N);
        uint64_t bytes = 0;
        for (size_t j = 0; j < combos.len; j++) {
            bytes += strlen(combos.data[j]);
            free(combos.data[j]);
        }
        free(combos.data);
        s += bytes;
    }
    wk->partial = s;
    return NULL;
}

int main(void) {
    long nworkers = sysconf(_SC_NPROCESSORS_ONLN);
    if (nworkers < 1) {
        nworkers = 1;
    }
    if (nworkers > ITERS) {
        nworkers = ITERS;
    }
    pthread_t *threads = malloc((size_t)nworkers * sizeof(pthread_t));
    Work *works = malloc((size_t)nworkers * sizeof(Work));
    long chunk = ITERS / nworkers;
    for (long w = 0; w < nworkers; w++) {
        works[w].start = w * chunk;
        works[w].end = (w == nworkers - 1) ? ITERS : (w + 1) * chunk;
        works[w].partial = 0;
        pthread_create(&threads[w], NULL, worker, &works[w]);
    }
    uint64_t total = 0;
    for (long w = 0; w < nworkers; w++) {
        pthread_join(threads[w], NULL);
        total += works[w].partial;
    }
    printf("%llu\n", (unsigned long long)total); // 50,388,000
    free(threads);
    free(works);
    return 0;
}
