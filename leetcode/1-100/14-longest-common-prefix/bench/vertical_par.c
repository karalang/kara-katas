/* LeetCode #14 — C pthreads-parallel mirror (par-lane BARE-METAL FLOOR, vertical LCP).
 * Same vertical-scan longest_common_prefix as ../vertical.c; the K=1M reduction
 * split across a fixed pool of _SC_NPROCESSORS_ONLN pthreads (spawn once, chunk,
 * join+merge). Raw OS threads, no runtime — the ceiling auto-par is measured
 * against. Sink matches the kara/rust/c/go mirrors.
 * Build: clang -O3 -pthread vertical_par.c -o … */
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <unistd.h>

#define M_CASES 8
#define N_STRINGS 16
#define K_ITERS 1000000LL

typedef struct {
    char **items;
    int   *lens;
    int    count;
} Strs;

static char nth_letter(int64_t n) {
    const char *alphabet = "abcdefghijklmnopqrstuvwxyz";
    return alphabet[n % 26];
}

static char *make_string(int64_t prefix_len, int64_t suffix_id, int *out_len) {
    const char *alphabet = "abcdefghijklmnopqrstuvwxyz";
    int len = (int)prefix_len + 6;
    char *out = (char *)malloc((size_t)len + 1);
    int p = 0;
    for (int64_t i = 0; i < prefix_len; i++) out[p++] = alphabet[i];
    char sig = nth_letter(suffix_id);
    for (int j = 0; j < 6; j++) out[p++] = sig;
    out[p] = '\0';
    *out_len = len;
    return out;
}

static Strs build_case(int64_t prefix_len, int64_t count) {
    Strs v;
    v.count = (int)count;
    v.items = (char **)malloc(sizeof(char *) * (size_t)count);
    v.lens  = (int *)malloc(sizeof(int) * (size_t)count);
    for (int64_t s = 0; s < count; s++) {
        int len;
        v.items[s] = make_string(prefix_len, s, &len);
        v.lens[s]  = len;
    }
    return v;
}

static int64_t longest_common_prefix(const Strs *strs) {
    int n = strs->count;
    if (n == 0) return 0;
    const char *first = strs->items[0];
    int first_len = strs->lens[0];
    int col = 0;
    while (col < first_len) {
        char c = first[col];
        int s = 1;
        int stop = 0;
        for (; s < n; s++) {
            if (col >= strs->lens[s] || strs->items[s][col] != c) { stop = 1; break; }
        }
        if (stop) break;
        col++;
    }
    char *prefix = (char *)malloc((size_t)col + 1);
    memcpy(prefix, first, (size_t)col);
    prefix[col] = '\0';
    int64_t len = (int64_t)strlen(prefix);
    free(prefix);
    return len;
}

typedef struct {
    const Strs *sets;
    int64_t start, end, partial;
} Work;

static void *worker(void *arg) {
    Work *wk = (Work *)arg;
    int64_t s = 0;
    for (int64_t k = wk->start; k < wk->end; k++) {
        int64_t idx = k % M_CASES;
        s += longest_common_prefix(&wk->sets[idx]);
    }
    wk->partial = s;
    return NULL;
}

int main(void) {
    const int64_t prefixes[M_CASES] = {0, 2, 4, 7, 10, 13, 16, 20};

    Strs *sets = (Strs *)malloc(sizeof(Strs) * (size_t)M_CASES);
    for (int64_t m = 0; m < M_CASES; m++) {
        sets[m] = build_case(prefixes[m], N_STRINGS);
    }

    long nworkers = sysconf(_SC_NPROCESSORS_ONLN);
    if (nworkers < 1) {
        nworkers = 1;
    }
    pthread_t *threads = malloc((size_t)nworkers * sizeof(pthread_t));
    Work *works = malloc((size_t)nworkers * sizeof(Work));
    int64_t chunk = K_ITERS / nworkers;
    for (long w = 0; w < nworkers; w++) {
        works[w].sets = sets;
        works[w].start = (int64_t)w * chunk;
        works[w].end = (w == nworkers - 1) ? K_ITERS : ((int64_t)w + 1) * chunk;
        works[w].partial = 0;
        pthread_create(&threads[w], NULL, worker, &works[w]);
    }
    int64_t total = 0;
    for (long w = 0; w < nworkers; w++) {
        pthread_join(threads[w], NULL);
        total += works[w].partial;
    }
    printf("%lld\n", (long long)total);
    free(threads);
    free(works);
    free(sets);
    return 0;
}
