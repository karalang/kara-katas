// LeetCode #2529: Maximum Count of Positive Integer and Negative Integer
// -- C mirror of the benchmark (count.kara): the same lists, passes, order
// and checksum.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t first_where(const int64_t *nums, int64_t n, int64_t above) {
    int64_t lo = 0, hi = n;
    while (lo < hi) {
        int64_t mid = lo + (hi - lo) / 2;
        if (nums[mid] > above) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}

static int64_t maximum_count(const int64_t *nums, int64_t n) {
    int64_t negatives = first_where(nums, n, -1);
    int64_t positives = n - first_where(nums, n, 0);
    return negatives > positives ? negatives : positives;
}

static int64_t seed = 2529;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int cmp(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int64_t lists[1000][2000];

int main(void) {
    for (int t = 0; t < 1000; t++) {
        int64_t shift = next_random() % 4001 - 2000;
        for (int j = 0; j < 2000; j++) {
            int64_t v = next_random() % 4001 - 2000 + shift;
            if (v < -2000) v = -2000;
            if (v > 2000) v = 2000;
            lists[t][j] = v;
        }
        qsort(lists[t], 2000, sizeof(int64_t), cmp);
    }
    const int passes = 3000;
    int64_t check = 0;
    for (int p = 0; p < passes; p++) {
        int64_t start = check % 1000;
        for (int64_t i = 0; i < 1000; i++)
            check = (check * 31 + maximum_count(lists[(start + i) % 1000], 2000) + p) % 1000000007;
    }
    printf("%d passes over 1000 lists of 2000 numbers: checksum %lld\n", passes, (long long)check);
    return 0;
}
