/* Benchmark mirror of meetpoint.kara — LeetCode #296, separable medians.
 * Same two scans (row-major then column-major), same reused scratch, same sink. */
#include <stdio.h>

#define NCASES 400
#define DIM    128
#define PASSES 30
#define CELLS  (DIM * DIM)
#define MOD    1000000007LL

static unsigned char corpus[(size_t)NCASES * CELLS];
static long rows[CELLS];
static long cols[CELLS];

int main(void) {
    long long state = 24601;
    for (size_t n = 0; n < (size_t)NCASES * CELLS; n++) {
        state = (state * 1103515245LL + 12345LL) & 0x7fffffffLL;
        corpus[n] = ((state / 65536) % 100 < 10) ? 1 : 0;
    }

    long long checksum = 0;

    for (int p = 0; p < PASSES; p++) {
        for (int ci = 0; ci < NCASES; ci++) {
            const unsigned char *base = corpus + (size_t)ci * CELLS;

            int k = 0;
            for (int r = 0; r < DIM; r++)
                for (int c = 0; c < DIM; c++)
                    if (base[r * DIM + c] == 1) rows[k++] = r;

            int k2 = 0;
            for (int c = 0; c < DIM; c++)
                for (int r = 0; r < DIM; r++)
                    if (base[r * DIM + c] == 1) cols[k2++] = c;

            long long total = 0;
            if (k > 0) {
                long mr = rows[k / 2];
                long mc = cols[k / 2];
                for (int i = 0; i < k; i++) {
                    long dr = rows[i] - mr;
                    total += (dr < 0) ? -dr : dr;
                    long dc = cols[i] - mc;
                    total += (dc < 0) ? -dc : dc;
                }
            }
            checksum = (checksum + total) % MOD;
        }
    }

    printf("checksum %lld\n", checksum);
    return 0;
}
