// benchmark's C mirror of hills.kara (LeetCode #2210, the ★ arm): one pass
// keeping the last number that differs from the current one, a run
// counted once, at its end.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t count_hill_valley(const int64_t *nums, long n) {
    int64_t count = 0;
    int64_t left = nums[0];
    for (long i = 1; i < n - 1; i++) {
        if (nums[i] == nums[i + 1]) continue;
        int64_t right = nums[i + 1];
        if ((nums[i] > left && nums[i] > right) || (nums[i] < left && nums[i] < right)) count++;
        if (nums[i] != left) left = nums[i];
    }
    return count;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 2210;
    const int64_t tops[3] = {3, 10, 100};
    int64_t *arrays = malloc(sizeof(int64_t) * 2000 * 100);
    for (long a = 0; a < 2000; a++)
        for (long i = 0; i < 100; i++) arrays[a * 100 + i] = next_random(&seed) % tops[a % 3] + 1;
    // every array counted once per pass
    int64_t check = 0;
    for (int64_t p = 0; p < 100; p++)
        for (long a = 0; a < 2000; a++)
            check = (check * 31 + count_hill_valley(arrays + a * 100, 100) + p) % 1000000007;
    printf("100 passes over 2000 arrays: checksum %lld\n", (long long)check);
    free(arrays);
    return 0;
}
