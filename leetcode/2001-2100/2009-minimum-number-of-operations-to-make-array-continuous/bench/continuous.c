// LeetCode #2009: Minimum Number of Operations to Make Array Continuous --
// the ★ arm's benchmark, a mirror of continuous.kara. The copy is
// allocated and sorted per call (qsort), as the Kāra program's is.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int cmp(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int64_t min_operations(const int64_t *nums, int64_t n) {
    int64_t *values = malloc(n * sizeof(int64_t));
    memcpy(values, nums, n * sizeof(int64_t));
    qsort(values, n, sizeof(int64_t), cmp);
    int64_t m = 0;
    for (int64_t i = 0; i < n; i++)
        if (m == 0 || values[m - 1] != values[i]) values[m++] = values[i];
    int64_t kept = 0, right = 0;
    for (int64_t left = 0; left < m; left++) {
        while (right < m && values[right] <= values[left] + n - 1) right++;
        if (right - left > kept) kept = right - left;
    }
    free(values);
    return n - kept;
}

static int64_t seed = 2009;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    static int64_t arrays[200][2000];
    for (int64_t a = 0; a < 200; a++) {
        int64_t top = 2000 * (a + 1);
        for (int i = 0; i < 2000; i++) {
            int64_t hi = next_random();
            arrays[a][i] = (hi * 32768 + next_random()) % top + 1;
        }
    }
    int64_t calls = 0, sum = 0, check = 0;
    for (int r = 0; r < 25; r++) {
        for (int a = 0; a < 200; a++) {
            int64_t answer = min_operations(arrays[a], 2000);
            calls++;
            sum += answer;
            check = (check * 31 + answer) % 1000000007;
        }
    }
    printf("%lld calls: sum %lld, checksum %lld\n", (long long)calls, (long long)sum, (long long)check);
    return 0;
}
