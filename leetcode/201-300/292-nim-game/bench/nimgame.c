/* Benchmark twin for LeetCode #292 — same algorithm as nimgame.kara.
 *
 * Builds the win/lose table the induction describes, rather than timing the
 * one-modulo closed form (which would measure the loop around it).
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define N 20000000

int main(void) {
    unsigned char *win = malloc((size_t)N + 1);
    if (!win) return 1;
    win[0] = 0;
    for (int64_t i = 1; i <= N; i++) {
        int w = 0;
        for (int64_t take = 1; take <= 3; take++)
            if (i - take >= 0 && !win[i - take]) w = 1;
        win[i] = (unsigned char)w;
    }
    int64_t losing = 0, checksum = 0;
    for (int64_t i = 0; i <= N; i++)
        if (!win[i]) {
            losing++;
            checksum = (checksum * 31 + i) % 1000000007;
        }
    printf("losing %lld checksum %lld\n", (long long)losing, (long long)checksum);
    free(win);
    return 0;
}
