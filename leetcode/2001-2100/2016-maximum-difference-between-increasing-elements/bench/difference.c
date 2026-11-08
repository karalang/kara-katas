// LeetCode #2016: Maximum Difference Between Increasing Elements -- the ★
// arm's benchmark, a mirror of difference.kara.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

static int64_t maximum_difference(const int64_t *nums, int n) {
    int64_t smallest = nums[0], best = -1;
    for (int i = 1; i < n; i++) {
        int64_t x = nums[i];
        if (x > smallest && x - smallest > best) best = x - smallest;
        if (x < smallest) smallest = x;
    }
    return best;
}

static int64_t seed = 2016;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    enum { ARRAYS = 1000, N = 10000 };
    int64_t *arrays = malloc((size_t)ARRAYS * N * sizeof(int64_t));
    for (int a = 0; a < ARRAYS; a++) {
        int64_t fall = a % 11, *nums = arrays + (size_t)a * N;
        for (int i = 0; i < N; i++) {
            if (i > 0 && next_random() % 10 < fall) {
                int64_t v = nums[i - 1] - next_random() % 1000;
                nums[i] = v < 1 ? 1 : v;
            } else {
                int64_t hi = next_random();
                nums[i] = (hi * 32768 + next_random()) % 1000000000 + 1;
            }
        }
    }
    int64_t calls = 0, sum = 0, check = 0;
    for (int r = 0; r < 10; r++) {
        for (int a = 0; a < ARRAYS; a++) {
            int64_t answer = maximum_difference(arrays + (size_t)a * N, N);
            calls++;
            sum += answer;
            check = (check * 31 + answer + 1) % 1000000007;
        }
    }
    free(arrays);
    printf("%lld calls: sum %lld, checksum %lld\n", (long long)calls, (long long)sum, (long long)check);
    return 0;
}
