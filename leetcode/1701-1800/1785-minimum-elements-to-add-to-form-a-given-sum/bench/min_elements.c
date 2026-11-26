// LeetCode #1785: Minimum Elements to Add to Form a Given Sum -- the bench
// in C, mirroring min_elements.kara: the gap over the limit, rounded up.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int32_t min_elements(const int32_t *nums, int n, int32_t limit, int32_t goal) {
    int64_t sum = 0;
    for (int i = 0; i < n; i++) sum += nums[i];
    int64_t gap = (int64_t)goal - sum;
    if (gap < 0) gap = -gap;
    return (int32_t)((gap + limit - 1) / limit);
}

static int64_t seed = 1785;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int32_t *lists = malloc(sizeof(int32_t) * 4000 * 100);
    for (int k = 0; k < 4000; k++) {
        for (int i = 0; i < 100; i++) {
            int64_t a = next_random();
            int64_t b = next_random();
            lists[k * 100 + i] = (int32_t)((a * 32768 + b) % 2000001 - 1000000);
        }
    }
    int64_t check = 0;
    for (int64_t call = 0; call < 6000000; call++) {
        const int32_t *nums = lists + ((check + call) % 4000) * 100;
        int64_t limit = 1 + (check + call) % 1000000;
        int64_t goal = check % 2000000001 - 1000000000;
        check = (check * 31 + min_elements(nums, 100, (int32_t)limit, (int32_t)goal)) % 1000000007;
    }
    printf("6000000 calls over 4000 lists: checksum %lld\n", (long long)check);
    free(lists);
    return 0;
}
