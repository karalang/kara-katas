/* LeetCode #59 — C pthreads-parallel mirror (par-lane BARE-METAL FLOOR,
 * spiral_matrix_ii). Same boundary-shrinking generator + position-weighted
 * checksum; the K=180k reduction split across a fixed pool of
 * _SC_NPROCESSORS_ONLN pthreads (spawn once, chunk, join+sum). Unlike kata
 * 57's par floor there is no count shortcut — the checksum reads every cell,
 * so each worker does the full generate + fold. Sink matches the
 * kara/rust/c/go mirrors.
 * Build: clang -O3 spiral_matrix_ii_par.c -o … -lpthread */
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>

#define M_SIZES 9
#define K_ITERS 180000LL

static int64_t **generate_matrix(int64_t n) {
    int64_t **grid = (int64_t **)malloc(sizeof(int64_t *) * (size_t)n);
    for (int64_t r = 0; r < n; r++) {
        grid[r] = (int64_t *)calloc((size_t)n, sizeof(int64_t));
    }
    int64_t top = 0, bottom = n - 1, left = 0, right = n - 1, v = 1;
    while (top <= bottom && left <= right) {
        for (int64_t c = left; c <= right; c++) grid[top][c] = v++;
        top++;
        for (int64_t r2 = top; r2 <= bottom; r2++) grid[r2][right] = v++;
        right--;
        if (top <= bottom) {
            for (int64_t c2 = right; c2 >= left; c2--) grid[bottom][c2] = v++;
            bottom--;
        }
        if (left <= right) {
            for (int64_t r3 = bottom; r3 >= top; r3--) grid[r3][left] = v++;
            left++;
        }
    }
    return grid;
}

static int64_t checksum(int64_t **grid, int64_t n) {
    int64_t s = 0;
    for (int64_t i = 0; i < n; i++)
        for (int64_t j = 0; j < n; j++)
            s += grid[i][j] * (i * n + j + 1);
    return s;
}

static void free_matrix(int64_t **grid, int64_t n) {
    for (int64_t r = 0; r < n; r++) free(grid[r]);
    free(grid);
}

typedef struct {
    int64_t start, end, partial;
} Work;

static void *worker(void *arg) {
    Work *wk = (Work *)arg;
    int64_t s = 0;
    for (int64_t k = wk->start; k < wk->end; k++) {
        int64_t n = 12 + (k % M_SIZES);
        int64_t **g = generate_matrix(n);
        s += checksum(g, n);
        free_matrix(g, n);
    }
    wk->partial = s;
    return NULL;
}

int main(void) {
    long nworkers = sysconf(_SC_NPROCESSORS_ONLN);
    if (nworkers < 1) nworkers = 1;
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
