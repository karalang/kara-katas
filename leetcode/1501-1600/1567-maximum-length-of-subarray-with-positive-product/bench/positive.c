// LeetCode #1567: Maximum Length of Subarray With Positive Product --
// bench: the ★ arm over 20 arrays of 200000 values, built once, each
// value 0 one time in 5000 and otherwise of 1 to 1000, negative one time in
// three; 20 passes, each first flipping the sign of one value of every
// array.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t get_max_len(const int64_t *nums, int64_t n) {
    int64_t positive = 0, negative = 0, best = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t x = nums[i];
        if (x > 0) {
            positive += 1;
            negative = negative > 0 ? negative + 1 : 0;
        } else if (x < 0) {
            int64_t was_positive = positive;
            positive = negative > 0 ? negative + 1 : 0;
            negative = was_positive + 1;
        } else {
            positive = 0;
            negative = 0;
        }
        if (positive > best) best = positive;
    }
    return best;
}

static int64_t seed = 1567;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

int main(void) {
    const int64_t n = 200000;
    int64_t *arrays[20];
    for (int a = 0; a < 20; a++) {
        arrays[a] = malloc(sizeof(int64_t) * n);
        for (int64_t i = 0; i < n; i++) {
            int64_t size = next_random() % 1000 + 1;
            int64_t kind = next_random();
            arrays[a][i] = kind % 5000 == 0 ? 0 : kind % 3 == 0 ? -size : size;
        }
    }
    int64_t check = 0, total = 0;
    for (int64_t p = 0; p < 20; p++) {
        for (int64_t a = 0; a < 20; a++) {
            int64_t at = (p * 7919 + a * 104729) % n;
            arrays[a][at] = -arrays[a][at];
            int64_t length = get_max_len(arrays[a], n);
            total += length;
            check = mix(check, length);
        }
    }
    printf("20 passes over 20 arrays of 200000 values: lengths sum %lld, checksum %lld\n",
           (long long)total, (long long)check);
    for (int a = 0; a < 20; a++) free(arrays[a]);
    return 0;
}
