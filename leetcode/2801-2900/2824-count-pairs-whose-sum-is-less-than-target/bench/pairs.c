// LeetCode #2824: Count Pairs Whose Sum is Less than Target -- the
// bench's C mirror of the ★ arm: the numbers copied and sorted by qsort,
// two pointers closing in.

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int ascending(const void *a, const void *b) {
    long long x = *(const long long *)a, y = *(const long long *)b;
    return (x > y) - (x < y);
}

static long long count_pairs(const long long *nums, int n, long long target) {
    long long sorted[50];
    memcpy(sorted, nums, n * sizeof *sorted);
    qsort(sorted, n, sizeof *sorted, ascending);
    long long count = 0;
    int i = 0, j = n - 1;
    while (i < j) {
        if (sorted[i] + sorted[j] < target) {
            count += j - i;
            i++;
        } else {
            j--;
        }
    }
    return count;
}

static long long seed = 2824;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    enum { COUNT = 200000, ROUNDS = 5 };
    static long long nums[COUNT][50], targets[COUNT];
    for (int c = 0; c < COUNT; c++) {
        for (int i = 0; i < 50; i++) nums[c][i] = next_random() % 101 - 50;
        targets[c] = next_random() % 101 - 50;
    }
    long long total = 0, check = 0;
    for (int r = 0; r < ROUNDS; r++)
        for (int c = 0; c < COUNT; c++) {
            long long a = count_pairs(nums[c], 50, targets[c]);
            total += a;
            check = (check * 31 + a + r) % 1000000007;
        }
    printf("%d arrays of 50, %d rounds: %lld pairs, checksum %lld\n", COUNT, ROUNDS, total, check);
    return 0;
}
