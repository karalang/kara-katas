/* LeetCode 306 - Additive Number.
 *
 * Mirror of additive.kara: the same O(n^3) scan (two prefix lengths, then
 * verification by exact digit-list addition) over the same flat digit array,
 * with the same planted positives, the same per-pass perturbation and the same
 * masked sink. Kept algorithm-for-algorithm so the benchmark lane is honest.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define CASES  220
#define WIDTH  18
#define PASSES 90
#define MASK   1073741823L

static long digits_span(const long *flat, long base, long lo, long hi, long *out) {
    long m = 0;
    for (long i = lo; i < hi; i++) out[m++] = flat[base + i];
    return m;
}

/* Returns a freshly allocated digit array, exactly as additive.kara's
 * add_digits returns a fresh Vec[i64]. Allocating per call is part of the
 * algorithm being measured, not an implementation detail to hoist away. */
static long *add_digits(const long *a, long na, const long *b, long nb, long *nout) {
    long rev[64], m = 0, carry = 0;
    long i = na - 1, j = nb - 1;
    while (i >= 0 || j >= 0 || carry > 0) {
        long s = carry;
        if (i >= 0) { s += a[i]; i--; }
        if (j >= 0) { s += b[j]; j--; }
        rev[m++] = s % 10;
        carry = s / 10;
    }
    long *out = malloc((size_t)m * sizeof(long));
    for (long k = 0; k < m; k++) out[k] = rev[m - 1 - k];
    *nout = m;
    return out;
}

static int matches_at(const long *flat, long base, long n, long pos, const long *num, long nn) {
    if (pos + nn > n) return 0;
    for (long k = 0; k < nn; k++) if (flat[base + pos + k] != num[k]) return 0;
    return 1;
}

static int no_lead_zero(const long *flat, long base, long lo, long hi) {
    return (hi - lo == 1) || flat[base + lo] != 0;
}

static int is_additive(const long *flat, long base, long n) {
    if (n < 3) return 0;
    for (long len1 = 1; len1 < n - 1; len1++) {
        if (!no_lead_zero(flat, base, 0, len1)) break;
        for (long len2 = 1; len2 < n - len1; len2++) {
            if (!no_lead_zero(flat, base, len1, len1 + len2)) break;
            long na = len1, nb = len2;
            long *a = malloc((size_t)na * sizeof(long));
            long *b = malloc((size_t)nb * sizeof(long));
            digits_span(flat, base, 0, len1, a);
            digits_span(flat, base, len1, len1 + len2, b);
            long pos = len1 + len2, ok = 1, steps = 0;
            while (pos < n && ok) {
                long nc;
                long *c = add_digits(a, na, b, nb, &nc);
                if (matches_at(flat, base, n, pos, c, nc)) {
                    /* The window slides and the oldest number dies -- the same
                     * ownership transfer as `a = b; b = c;` in the Kara arm. */
                    pos += nc;
                    free(a); a = b; na = nb; b = c; nb = nc;
                    steps++;
                } else { free(c); ok = 0; }
            }
            free(a); free(b);
            if (ok && pos == n && steps > 0) return 1;
        }
    }
    return 0;
}

int main(void) {
    static const char *planted[] = {
        "022461016264268110",
        "020204060100160260",
        "021214263105168273",
        "022224466110176286",
        "023234669115184299",
        "024244872120192312",
        "025255075125200325",
        "026265278130208338"
    };
    const long nplant = (long)(sizeof planted / sizeof planted[0]);

    long *flat = malloc((size_t)(CASES * WIDTH) * sizeof(long));
    if (!flat) return 1;
    long m = 0, seed = 7;
    for (long c = 0; c < CASES; c++) {
        if (c % 25 == 0) {
            const char *p = planted[(c / 25) % nplant];
            for (long i = 0; i < WIDTH; i++) flat[m++] = p[i] - '0';
        } else {
            for (long i = 0; i < WIDTH; i++) {
                seed = (seed * 1103515245L + 12345L) % 2147483647L;
                flat[m++] = seed % 10;
            }
        }
    }

    long checksum = 1;
    for (long pass = 0; pass < PASSES; pass++) {
        long site = (checksum * 31 + pass * 7919) % (CASES * WIDTH);
        flat[site] = (flat[site] + 1) % 10;
        long hits = 0;
        for (long c = 0; c < CASES; c++) if (is_additive(flat, c * WIDTH, WIDTH)) hits++;
        checksum = (checksum * 131 + hits * 7919 + site) & MASK;
    }
    printf("checksum %ld\n", checksum);
    free(flat);
    return 0;
}
