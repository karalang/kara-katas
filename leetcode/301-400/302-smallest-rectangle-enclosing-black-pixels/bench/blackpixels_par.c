/* Par-lane C mirror for LeetCode #302 — the four edge searches by hand.
 *
 * Kara's auto-par fans out the four independent searches inside min_area with
 * no annotation (`karac query concurrency`: parallel_groups [0,1,2,3]). This is
 * the same fan-out written by hand on RAW PTHREADS — the bare-metal floor, no
 * work-stealing runtime and no pool.
 *
 * That is the honest comparator for "what does it cost to write this yourself
 * in C", and it is deliberately not a tuned thread pool: the point of the par
 * lane is what the other languages make you do, not how well a hand-rolled
 * scheduler can be made to perform. Expect the per-call thread creation to show
 * up in the number — 1200 calls x 3 spawned threads is 3600 clone() calls, and
 * that cost is the finding, not a flaw in the measurement. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <pthread.h>

static uint8_t *img;
static int64_t W, H;

static inline int row_has_black(int64_t r) {
    for (int64_t c = 0; c < W; c++) if (img[r * W + c] == 1) return 1;
    return 0;
}
static inline int col_has_black(int64_t c) {
    for (int64_t r = 0; r < H; r++) if (img[r * W + c] == 1) return 1;
    return 0;
}
static int64_t first_black_row(int64_t lo, int64_t hi) {
    while (lo < hi) { int64_t m = lo + (hi - lo) / 2; if (row_has_black(m)) hi = m; else lo = m + 1; }
    return lo;
}
static int64_t first_white_row(int64_t lo, int64_t hi) {
    while (lo < hi) { int64_t m = lo + (hi - lo) / 2; if (row_has_black(m)) lo = m + 1; else hi = m; }
    return lo;
}
static int64_t first_black_col(int64_t lo, int64_t hi) {
    while (lo < hi) { int64_t m = lo + (hi - lo) / 2; if (col_has_black(m)) hi = m; else lo = m + 1; }
    return lo;
}
static int64_t first_white_col(int64_t lo, int64_t hi) {
    while (lo < hi) { int64_t m = lo + (hi - lo) / 2; if (col_has_black(m)) lo = m + 1; else hi = m; }
    return lo;
}

typedef struct { int64_t lo, hi, out; int which; } job;

static void *run_job(void *p) {
    job *j = (job *)p;
    switch (j->which) {
        case 0: j->out = first_black_row(j->lo, j->hi); break;
        case 1: j->out = first_white_row(j->lo, j->hi); break;
        case 2: j->out = first_black_col(j->lo, j->hi); break;
        default: j->out = first_white_col(j->lo, j->hi); break;
    }
    return NULL;
}

static int64_t min_area_par(int64_t x, int64_t y) {
    job jobs[4] = {
        { 0,     x + 1, 0, 0 },
        { x + 1, H,     0, 1 },
        { 0,     y + 1, 0, 2 },
        { y + 1, W,     0, 3 },
    };
    pthread_t th[4];
    /* Three spawned, one run on the calling thread — the same shape as the
     * nested-join Rust mirror, so the calling thread does work rather than
     * only waiting. */
    for (int i = 1; i < 4; i++) pthread_create(&th[i], NULL, run_job, &jobs[i]);
    run_job(&jobs[0]);
    for (int i = 1; i < 4; i++) pthread_join(th[i], NULL);
    return (jobs[1].out - jobs[0].out) * (jobs[3].out - jobs[2].out);
}

int main(void) {
    const int64_t n = 4096, queries = 1200;
    W = H = n;
    img = calloc((size_t)(n * n), 1);
    int64_t r0 = n / 2, c0 = n / 2;
    for (int64_t r = 0; r < 40; r++)
        for (int64_t c = 0; c < 40; c++) img[(r0 + r) * n + (c0 + c)] = 1;
    for (int64_t k = 0; k < 25; k++) img[(r0 + 40 + k) * n + (c0 + 20)] = 1;

    int64_t checksum = 0;
    for (int64_t q = 0; q < queries; q++) {
        int64_t sx = r0 + q % 40;
        int64_t sy = c0 + (q * 7) % 40;
        checksum = (checksum * 31 + min_area_par(sx, sy)) % 1000000007;
    }
    printf("queries %lld checksum %lld\n", (long long)queries, (long long)checksum);
    free(img);
    return 0;
}
