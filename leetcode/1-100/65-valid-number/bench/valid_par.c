/* LeetCode #65 — C pthreads-parallel mirror (par-lane BARE-METAL FLOOR, valid).
 * Same 8-state DFA is_number; the K=10M reduction split across a fixed pool of
 * _SC_NPROCESSORS_ONLN pthreads (spawn once, chunk, join+merge). Raw OS
 * threads, no runtime — the ceiling auto-par is measured against. Sink matches
 * the kara/rust/c/go mirrors.
 * Build: clang -O3 -pthread valid_par.c -o … */
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>

#define N 8
#define K_ITERS 10000000LL

static int32_t categorize(unsigned char b) {
    if (b >= '0' && b <= '9') return 0;
    if (b == '+' || b == '-') return 1;
    if (b == '.')             return 2;
    if (b == 'e' || b == 'E') return 3;
    return 4;
}

static int is_number(const char *s) {
    size_t n = strlen(s);

    int32_t state = 0;
    for (size_t i = 0; i < n; i++) {
        int32_t cat = categorize((unsigned char)s[i]);

        if (state == 0) {
            switch (cat) {
                case 0: state = 2; break;
                case 1: state = 1; break;
                case 2: state = 3; break;
                default: return 0;
            }
        } else if (state == 1) {
            switch (cat) {
                case 0: state = 2; break;
                case 2: state = 3; break;
                default: return 0;
            }
        } else if (state == 2) {
            switch (cat) {
                case 0: state = 2; break;
                case 2: state = 4; break;
                case 3: state = 6; break;
                default: return 0;
            }
        } else if (state == 3) {
            switch (cat) {
                case 0: state = 5; break;
                default: return 0;
            }
        } else if (state == 4) {
            switch (cat) {
                case 0: state = 5; break;
                case 3: state = 6; break;
                default: return 0;
            }
        } else if (state == 5) {
            switch (cat) {
                case 0: state = 5; break;
                case 3: state = 6; break;
                default: return 0;
            }
        } else if (state == 6) {
            switch (cat) {
                case 0: state = 8; break;
                case 1: state = 7; break;
                default: return 0;
            }
        } else if (state == 7) {
            switch (cat) {
                case 0: state = 8; break;
                default: return 0;
            }
        } else if (state == 8) {
            switch (cat) {
                case 0: state = 8; break;
                default: return 0;
            }
        } else {
            return 0;
        }
    }

    return state == 2 || state == 4 || state == 5 || state == 8;
}

static const char *inputs[8] = {
    "0",
    "-.9",
    "53.5e93",
    "+6e-1",
    "abc",
    "1e",
    "99e2.5",
    "-123.456e789",
};

typedef struct {
    int64_t start, end, partial;
} Work;

static void *worker(void *arg) {
    Work *wk = (Work *)arg;
    int64_t s = 0;
    for (int64_t k = wk->start; k < wk->end; k++) {
        int64_t idx = k % N;
        if (is_number(inputs[idx])) {
            s += 1;
        }
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
