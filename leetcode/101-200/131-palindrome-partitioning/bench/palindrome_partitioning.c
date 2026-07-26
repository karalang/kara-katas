/* Benchmark harness for LeetCode #131 — Palindrome Partitioning.
 * Mirrors palindrome_partitioning.kara algorithm-for-algorithm.
 *
 * `substring` walks the string and filters, matching the kata's O(n)
 * implementation rather than a memcpy of the range. The per-piece cost is a
 * real part of what the benchmark measures, so shortcutting it here would make
 * C a different algorithm.
 */

#include <stdio.h>
#include <string.h>

#define MAXN 32
#define MAXPATH 32
#define ITERS 150

static long long modulus(void) { return 1000000007LL; }

static int is_pal(const char *bytes, long long lo, long long hi) {
    long long l = lo;
    long long h = hi;
    while (l < h) {
        if (bytes[l] != bytes[h]) {
            return 0;
        }
        l++;
        h--;
    }
    return 1;
}

static void substring(const char *s, long long lo, long long hi, char *out) {
    long long w = 0;
    for (long long i = 0; s[i] != '\0'; i++) {
        if (i >= lo && i <= hi) {
            out[w++] = s[i];
        }
    }
    out[w] = '\0';
}

static char path[MAXPATH][MAXN];
static long long pathn;

static long long part_hash(void) {
    long long m = modulus();
    long long h = 0;
    for (long long idx = 0; idx < pathn; idx++) {
        for (const char *p = path[idx]; *p; p++) {
            h = (h * 131 + ((long long)(unsigned char)*p - 96)) % m;
        }
        h = (h * 131 + 27) % m;
    }
    return h;
}

static void backtrack(const char *s, long long start, long long n, long long *count,
                      long long *digest) {
    if (start == n) {
        long long m = modulus();
        *digest = (*digest + part_hash()) % m;
        *count += 1;
        return;
    }
    for (long long end = start; end < n; end++) {
        if (is_pal(s, start, end)) {
            substring(s, start, end, path[pathn]);
            pathn++;
            backtrack(s, end + 1, n, count, digest);
            pathn--;
        }
    }
}

int main(void) {
    const char *cases[4] = {
        "aaaaaaaaaaaaaaaa",
        "abababababababab",
        "abcdefghijklmnop",
        "aabaacaabaacaaba",
    };
    long long np = 4;

    long long sink = 0;
    for (long long it = 0; it < ITERS; it++) {
        long long idx = (it * 3) % np;
        const char *s = cases[idx];
        long long n = (long long)strlen(s);
        pathn = 0;
        long long count = 0;
        long long digest = 0;
        backtrack(s, 0, n, &count, &digest);
        sink = (sink + count * 7 + digest) % 1000000007LL;
    }
    printf("%lld\n", sink);
    return 0;
}
