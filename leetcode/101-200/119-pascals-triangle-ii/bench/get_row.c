/* LeetCode #119 — C mirror, in-place single-row Pascal.
 * Same algorithm + workload as get_row.kara: each rep builds one row of length rowIndex+1 (data-
 * dependent rowIndex = 30 + acc%20), updates it in place right-to-left, folds every entry. K=440000.
 * The metal floor: a single malloc'd long[] per rep. */
#include <stdio.h>
#include <stdlib.h>
#define MOD 1000000007LL
static long long *get_row(long long ri, long long *len_out) {
    long long n = ri + 1;
    long long *row = (long long *)malloc(sizeof(long long) * n);
    for (long long j = 0; j < n; j++) row[j] = 1;
    for (long long i = 2; i <= ri; i++)
        for (long long k = i - 1; k >= 1; k--) row[k] = row[k] + row[k - 1];
    *len_out = n;
    return row;
}
static long long row_hash(long long *row, long long n) {
    long long h = 1;
    for (long long j = 0; j < n; j++) h = (h * 131 + row[j]) % MOD;
    return (h * 31 + n + 7) % MOD;
}
int main(void) {
    long long acc = 0;
    for (long long rep = 0; rep < 440000; rep++) {
        long long ri = 30 + (acc % 20), n;
        long long *row = get_row(ri, &n);
        acc = (acc * 131 + row_hash(row, n)) % MOD;
        free(row);
    }
    printf("%lld\n", acc);
    return 0;
}
