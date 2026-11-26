// LeetCode #1477: Find Two Non-overlapping Sub-arrays Each With Target
// Sum -- bench, C mirror of min_sum_of_lengths.kara. The table of shortest
// windows is malloc'ed each call, as the Kāra and Rust ones are made.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int32_t min_sum_of_lengths(const int32_t *arr, int64_t n, int32_t target) {
    int64_t none = n + 1;
    int64_t *shortest = malloc(sizeof(int64_t) * n);
    int64_t best = 2 * none;
    int64_t sum = 0;
    int64_t left = 0;
    for (int64_t right = 0; right < n; right++) {
        sum += arr[right];
        while (sum > target) {
            sum -= arr[left];
            left++;
        }
        int64_t here = none;
        if (sum == target) {
            here = right - left + 1;
            if (left > 0 && shortest[left - 1] < none && here + shortest[left - 1] < best) {
                best = here + shortest[left - 1];
            }
        }
        if (right > 0 && shortest[right - 1] < here) {
            shortest[right] = shortest[right - 1];
        } else {
            shortest[right] = here;
        }
    }
    free(shortest);
    return best >= 2 * none ? -1 : (int32_t)best;
}

static int64_t seed = 1477;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int64_t n = 100000;
    int32_t *arr = malloc(sizeof(int32_t) * n);
    for (int64_t i = 0; i < n; i++) arr[i] = (int32_t)(1 + next_random() % 1000);
    int64_t check = 0;
    for (int64_t pass = 0; pass < 400; pass++) {
        arr[check % 100000] = (int32_t)(1 + (check / 7) % 1000);
        int32_t target = (int32_t)(500 + check % 20000);
        int32_t got = min_sum_of_lengths(arr, n, target);
        check = (check * 31 + got + 1 + pass) % 1000000007;
    }
    printf("400 passes over 100000 values: checksum %lld\n", (long long)check);
    free(arr);
    return 0;
}
