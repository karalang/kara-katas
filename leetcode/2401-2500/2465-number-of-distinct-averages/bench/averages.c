// LeetCode #2465: Number of Distinct Averages -- the bench, the ★ arm in
// C: a sorted copy by `qsort`, the `i`th smallest paired with the `i`th
// largest. C has no set, so the sums, at most 200, are marked in a table
// of 201 flags cleared for every answer.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int by_value(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int64_t distinct_averages(const int64_t *nums, int64_t n) {
    int64_t sorted[100];
    memcpy(sorted, nums, sizeof(int64_t) * n);
    qsort(sorted, n, sizeof(int64_t), by_value);
    char seen[201] = {0};
    int64_t count = 0;
    for (int64_t i = 0; i < n / 2; i++) {
        int64_t s = sorted[i] + sorted[n - 1 - i];
        if (!seen[s]) {
            seen[s] = 1;
            count++;
        }
    }
    return count;
}

static int64_t seed = 2465;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

#define LISTS 1000
#define N 100

int main(void) {
    // 1000 lists of 100 numbers from 0 to 100 built once; then 900
    // passes, each setting one number of every list from the checksum so
    // far, then answering every list and folding the answer plus the pass
    // into the checksum
    static int64_t lists[LISTS][N];
    for (int a = 0; a < LISTS; a++)
        for (int i = 0; i < N; i++) lists[a][i] = next_random() % 101;
    int64_t check = 0;
    for (int64_t p = 0; p < 900; p++) {
        for (int64_t a = 0; a < LISTS; a++) {
            lists[a][(check + a) % N] = check % 101;
            check = (check * 31 + distinct_averages(lists[a], N) + p) % 1000000007;
        }
    }
    printf("900 passes over 1000 lists of 100: checksum %lld\n", (long long)check);
    return 0;
}
