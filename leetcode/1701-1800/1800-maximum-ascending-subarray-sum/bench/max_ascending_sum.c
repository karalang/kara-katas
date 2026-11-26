// LeetCode #1800: Maximum Ascending Subarray Sum -- the bench in C: the ★
// arm over 4000 random lists of 100 numbers built once, 400000 calls.
#include <stdint.h>
#include <stdio.h>

static int32_t max_ascending_sum(const int32_t *nums, int n) {
    int32_t run = nums[0];
    int32_t best = run;
    for (int i = 1; i < n; i++) {
        if (nums[i] > nums[i - 1]) {
            run += nums[i];
        } else {
            run = nums[i];
        }
        if (run > best) best = run;
    }
    return best;
}

static int64_t seed = 1800;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int32_t lists[4000][100];
    for (int l = 0; l < 4000; l++)
        for (int x = 0; x < 100; x++) lists[l][x] = (int32_t)(1 + next_random() % 100);
    int64_t check = 0;
    for (int64_t call = 0; call < 400000; call++) {
        check = (check * 31 + max_ascending_sum(lists[(check + call) % 4000], 100)) % 1000000007;
    }
    printf("400000 calls over 4000 lists of 100 numbers: checksum %lld\n", (long long)check);
    return 0;
}
