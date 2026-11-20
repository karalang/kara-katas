// LeetCode #1748: Sum of Unique Elements -- the bench (unique.kara in C):
// one pass with a state per value.
#include <stdint.h>
#include <stdio.h>

enum { COUNT = 50000, ROUNDS = 10, N = 100 };

static int32_t sum_of_unique(const int32_t *nums, int64_t n) {
    int64_t seen[101] = {0};
    int32_t sum = 0;
    for (int64_t k = 0; k < n; k++) {
        int32_t x = nums[k];
        if (seen[x] == 0)
            sum += x;
        else if (seen[x] == 1)
            sum -= x;
        seen[x] = seen[x] + 1 < 2 ? seen[x] + 1 : 2;
    }
    return sum;
}

static int64_t seed = 1748;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int32_t arrays[COUNT][N];
    for (int c = 0; c < COUNT; c++)
        for (int64_t i = 0; i < N; i++) arrays[c][i] = (int32_t)(next_random() % 100 + 1);
    int64_t sum = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int c = 0; c < COUNT; c++) {
            int64_t answer = sum_of_unique(arrays[c], N);
            sum += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    printf("%d arrays of %d values, %d rounds: unique sums add to %lld, checksum %lld\n", COUNT, N, ROUNDS, (long long)sum, (long long)check);
    return 0;
}
