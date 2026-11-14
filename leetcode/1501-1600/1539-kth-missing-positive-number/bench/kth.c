// LeetCode #1539: Kth Missing Positive Number -- bench: the ★ arm (binary
// search on the count of missing numbers) over 1000 arrays of 1 to 1000
// values and 1000 values of k, built once, every pair asked 5 times. C
// mirror of kth.kara.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t find_kth_positive(const int64_t *arr, int64_t n, int64_t k) {
    int64_t lo = 0, hi = n;
    while (lo < hi) {
        int64_t mid = (lo + hi) / 2;
        if (arr[mid] - mid - 1 < k) {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    return lo + k;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

int main(void) {
    int64_t seed = 1539;
    int64_t *arrays[1000];
    int64_t lens[1000];
    for (int a = 0; a < 1000; a++) {
        int64_t n = next_random(&seed) % 1000 + 1;
        int64_t gap = next_random(&seed) % 4 + 1;
        int64_t *arr = malloc(n * sizeof(int64_t));
        int64_t value = 0;
        for (int64_t i = 0; i < n; i++) {
            value += next_random(&seed) % gap + 1;
            arr[i] = value;
        }
        arrays[a] = arr;
        lens[a] = n;
    }
    int64_t ks[1000];
    for (int i = 0; i < 1000; i++) {
        ks[i] = next_random(&seed) % 2000 + 1;
    }
    int64_t check = 0;
    for (int p = 0; p < 5; p++) {
        for (int a = 0; a < 1000; a++) {
            for (int i = 0; i < 1000; i++) {
                check = mix(check, find_kth_positive(arrays[a], lens[a], ks[i]));
            }
        }
    }
    for (int a = 0; a < 1000; a++) {
        free(arrays[a]);
    }
    printf("5 passes over 1000 arrays of up to 1000 values and 1000 values of k: checksum %lld\n", (long long)check);
    return 0;
}
