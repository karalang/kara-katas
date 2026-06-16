/* LeetCode #9 — C pthreads-parallel mirror (par-lane BARE-METAL FLOOR, palindrome).
 * Same half-reverse is_palindrome; the K=50M reduction split across a fixed pool
 * of _SC_NPROCESSORS_ONLN pthreads (spawn once, chunk, join+merge). Raw OS
 * threads, no runtime — the ceiling auto-par is measured against. Sink matches
 * the kara/rust/c/go mirrors.
 * Build: clang -O3 palindrome_par.c -o … -lpthread */
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>

#define N 1024
#define K_ITERS 50000000LL

static int is_palindrome(int32_t x) {
    if (x < 0 || (x % 10 == 0 && x != 0)) {
        return 0;
    }
    int32_t reversed = 0;
    while (x > reversed) {
        reversed = reversed * 10 + x % 10;
        x /= 10;
    }
    return (x == reversed) || (x == reversed / 10);
}

static int32_t manufacture_palindrome(int32_t v32) {
    int32_t lo = v32 < 0 ? -v32 : v32;
    int32_t four_raw = lo % 10000;
    int32_t four = four_raw < 1000 ? four_raw + 1000 : four_raw;
    int32_t d0 = four % 10;
    int32_t d1 = (four / 10) % 10;
    int32_t d2 = (four / 100) % 10;
    int32_t d3 = (four / 1000) % 10;
    int32_t rev = d0 * 1000 + d1 * 100 + d2 * 10 + d3;
    return four * 10000 + rev;
}

typedef struct {
    const int32_t *inputs;
    int64_t start, end, partial;
} Work;

static void *worker(void *arg) {
    Work *wk = (Work *)arg;
    int64_t s = 0;
    for (int64_t k = wk->start; k < wk->end; k++) {
        int64_t idx = k % N;
        s += is_palindrome(wk->inputs[idx]) ? 1 : 0;
    }
    wk->partial = s;
    return NULL;
}

int main(void) {
    int32_t *inputs = (int32_t *)malloc((size_t)N * sizeof(int32_t));
    for (int64_t i = 0; i < N; i++) {
        int64_t raw = i * 2654435769LL + 305419896LL;
        int32_t v32 = (int32_t)raw;
        inputs[i] = (i % 16 == 0) ? manufacture_palindrome(v32) : v32;
    }

    long nworkers = sysconf(_SC_NPROCESSORS_ONLN);
    if (nworkers < 1) {
        nworkers = 1;
    }
    pthread_t *threads = malloc((size_t)nworkers * sizeof(pthread_t));
    Work *works = malloc((size_t)nworkers * sizeof(Work));
    int64_t chunk = K_ITERS / nworkers;
    for (long w = 0; w < nworkers; w++) {
        works[w].inputs = inputs;
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
    free(inputs);
    return 0;
}
