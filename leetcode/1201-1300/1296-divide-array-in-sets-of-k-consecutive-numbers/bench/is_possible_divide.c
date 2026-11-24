// LeetCode #1296 bench: the ★ arm over 20 arrays of 16666 runs of 6
// consecutive numbers, shuffled, built once; then 10 passes, each swapping two
// numbers of every array and choosing k from the checksum so far. C has no
// sorted map: the counts are runs of a sorted copy, each later number's run
// found by binary search, as the ★ arm finds its keys in a `SortedMap`.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

enum { ARRAYS = 20, RUNS = 16666, LEN = RUNS * 6 };

static int cmp_i64(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int is_possible_divide(const int64_t *nums, int64_t n, int64_t k) {
    if (n % k != 0) {
        return 0;
    }
    int64_t *sorted = malloc(sizeof(int64_t) * n);
    memcpy(sorted, nums, sizeof(int64_t) * n);
    qsort(sorted, n, sizeof(int64_t), cmp_i64);
    int64_t *keys = malloc(sizeof(int64_t) * n);
    int64_t *count = malloc(sizeof(int64_t) * n);
    int64_t m = 0;
    for (int64_t i = 0; i < n; i++) {
        if (m > 0 && keys[m - 1] == sorted[i]) {
            count[m - 1]++;
        } else {
            keys[m] = sorted[i];
            count[m] = 1;
            m++;
        }
    }
    int ok = 1;
    for (int64_t i = 0; i < m && ok; i++) {
        int64_t sets = count[i];
        if (sets == 0) {
            continue;
        }
        int64_t lo = i;
        for (int64_t y = keys[i]; y < keys[i] + k; y++) {
            // the run of y, at or after lo
            int64_t a = lo, b = m;
            while (a < b) {
                int64_t mid = (a + b) / 2;
                if (keys[mid] < y) {
                    a = mid + 1;
                } else {
                    b = mid;
                }
            }
            if (a == m || keys[a] != y || count[a] < sets) {
                ok = 0;
                break;
            }
            count[a] -= sets;
            lo = a;
        }
    }
    free(sorted);
    free(keys);
    free(count);
    return ok;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t wide_random(int64_t *seed) {
    int64_t a = next_random(seed);
    return a * 32768 + next_random(seed);
}

static int64_t arrays[ARRAYS][LEN];

int main(void) {
    int64_t seed = 1296;
    for (int a = 0; a < ARRAYS; a++) {
        int64_t spread = a % 2 == 0 ? 10000 : 1000000000;
        int64_t n = 0;
        for (int r = 0; r < RUNS; r++) {
            int64_t start = 1 + wide_random(&seed) % spread;
            for (int d = 0; d < 6; d++) {
                arrays[a][n++] = start + d;
            }
        }
        for (int64_t i = 0; i < n; i++) {
            int64_t j = i + wide_random(&seed) % (n - i);
            int64_t held = arrays[a][i];
            arrays[a][i] = arrays[a][j];
            arrays[a][j] = held;
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 10; p++) {
        for (int a = 0; a < ARRAYS; a++) {
            int64_t i = check % LEN, j = (check / LEN) % LEN;
            int64_t held = arrays[a][i];
            arrays[a][i] = arrays[a][j];
            arrays[a][j] = held;
            int64_t k = 1 + check % 6;
            int possible = is_possible_divide(arrays[a], LEN, k);
            check = (check * 31 + (possible ? 2 : 1) + p) % 1000000007;
        }
    }
    printf("10 passes over 20 arrays of 99996: checksum %lld\n", (long long)check);
    return 0;
}
