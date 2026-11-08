// LeetCode #1064: Fixed Point -- the benchmark, the same binary search as
// fixed.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t fixed_point(const int64_t *arr, int64_t n) {
    // arr[i] < i for every i below lo, and arr[i] >= i from hi on
    int64_t lo = 0, hi = n;
    while (lo < hi) {
        int64_t mid = lo + (hi - lo) / 2;
        if (arr[mid] < mid)
            lo = mid + 1;
        else
            hi = mid;
    }
    return lo < n && arr[lo] == lo ? lo : -1;
}

static int64_t seed = 1064;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

// `n` distinct numbers in ascending order from `first`, each the last
// plus 1 or 2.
static int64_t *random_sorted(int64_t n, int64_t first) {
    int64_t *arr = malloc(n * sizeof *arr);
    int64_t x = first;
    for (int64_t i = 0; i < n; i++) {
        arr[i] = x;
        x += 1 + next_random() % 2;
    }
    return arr;
}

int main(void) {
    // 8 arrays of 1000000 numbers, built once, then each answered on its
    // first 500000 suffixes
    int64_t *arrays[8];
    for (int64_t a = 0; a < 8; a++) arrays[a] = random_sorted(1000000, -100000 * a);
    int64_t calls = 0, found = 0, check = 0;
    for (int a = 0; a < 8; a++) {
        for (int64_t p = 0; p < 500000; p++) {
            int64_t answer = fixed_point(arrays[a] + p, 1000000 - p);
            if (answer >= 0) found++;
            check = (check * 31 + answer + 1) % 1000000007;
            calls++;
        }
    }
    printf("%lld calls: %lld found, checksum %lld\n", (long long)calls, (long long)found,
           (long long)check);
    return 0;
}
