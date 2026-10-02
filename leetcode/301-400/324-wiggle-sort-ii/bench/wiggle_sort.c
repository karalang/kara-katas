// Benchmark mirror of LeetCode #324 — same select arm as
// bench/wiggle_sort.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define LEN 1000000
#define PASSES 16
#define STRIDE 9973
#define MODULUS 1073741789

static void swap(int64_t *a, int64_t i, int64_t j) {
    int64_t t = a[i];
    a[i] = a[j];
    a[j] = t;
}

static int64_t median3(int64_t x, int64_t y, int64_t z) {
    if ((x <= y && y <= z) || (z <= y && y <= x)) return y;
    if ((y <= x && x <= z) || (z <= x && x <= y)) return x;
    return z;
}

static int64_t select_k(int64_t *a, int64_t n, int64_t k) {
    int64_t lo = 0, hi = n - 1;
    while (lo < hi) {
        int64_t mid = lo + (hi - lo) / 2;
        int64_t pivot = median3(a[lo], a[mid], a[hi]);
        int64_t lt = lo, i = lo, gt = hi;
        while (i <= gt) {
            if (a[i] < pivot) {
                swap(a, lt, i);
                lt++;
                i++;
            } else if (a[i] > pivot) {
                swap(a, i, gt);
                gt--;
            } else {
                i++;
            }
        }
        if (k < lt) hi = lt - 1;
        else if (k > gt) lo = gt + 1;
        else return pivot;
    }
    return a[k];
}

static void wiggle_sort(int64_t *nums, int64_t n) {
    int64_t median = select_k(nums, n, n / 2);
    int64_t m = n | 1;
    int64_t left = 0, i = 0, right = n - 1;
    while (i <= right) {
        int64_t vi = (1 + 2 * i) % m;
        if (nums[vi] > median) {
            swap(nums, (1 + 2 * left) % m, vi);
            left++;
            i++;
        } else if (nums[vi] < median) {
            swap(nums, vi, (1 + 2 * right) % m);
            right--;
        } else {
            i++;
        }
    }
}

static int64_t next(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t draw(int64_t *seed, int64_t bound) {
    int64_t hi = next(seed);
    int64_t lo = next(seed);
    return (hi * 32768 + lo) % bound;
}

static void refill(int64_t *nums, int64_t n, int64_t k, int64_t *seed) {
    for (int64_t i = 0; i < n; i++) {
        if (i % 2 == 0) nums[i] = draw(seed, k);
        else nums[i] = k + draw(seed, k);
    }
    for (int64_t i = n - 1; i > 0; i--) {
        int64_t j = draw(seed, i + 1);
        swap(nums, i, j);
    }
}

static int64_t violations(const int64_t *a, int64_t n) {
    int64_t bad = 0;
    for (int64_t i = 1; i < n; i++) {
        if (i % 2 == 1) {
            if (a[i] <= a[i - 1]) bad++;
        } else {
            if (a[i] >= a[i - 1]) bad++;
        }
    }
    return bad;
}

int main(void) {
    int64_t seed = 324, sink = 0, bad = 0;
    int64_t ks[4] = {2, 3, 50, 2500};
    int64_t *nums = calloc(LEN, sizeof(int64_t));
    for (int64_t p = 0; p < PASSES; p++) {
        refill(nums, LEN, ks[p % 4], &seed);
        wiggle_sort(nums, LEN);
        bad = violations(nums, LEN);
        int64_t probe = 0;
        for (int64_t i = 0; i < LEN; i += STRIDE) probe = (probe * 31 + nums[i]) % MODULUS;
        sink = (sink * 131 + bad * 7 + probe) % MODULUS;
    }
    printf("sink %lld violations %lld\n", (long long)sink, (long long)bad);
    free(nums);
    return 0;
}
