// benchmark's C mirror of pairs.kara (LeetCode #2206, the ★ arm): a count
// per value up to 500, then one pass over the counts. The count table is
// allocated per call, as Kāra's `Vec.filled(501, 0)`.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static bool divide_array(const int64_t *nums, int64_t n) {
    int64_t *count = calloc(501, sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) count[nums[i]]++;
    bool ok = true;
    for (int64_t v = 0; v < 501; v++) {
        if (count[v] % 2 == 1) {
            ok = false;
            break;
        }
    }
    free(count);
    return ok;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

// 1000 numbers up to `top`: 500 pairs shuffled, or 1000 drawn freely
static int64_t *random_array(bool paired, int64_t top, int64_t *seed) {
    int64_t *nums = malloc(sizeof(int64_t) * 1000);
    if (paired) {
        for (int i = 0; i < 500; i++) {
            int64_t x = next_random(seed) % top + 1;
            nums[2 * i] = x;
            nums[2 * i + 1] = x;
        }
        for (int64_t i = 999; i >= 1; i--) {
            int64_t j = next_random(seed) % (i + 1);
            int64_t t = nums[i];
            nums[i] = nums[j];
            nums[j] = t;
        }
    } else {
        for (int i = 0; i < 1000; i++) nums[i] = next_random(seed) % top + 1;
    }
    return nums;
}

int main(void) {
    int64_t seed = 2206;
    static const int64_t tops[3] = {2, 5, 500};
    int64_t *arrays[200];
    for (int a = 0; a < 200; a++) arrays[a] = random_array(a % 4 != 3, tops[a % 3], &seed);
    // each odd pass punches one number of every array before the count and
    // puts it back after
    int64_t check = 0;
    for (int64_t p = 0; p < 1500; p++) {
        for (int64_t a = 0; a < 200; a++) {
            int64_t at = (p * 7 + a) % 1000;
            int64_t old = arrays[a][at];
            if (p % 2 == 1) arrays[a][at] = (p + a) % 500 + 1;
            bool paired = divide_array(arrays[a], 1000);
            arrays[a][at] = old;
            check = (check * 31 + (paired ? 2 : 1)) % 1000000007;
        }
    }
    printf("1500 passes over 200 arrays: checksum %lld\n", (long long)check);
    for (int a = 0; a < 200; a++) free(arrays[a]);
    return 0;
}
