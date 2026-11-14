// LeetCode #2148: Count Elements With Strictly Smaller and Greater
// Elements -- the benchmark's C mirror of elements.kara.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t count_elements(const int64_t *nums, int64_t n) {
    int64_t low = nums[0];
    int64_t high = nums[0];
    for (int64_t i = 1; i < n; i++) {
        if (nums[i] < low) low = nums[i];
        if (nums[i] > high) high = nums[i];
    }
    int64_t count = 0;
    for (int64_t i = 0; i < n; i++) {
        if (low < nums[i] && nums[i] < high) count++;
    }
    return count;
}

static int64_t seed = 2148;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int64_t *pool = malloc(sizeof(int64_t) * 100000);
    for (int i = 0; i < 100000; i++) {
        pool[i] = next_random() * 7 % 200001 - 100000;
    }
    int64_t total = 0;
    int64_t check = 0;
    for (int64_t round = 0; round < 200000; round++) {
        int64_t at = next_random() % 100000;
        pool[at] = next_random() % 21 - 10;
        int64_t from = next_random() % (100000 - 100);
        int64_t *nums = malloc(sizeof(int64_t) * 100);
        memcpy(nums, pool + from, sizeof(int64_t) * 100);
        int64_t count = count_elements(nums, 100);
        free(nums);
        total += count;
        check = (check * 31 + count + round) % 1000000007;
    }
    printf("200000 counts: %lld counted in all, checksum %lld\n", (long long)total, (long long)check);
    free(pool);
    return 0;
}
