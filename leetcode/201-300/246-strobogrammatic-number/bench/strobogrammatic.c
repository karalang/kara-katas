/* Benchmark mirror for LeetCode #246 - Strobogrammatic Number.
 *
 * Same algorithm, same LCG, same sink as the Kara/Rust/Go/Python mirrors.
 * Build-once + punch: 20,000 length-32 numbers built once, 100 passes of the
 * two-pointer check = 2,000,000 calls.
 *
 * The corpus is mostly ACCEPTING by construction (1 in 8 corrupted at one
 * random position) so that rejects happen mid-scan; a uniform digit draw would
 * make almost every number reject on its first character and the benchmark
 * would measure early return instead of the scan.
 *
 * NOTE on parity: STALE CLAIM REMOVED (2026-08-04). This comment used to say
 * the Kara/Rust/Go/Python lanes materialise a character sequence per call while
 * C indexes bytes in place, so C was doing strictly less work. That stopped
 * being true when every lane was moved to one flat N*LEN byte buffer indexed by
 * offset - all five now do the same work per call.
 *
 * C's remaining lead over Kara is bounds-check elimination and nothing else:
 * Kara's punch loop is 21 instructions to C's 15, and the 6-instruction excess
 * is exactly two per-iteration bounds checks. Adding equivalent checks to this
 * mirror (see the README's confirmation section) makes clang emit an isomorphic
 * loop and lands it on Kara's time. Filed as kara B-2026-08-04-8.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 20000
#define LEN 32
#define PASSES 100

static const char PAIR_A[5] = {'0', '1', '8', '6', '9'};
static const char PAIR_B[5] = {'0', '1', '8', '9', '6'};
static const char ALLD[10] = {'0','1','2','3','4','5','6','7','8','9'};

/* -1 = does not survive rotation */
static int rotate_digit(char c) {
    switch (c) {
        case '0': return '0';
        case '1': return '1';
        case '8': return '8';
        case '6': return '9';
        case '9': return '6';
        default:  return -1;
    }
}

static int is_strobogrammatic(const char *num, long len) {
    long lo = 0, hi = len - 1;
    while (lo <= hi) {
        int r = rotate_digit(num[lo]);
        if (r < 0 || (char)r != num[hi]) return 0;
        lo++;
        hi--;
    }
    return 1;
}

static long lcg(long state) {
    return (state * 1103515245L + 12345L) & 2147483647L;
}

int main(void) {
    char *corpus = malloc((size_t)N * LEN);
    long state = 1;
    for (long k = 0; k < N; k++) {
        char *num = corpus + k * LEN;
        long lo = 0, hi = LEN - 1;
        while (lo < hi) {
            state = lcg(state);
            long p = (state / 65536) % 5;
            num[lo] = PAIR_A[p];
            num[hi] = PAIR_B[p];
            lo++;
            hi--;
        }
        state = lcg(state);
        if ((state / 65536) % 8 == 0) {
            state = lcg(state);
            long pos = (state / 65536) % LEN;
            state = lcg(state);
            num[pos] = ALLD[(state / 65536) % 10];
        }
    }

    long acc = 0;
    for (long p = 0; p < PASSES; p++)
        for (long i = 0; i < N; i++)
            acc = (acc * 131 + is_strobogrammatic(corpus + i * LEN, LEN)) % 1000000007L;
    printf("%ld\n", acc);
    return 0;
}
