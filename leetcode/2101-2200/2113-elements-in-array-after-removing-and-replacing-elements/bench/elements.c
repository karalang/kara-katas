// LeetCode #2113: Elements in Array After Removing and Replacing Elements
// -- the benchmark, the same algorithm as elements.kara: each query's
// minute modulo the period `2n`, then one value or -1 for its phase.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define Q 100000

static void element_in_nums(const int64_t *nums, int64_t n, const int64_t *times,
                            const int64_t *places, int64_t q, int64_t *ans) {
    for (int64_t j = 0; j < q; j++) {
        int64_t t = times[j] % (2 * n), index = places[j];
        if (t < n) {
            ans[j] = index < n - t ? nums[t + index] : -1;
        } else {
            ans[j] = index < t - n ? nums[index] : -1;
        }
    }
}

static int64_t seed = 2113;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int64_t arrays[20][100];
    for (int a = 0; a < 20; a++)
        for (int i = 0; i < 100; i++) arrays[a][i] = next_random() % 101;
    int64_t *times = malloc(sizeof(int64_t) * Q), *places = malloc(sizeof(int64_t) * Q);
    int64_t *ans = malloc(sizeof(int64_t) * Q);
    for (int j = 0; j < Q; j++) {
        times[j] = next_random() % 100001;
        places[j] = next_random() % 100;
    }
    int64_t total = 0, check = 0;
    for (int64_t s = 0; s < 50; s++) {
        int64_t j = s * 1999 % Q;
        times[j] += 1;
        element_in_nums(arrays[s % 20], 100, times, places, Q, ans);
        int64_t sum = 0;
        for (int k = 0; k < Q; k++) sum += ans[k];
        total += sum;
        check = (check * 31 + sum) % 1000000007;
    }
    printf("50 solves: %lld summed, checksum %lld\n", (long long)total, (long long)check);
    free(times);
    free(places);
    free(ans);
    return 0;
}
