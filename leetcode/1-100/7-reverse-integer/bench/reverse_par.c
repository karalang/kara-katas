/* LeetCode #7 — C pthreads-parallel mirror (par-lane BARE-METAL FLOOR, reverse).
 * Same pop-and-push reverse; the K=50M reduction split across a fixed pool
 * of _SC_NPROCESSORS_ONLN pthreads (spawn once, chunk, join+merge). Raw OS
 * threads, no runtime — the ceiling auto-par is measured against. Sink matches
 * the kara/rust/c/go mirrors.
 * Build: clang -O3 reverse_par.c -o … -lpthread */
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>

#define N 1024
#define K_ITERS 50000000LL

static int32_t reverse(int32_t x) {
    int32_t result = 0;
    const int32_t int_max = 2147483647;
    const int32_t int_min = -2147483648;
    const int32_t max_div = int_max / 10;
    const int32_t min_div = int_min / 10;

    while (x != 0) {
        int32_t digit = x % 10;
        if (result > max_div || (result == max_div && digit > 7)) {
            return 0;
        }
        if (result < min_div || (result == min_div && digit < -8)) {
            return 0;
        }
        result = result * 10 + digit;
        x /= 10;
    }
    return result;
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
        s += (int64_t)reverse(wk->inputs[idx]);
    }
    wk->partial = s;
    return NULL;
}

int main(void) {
    int32_t *inputs = (int32_t *)malloc((size_t)N * sizeof(int32_t));
    for (int64_t i = 0; i < N; i++) {
        int64_t raw = i * 2654435769LL + 305419896LL;
        inputs[i] = (int32_t)raw;
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
