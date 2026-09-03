/* Benchmark mirror — LeetCode 310, Minimum Height Trees.
 * Same four CSR trees, same LCG, same leaf-peeling, same checksum-driven tree
 * selection and masked sink as peel.kara. See ../README.md § Benchmarks. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(void) {
    const int64_t n = 60000, trees = 4, passes = 950;
    int64_t *all_off = malloc((size_t)(trees * (n + 1)) * sizeof(int64_t));
    int64_t off_len = 0;
    int64_t nbr_cap = trees * 2 * (n - 1) + 16;
    int64_t *all_nbr = malloc((size_t)nbr_cap * sizeof(int64_t));
    int64_t nbr_len = 0;

    int64_t state = 20310;
    int64_t *deg = malloc((size_t)n * sizeof(int64_t));
    int64_t *pa  = malloc((size_t)n * sizeof(int64_t));
    int64_t *cursor = malloc((size_t)n * sizeof(int64_t));
    for (int64_t t = 0; t < trees; t++) {
        int64_t window = 1 + t * 3;
        for (int64_t i = 0; i < n; i++) deg[i] = 0;
        pa[0] = 0;
        for (int64_t i = 1; i < n; i++) {
            int64_t w = window; if (w > i) w = i;
            state = (state * 1103515245 + 12345) % 2147483648;
            int64_t p = i - 1 - state % w;
            pa[i] = p; deg[i] += 1; deg[p] += 1;
        }
        int64_t base = off_len;
        int64_t running = nbr_len;
        for (int64_t k = 0; k < n; k++) { all_off[off_len++] = running; running += deg[k]; }
        all_off[off_len++] = running;
        for (int64_t k = 0; k < n; k++) cursor[k] = all_off[base + k];
        for (int64_t k = 0; k < running - nbr_len; k++) all_nbr[nbr_len + k] = 0;
        nbr_len = running;
        for (int64_t i = 1; i < n; i++) {
            int64_t p = pa[i];
            all_nbr[cursor[i]++] = p;
            all_nbr[cursor[p]++] = i;
        }
    }

    int64_t checksum = 0;
    int64_t *degree = malloc((size_t)n * sizeof(int64_t));
    int64_t *alive  = malloc((size_t)n * sizeof(int64_t));
    int64_t *layer  = malloc((size_t)n * sizeof(int64_t));
    int64_t *next   = malloc((size_t)n * sizeof(int64_t));

    for (int64_t p = 0; p < passes; p++) {
        int64_t which = (p + checksum) % trees;
        int64_t base = which * (n + 1);

        int64_t lcount = 0;
        for (int64_t i = 0; i < n; i++) {
            int64_t d = all_off[base + i + 1] - all_off[base + i];
            degree[i] = d; alive[i] = 1;
            if (d == 1) layer[lcount++] = i;
        }

        int64_t remaining = n;
        while (remaining > 2) {
            remaining -= lcount;
            int64_t ncount = 0;
            for (int64_t k = 0; k < lcount; k++) {
                int64_t v = layer[k];
                alive[v] = 0;
                for (int64_t j = all_off[base + v]; j < all_off[base + v + 1]; j++) {
                    int64_t w = all_nbr[j];
                    if (alive[w] == 1) {
                        degree[w] -= 1;
                        if (degree[w] == 1) next[ncount++] = w;
                    }
                }
            }
            for (int64_t c = 0; c < ncount; c++) layer[c] = next[c];
            lcount = ncount;
        }

        int64_t acc = 0;
        for (int64_t i = 0; i < n; i++) if (alive[i] == 1) acc += i;
        checksum = (checksum + acc) & 0x3FFFFFFF;
    }
    printf("checksum %lld\n", (long long)checksum);
    return 0;
}
