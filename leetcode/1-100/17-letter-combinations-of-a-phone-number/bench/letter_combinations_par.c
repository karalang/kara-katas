/* LeetCode #17 — C pthreads-parallel mirror (par-lane BARE-METAL FLOOR,
 * letter_combinations). Same BFS letter_combinations as the seq C mirror;
 * the K=100k reduction split across a fixed pool of _SC_NPROCESSORS_ONLN
 * pthreads (spawn once, chunk, join+merge). Raw OS threads, no runtime —
 * the ceiling auto-par is measured against. Sink matches the
 * kara/rust/c/go mirrors.
 * Build: clang -O3 letter_combinations_par.c -o … -lpthread */
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <unistd.h>

#define M_CASES 8
#define K_ITERS 100000LL

typedef struct {
    char **items;
    int    count;
} Combos;

static void combos_free(Combos *c) {
    for (int i = 0; i < c->count; i++) free(c->items[i]);
    free(c->items);
}

static Combos letter_combinations(const char *digits) {
    static const char *groups[8] = {
        "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"
    };
    Combos out = {NULL, 0};
    size_t dlen = strlen(digits);
    if (dlen == 0) return out;

    out.items = (char **)malloc(sizeof(char *));
    out.items[0] = (char *)calloc(1, 1);
    out.count = 1;

    for (size_t d = 0; d < dlen; d++) {
        int idx = digits[d] - '2';
        const char *letters = groups[idx];
        int letters_len = (int)strlen(letters);
        int prev_len = out.count;
        int next_cap = prev_len * letters_len;
        Combos next;
        next.items = (char **)malloc(sizeof(char *) * (size_t)next_cap);
        next.count = next_cap;
        int w = 0;
        for (int i = 0; i < prev_len; i++) {
            int plen = (int)strlen(out.items[i]);
            for (int j = 0; j < letters_len; j++) {
                char *s = (char *)malloc((size_t)plen + 2);
                memcpy(s, out.items[i], (size_t)plen);
                s[plen] = letters[j];
                s[plen + 1] = '\0';
                next.items[w++] = s;
            }
        }
        combos_free(&out);
        out = next;
    }
    return out;
}

typedef struct {
    const char **cases;
    int64_t start, end, partial;
} Work;

static void *worker(void *arg) {
    Work *wk = (Work *)arg;
    int64_t s = 0;
    for (int64_t k = wk->start; k < wk->end; k++) {
        int64_t idx = k % M_CASES;
        Combos r = letter_combinations(wk->cases[idx]);
        s += (int64_t)r.count;
        combos_free(&r);
    }
    wk->partial = s;
    return NULL;
}

int main(void) {
    static const char *cases[M_CASES] = {"", "2", "7", "23", "79", "234", "279", "2349"};

    long nworkers = sysconf(_SC_NPROCESSORS_ONLN);
    if (nworkers < 1) {
        nworkers = 1;
    }
    pthread_t *threads = malloc((size_t)nworkers * sizeof(pthread_t));
    Work *works = malloc((size_t)nworkers * sizeof(Work));
    int64_t chunk = K_ITERS / nworkers;
    for (long w = 0; w < nworkers; w++) {
        works[w].cases = cases;
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
    return 0;
}
