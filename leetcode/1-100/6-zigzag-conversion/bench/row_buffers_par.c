/* LeetCode #6 — C pthreads-parallel mirror (par-lane BARE-METAL FLOOR, row_buffers).
 * Same row-buffer convert_off; the K=10K reduction split across a fixed pool
 * of _SC_NPROCESSORS_ONLN pthreads (spawn once, chunk, join+merge). Raw OS
 * threads, no runtime — the ceiling auto-par is measured against. Sink matches
 * the kara/rust/c/go mirrors.
 * Build: clang -O3 -pthread row_buffers_par.c -o … */
#include <pthread.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

static void convert_off(const char *chars, size_t off, size_t len, size_t num_rows,
                        char *out, size_t *out_len) {
    if (num_rows <= 1 || num_rows >= len) {
        for (size_t i = 0; i < len; i++) {
            out[i] = chars[off + i];
        }
        *out_len = len;
        return;
    }

    char **rows = (char **)malloc(num_rows * sizeof(char *));
    size_t *row_lens = (size_t *)calloc(num_rows, sizeof(size_t));
    size_t *row_caps = (size_t *)calloc(num_rows, sizeof(size_t));
    for (size_t r = 0; r < num_rows; r++) {
        row_caps[r] = 64;
        rows[r] = (char *)malloc(row_caps[r]);
    }

    size_t cur = 0;
    int going_down = 0;
    for (size_t i = 0; i < len; i++) {
        if (row_lens[cur] == row_caps[cur]) {
            row_caps[cur] *= 2;
            rows[cur] = (char *)realloc(rows[cur], row_caps[cur]);
        }
        rows[cur][row_lens[cur]++] = chars[off + i];
        if (cur == 0 || cur == num_rows - 1) {
            going_down = !going_down;
        }
        if (going_down) {
            cur++;
        } else {
            cur--;
        }
    }

    size_t pos = 0;
    for (size_t r = 0; r < num_rows; r++) {
        memcpy(out + pos, rows[r], row_lens[r]);
        pos += row_lens[r];
        free(rows[r]);
    }
    *out_len = pos;
    free(rows);
    free(row_lens);
    free(row_caps);
}

#define N 10000
#define R_PERIOD 1000
#define K_ITERS 10000
#define NUM_ROWS 4

typedef struct {
    const char *chars;
    int64_t start, end, partial;
} Work;

static void *worker(void *arg) {
    Work *wk = (Work *)arg;
    char *result = (char *)malloc(N);
    size_t result_len;
    int64_t s = 0;
    for (int64_t k = wk->start; k < wk->end; k++) {
        size_t off = (size_t)(k % R_PERIOD);
        convert_off(wk->chars, off, N, NUM_ROWS, result, &result_len);
        s += (int64_t)(unsigned char)result[0]
           + (int64_t)(unsigned char)result[result_len - 1];
    }
    wk->partial = s;
    free(result);
    return NULL;
}

int main(void) {
    static const char pattern[] = "PAYPALISHIRING";
    const size_t pattern_len = sizeof(pattern) - 1;
    const size_t need = N + R_PERIOD;

    char *chars = (char *)malloc(need + pattern_len);
    size_t filled = 0;
    while (filled < need) {
        memcpy(chars + filled, pattern, pattern_len);
        filled += pattern_len;
    }

    long nworkers = sysconf(_SC_NPROCESSORS_ONLN);
    if (nworkers < 1) {
        nworkers = 1;
    }
    pthread_t *threads = malloc((size_t)nworkers * sizeof(pthread_t));
    Work *works = malloc((size_t)nworkers * sizeof(Work));
    int64_t chunk = K_ITERS / nworkers;
    for (long w = 0; w < nworkers; w++) {
        works[w].chars = chars;
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
    free(chars);
    return 0;
}
