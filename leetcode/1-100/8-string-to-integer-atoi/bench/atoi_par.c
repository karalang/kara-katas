/* LeetCode #8 — C pthreads-parallel mirror (par-lane BARE-METAL FLOOR, atoi).
 * Same one-pass my_atoi; the K=10M reduction split across a fixed pool of
 * _SC_NPROCESSORS_ONLN pthreads (spawn once, chunk, join+merge). Raw OS
 * threads, no runtime — the ceiling auto-par is measured against. Sink
 * matches the kara/rust/c/go mirrors.
 * Build: clang -O3 atoi_par.c -o … -lpthread */
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>

#define N 8
#define K_ITERS 10000000LL

static int32_t my_atoi(const char *s) {
    size_t n = strlen(s);

    size_t i = 0;
    while (i < n && s[i] == ' ') {
        i++;
    }

    int32_t sign = 1;
    if (i < n && s[i] == '+') {
        i++;
    } else if (i < n && s[i] == '-') {
        sign = -1;
        i++;
    }

    const int32_t int_max = 2147483647;
    const int32_t int_min = -2147483648;
    const int32_t max_div = int_max / 10;

    int32_t result = 0;
    while (i < n) {
        unsigned char b = (unsigned char)s[i];
        if (b < '0' || b > '9') {
            break;
        }
        int32_t digit = (int32_t)(b - '0');
        if (result > max_div || (result == max_div && digit > 7)) {
            return sign == 1 ? int_max : int_min;
        }
        result = result * 10 + digit;
        i++;
    }

    return sign * result;
}

typedef struct {
    const char **inputs;
    int64_t start, end, partial;
} Work;

static void *worker(void *arg) {
    Work *wk = (Work *)arg;
    int64_t s = 0;
    for (int64_t k = wk->start; k < wk->end; k++) {
        int64_t idx = k % N;
        s += (int64_t)my_atoi(wk->inputs[idx]);
    }
    wk->partial = s;
    return NULL;
}

int main(void) {
    const char *inputs[N] = {
        "42",
        "   -42",
        "4193 with words",
        "91283472332",
        "+1",
        "  0000000000012345678",
        "-2147483648",
        "  -0012a42",
    };

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
    return 0;
}
