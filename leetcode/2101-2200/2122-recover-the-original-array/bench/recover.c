// LeetCode #2122: Recover the Original Array -- the benchmark, the same
// algorithm as recover.kara: each positive even distance from the
// smallest number tried as 2k, smallest first, the sorted numbers paired
// by two pointers.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int cmp(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

// Writes the original into `out` and returns its length, or 0.
static int64_t recover_array(const int64_t *nums, int64_t m, int64_t *out) {
    int64_t *sorted = malloc(sizeof(int64_t) * (size_t)m);
    memcpy(sorted, nums, sizeof(int64_t) * (size_t)m);
    qsort(sorted, (size_t)m, sizeof(int64_t), cmp);
    char *used = malloc((size_t)m);
    int64_t found = 0;
    for (int64_t i = 1; i < m; i++) {
        int64_t gap = sorted[i] - sorted[0];
        if (gap == 0 || gap % 2 != 0 || (i > 1 && gap == sorted[i - 1] - sorted[0])) continue;
        int64_t k = gap / 2, len = 0, high = 0;
        memset(used, 0, (size_t)m);
        for (int64_t low = 0; low < m; low++) {
            if (used[low]) continue;
            while (high < m && (used[high] || high <= low || sorted[high] < sorted[low] + 2 * k)) high++;
            if (high == m || sorted[high] != sorted[low] + 2 * k) break;
            used[high] = 1;
            out[len++] = sorted[low] + k;
        }
        if (len * 2 == m) {
            found = len;
            break;
        }
    }
    free(used);
    free(sorted);
    return found;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 2122;
    static int64_t arrays[40][2000];
    const int64_t tops[3] = {1000, 10000, 100000};
    for (int g = 0; g < 40; g++) {
        int64_t k = next_random(&seed) % 500 + 1;
        for (int t = 0; t < 1000; t++) {
            int64_t a = next_random(&seed);
            int64_t x = (a * 32768 + next_random(&seed)) % tops[g % 3] + 1 + k;
            arrays[g][2 * t] = x - k;
            arrays[g][2 * t + 1] = x + k;
        }
        for (int64_t i = 1999; i > 0; i--) {
            int64_t j = next_random(&seed) % (i + 1);
            int64_t tmp = arrays[g][i];
            arrays[g][i] = arrays[g][j];
            arrays[g][j] = tmp;
        }
    }
    static int64_t out[1000];
    int64_t sizes = 0, check = 0;
    for (int r = 0; r < 200; r++) {
        for (int g = 0; g < 40; g++) {
            for (int i = 0; i < 2000; i++) arrays[g][i] += 1;
            int64_t len = recover_array(arrays[g], 2000, out);
            sizes += len;
            for (int64_t i = 0; i < len; i++) check = (check * 31 + out[i]) % 1000000007;
        }
    }
    printf("8000 solves: %lld values recovered, checksum %lld\n", (long long)sizes, (long long)check);
    return 0;
}
