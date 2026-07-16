/* LeetCode #118 — C mirror, additive Pascal's triangle.
 * Same algorithm + workload as generate.kara: each rep builds a full triangle of a data-dependent
 * row count (30 + acc%16) as a NESTED `long**` with per-row malloc (structural parity with the
 * Vec[Vec] the others build — a flat contiguous array would give C an unfair cache edge), and folds
 * every entry. K = 80000. */
#include <stdio.h>
#include <stdlib.h>

#define MOD 1000000007LL

/* Build a triangle: tri[i] is a malloc'd row of (i+1) longs. *rows_out set to num_rows. */
static long long **generate(long long num_rows) {
    long long **tri = (long long **)malloc(sizeof(long long *) * num_rows);
    for (long long i = 0; i < num_rows; i++) {
        long long *row = (long long *)malloc(sizeof(long long) * (i + 1));
        for (long long j = 0; j <= i; j++) {
            if (j == 0 || j == i) row[j] = 1;
            else row[j] = tri[i - 1][j - 1] + tri[i - 1][j];
        }
        tri[i] = row;
    }
    return tri;
}

static void free_tri(long long **tri, long long num_rows) {
    for (long long i = 0; i < num_rows; i++) free(tri[i]);
    free(tri);
}

static long long triangle_hash(long long **tri, long long num_rows) {
    long long h = 1;
    for (long long i = 0; i < num_rows; i++) {
        for (long long j = 0; j <= i; j++) h = (h * 131 + tri[i][j]) % MOD;
        h = (h * 31 + (i + 1) + 7) % MOD;
    }
    return h;
}

int main(void) {
    long long acc = 0;
    for (long long rep = 0; rep < 80000; rep++) {
        long long rows = 30 + (acc % 16);
        long long **tri = generate(rows);
        long long h = triangle_hash(tri, rows);
        acc = (acc * 131 + h) % MOD;
        free_tri(tri, rows);
    }
    printf("%lld\n", acc);
    return 0;
}
