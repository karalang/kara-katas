/* LeetCode #71 — C pthreads-parallel mirror (par-lane BARE-METAL FLOOR, simplify).
 * Same one-pass simplify; the K=1M reduction split across a fixed pool of
 * _SC_NPROCESSORS_ONLN pthreads (spawn once, chunk, join+merge). Raw OS
 * threads, no runtime — the ceiling auto-par is measured against. Sink (sum of
 * simplified-output lengths) matches the kara/rust/c/go mirrors.
 * Build: clang -O3 simplify_par.c -o … -lpthread */
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>

#define N 8
#define K_ITERS 1000000LL
#define MAX_LEN 64
#define MAX_COMPS 32

static const char *inputs[N] = {
    "/home/",
    "/home/user/Documents/../Pictures",
    "/.../a/../b/c/../d/./",
    "/a/b/c/../..",
    "/a//b////c/d//././/..",
    "/abc_123",
    "/a/b/../c/../../d",
    "/...hidden",
};

static int64_t simplify(const char *s, char *out) {
    int64_t n = (int64_t)strlen(s);

    int64_t starts[MAX_COMPS];
    int64_t ends[MAX_COMPS];
    int64_t top = 0;

    int64_t i = 0;
    while (i < n) {
        while (i < n && s[i] == '/') i++;
        if (i >= n) break;
        int64_t j = i;
        while (j < n && s[j] != '/') j++;
        int64_t len = j - i;

        int is_dot    = (len == 1) && s[i] == '.';
        int is_dotdot = (len == 2) && s[i] == '.' && s[i + 1] == '.';

        if (is_dot) {
            // skip
        } else if (is_dotdot) {
            if (top > 0) top--;
        } else {
            starts[top] = i;
            ends[top] = j;
            top++;
        }
        i = j;
    }

    if (top == 0) {
        out[0] = '/';
        out[1] = '\0';
        return 1;
    }

    int64_t pos = 0;
    for (int64_t k = 0; k < top; k++) {
        out[pos++] = '/';
        int64_t a = starts[k];
        int64_t b = ends[k];
        for (int64_t p = a; p < b; p++) {
            out[pos++] = s[p];
        }
    }
    out[pos] = '\0';
    return pos;
}

typedef struct {
    int64_t start, end, partial;
} Work;

static void *worker(void *arg) {
    Work *wk = (Work *)arg;
    char out[MAX_LEN];
    int64_t s = 0;
    for (int64_t k = wk->start; k < wk->end; k++) {
        s += simplify(inputs[k % N], out);
    }
    wk->partial = s;
    return NULL;
}

int main(void) {
    long nworkers = sysconf(_SC_NPROCESSORS_ONLN);
    if (nworkers < 1) {
        nworkers = 1;
    }
    pthread_t *threads = malloc((size_t)nworkers * sizeof(pthread_t));
    Work *works = malloc((size_t)nworkers * sizeof(Work));
    int64_t chunk = K_ITERS / nworkers;
    for (long w = 0; w < nworkers; w++) {
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
