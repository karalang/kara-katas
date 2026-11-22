// LeetCode #2702: Minimum Operations to Make Numbers Non-positive -- the
// bench (nonpositive.kara in C): a binary search on the count, each
// trial summing the extra shares the numbers still above t * y need.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t min_operations(const int64_t *nums, int n, int64_t x, int64_t y) {
    int64_t top = nums[0];
    for (int i = 1; i < n; i++) if (nums[i] > top) top = nums[i];
    int64_t low = 0, high = top / y + 1;
    while (low < high) {
        int64_t t = (low + high) / 2, need = 0;
        for (int i = 0; i < n; i++) {
            int64_t v = nums[i];
            if (v > t * y) {
                need += (v - t * y + x - y - 1) / (x - y);
                if (need > t) break;
            }
        }
        if (need <= t) high = t;
        else low = t + 1;
    }
    return low;
}

static int64_t seed = 2702;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

int main(void) {
    const int arrays = 100, n = 10000, rounds = 5;
    int64_t *nums = malloc(sizeof(int64_t) * arrays * n);
    int64_t xs[100], ys[100];
    for (int a = 0; a < arrays; a++) {
        for (int i = 0; i < n; i++) nums[a * n + i] = wide() % 1000000000 + 1;
        ys[a] = next_random() % 1000 + 1;
        xs[a] = ys[a] + wide() % 1000000 + 1;
    }
    int64_t sum = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int a = 0; a < arrays; a++) {
            int64_t t = min_operations(nums + a * n, n, xs[a], ys[a]);
            sum += t;
            check = (check * 31 + t + r) % 1000000007;
        }
    }
    printf("%d arrays of %d numbers up to 1000000000, %d rounds: operations sum to %lld, checksum %lld\n", arrays, n, rounds, (long long)sum, (long long)check);
    free(nums);
    return 0;
}
