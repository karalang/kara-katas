/* Benchmark harness for LeetCode #132 — Palindrome Partitioning II.
 * Mirrors min_cut.kara algorithm-for-algorithm.
 *
 * The palindrome table is a genuinely nested structure (array of row pointers)
 * matching Vec<Vec<bool>> / [][]bool, not a flat n*n block, and its element
 * type is `unsigned char` rather than a packed bitset — a bitset would be a
 * different data structure from the other lanes' bool vectors.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 500
#define ITERS 400
#define NP 4

static unsigned char *pal[N];
static long long cut_[N];

static long long min_cut(const char *s) {
    long long n = (long long)strlen(s);
    if (n <= 1) {
        return 0;
    }

    for (long long i = 0; i < n; i++) {
        for (long long j = 0; j < n; j++) {
            pal[i][j] = (i == j);
        }
    }

    for (long long length = 2; length <= n; length++) {
        for (long long lo = 0; lo <= n - length; lo++) {
            long long hi = lo + length - 1;
            int ends_match = (unsigned char)s[lo] == (unsigned char)s[hi];
            int inner_ok = (length == 2) || pal[lo + 1][hi - 1];
            if (ends_match && inner_ok) {
                pal[lo][hi] = 1;
            }
        }
    }

    for (long long i = 0; i < n; i++) {
        cut_[i] = 0;
    }
    for (long long i = 0; i < n; i++) {
        if (pal[0][i]) {
            cut_[i] = 0;
        } else {
            long long best = i;
            for (long long j = 1; j <= i; j++) {
                if (pal[j][i] && (cut_[j - 1] + 1) < best) {
                    best = cut_[j - 1] + 1;
                }
            }
            cut_[i] = best;
        }
    }
    return cut_[n - 1];
}

static void lcg_str(long long seed, long long n, long long alpha, char *out) {
    const char *alphabet = "abcdefghijklmnopqrstuvwxyz";
    long long x = seed;
    long long w = 0;
    for (long long k = 0; k < n; k++) {
        x = (x * 1103515245 + 12345) % 2147483648LL;
        long long target = (x / 65536) % alpha;
        for (long long idx = 0; idx < 26; idx++) {
            if (idx == target) {
                out[w++] = alphabet[idx];
            }
        }
    }
    out[w] = '\0';
}

int main(void) {
    for (long long i = 0; i < N; i++) {
        pal[i] = malloc((size_t)N);
    }

    static char cases[NP][N + 1];
    long long alphas[NP] = {2, 4, 26, 3};
    for (long long j = 0; j < NP; j++) {
        lcg_str(j + 1, N, alphas[j], cases[j]);
    }

    long long sink = 0;
    for (long long it = 0; it < ITERS; it++) {
        long long idx = (it * 3) % NP;
        sink = (sink + min_cut(cases[idx])) % 1000000007LL;
    }
    printf("%lld\n", sink);
    return 0;
}
