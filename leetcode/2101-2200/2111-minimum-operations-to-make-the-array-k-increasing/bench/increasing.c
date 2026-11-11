// LeetCode #2111: Minimum Operations to Make the Array K-Increasing -- the
// benchmark, the same algorithm as increasing.kara: each chain's patience
// tails, the first tail above each value found by binary search.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 100000

static int64_t tails[N];

static int64_t k_increasing(const int64_t *arr, int64_t n, int64_t k) {
    int64_t changes = 0;
    for (int64_t r = 0; r < k; r++) {
        int64_t count = 0, len = 0;
        for (int64_t i = r; i < n; i += k) {
            int64_t x = arr[i];
            int64_t lo = 0, hi = count;
            while (lo < hi) {
                int64_t mid = lo + (hi - lo) / 2;
                if (tails[mid] <= x) lo = mid + 1; else hi = mid;
            }
            tails[lo] = x;
            if (lo == count) count++;
            len++;
        }
        changes += len - count;
    }
    return changes;
}

static int64_t seed = 2111;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int64_t *arrays[10];
    for (int a = 0; a < 10; a++) {
        arrays[a] = malloc(sizeof(int64_t) * N);
        for (int i = 0; i < N; i++) {
            int64_t hi = next_random();
            int64_t lo = next_random();
            arrays[a][i] = (hi * 32768 + lo) % 100000 + 1;
        }
    }
    int64_t total = 0, check = 0;
    for (int64_t round = 0; round < 10; round++) {
        for (int a = 0; a < 10; a++) {
            int64_t at = round * 9973 + a;
            arrays[a][at] = arrays[a][at] % 100000 + 1;
            int64_t got = k_increasing(arrays[a], N, round + 1);
            total += got;
            check = (check * 31 + got) % 1000000007;
        }
    }
    printf("100 solves: %lld operations, checksum %lld\n", (long long)total, (long long)check);
    for (int a = 0; a < 10; a++) free(arrays[a]);
    return 0;
}
