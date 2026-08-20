/* Benchmark twin for LeetCode #293 — same algorithm as flipgame.kara.
 *
 * PARITY NOTE. Kara's String is append-only, so its inner loop builds each
 * result character by character with a branch per position, and allocates a
 * fresh owned string per result. This mirror does the same: malloc per state,
 * one branch per character. An earlier version of this file used a static
 * buffer and memcpy, which measured 29 ms against Kara's 515 -- a 17x gap that
 * was entirely the algorithm, not the language.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define LEN 64
#define BOARDS 40000
#define MAXOUT 64

static int64_t next_rand(int64_t s) { return (s * 1103515245 + 12345) & 2147483647; }

int main(void) {
    int64_t seed = 20260820;
    int densities[3] = {15, 50, 85};
    int64_t total_states = 0, checksum = 0;
    char cs[LEN];
    char *out[MAXOUT];

    for (int d = 0; d < 3; d++) {
        for (int b = 0; b < BOARDS; b++) {
            for (int i = 0; i < LEN; i++) {
                seed = next_rand(seed);
                cs[i] = ((seed / 65536) % 100) < densities[d] ? '+' : '-';
            }
            int nout = 0;
            for (int i = 0; i + 1 < LEN; i++) {
                if (cs[i] == '+' && cs[i + 1] == '+') {
                    char *t = malloc(LEN + 1);        /* one owned string per state */
                    for (int j = 0; j < LEN; j++)     /* one branch per character */
                        t[j] = (j == i || j == i + 1) ? '-' : cs[j];
                    t[LEN] = '\0';
                    out[nout++] = t;
                }
            }
            total_states += nout;
            for (int k = 0; k < nout; k++) {
                checksum = (checksum * 31 + LEN) % 1000000007;
                free(out[k]);
            }
        }
    }
    printf("states %lld checksum %lld\n", (long long)total_states, (long long)checksum);
    return 0;
}
