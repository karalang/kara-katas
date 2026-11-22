// LeetCode #2750: Ways to Split Array Into Good Subarrays -- the bench
// (splits.kara in C): the product of the distances between neighbouring
// 1s, mod 10^9 + 7.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define MOD 1000000007LL
#define SIZE 100000

static int64_t number_of_good_subarray_splits(const int64_t *nums, int64_t n) {
    int64_t ways = 1, last = -1;
    for (int64_t i = 0; i < n; i++) {
        if (nums[i] == 1) {
            if (last >= 0) ways = ways * (i - last) % MOD;
            last = i;
        }
    }
    return last < 0 ? 0 : ways;
}

static int64_t seed = 2750;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int count = 50, rounds = 20;
    int64_t *arrays = malloc(sizeof(int64_t) * count * SIZE);
    for (int k = 0; k < count; k++) {
        int64_t percent = next_random() % 30 + 1;
        for (int i = 0; i < SIZE; i++) arrays[(int64_t)k * SIZE + i] = next_random() % 100 < percent ? 1 : 0;
    }
    int64_t sum = 0, check = 0;
    for (int r = 0; r < rounds; r++)
        for (int k = 0; k < count; k++) {
            int64_t ways = number_of_good_subarray_splits(arrays + (int64_t)k * SIZE, SIZE);
            sum += ways;
            check = (check * 31 + ways + r) % 1000000007;
        }
    printf("%d arrays of 100000, %d rounds: ways sum to %lld, checksum %lld\n", count, rounds, (long long)sum, (long long)check);
    free(arrays);
    return 0;
}
