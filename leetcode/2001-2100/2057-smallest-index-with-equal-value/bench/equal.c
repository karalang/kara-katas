// LeetCode #2057: Smallest Index With Equal Value -- C mirror of the ★
// arm's benchmark (equal.kara): the same 1000000 arrays drawn into one
// buffer, each answered by walking its indices from the front.
#include <stdint.h>
#include <stdio.h>

static int64_t seed = 2057;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t smallest_equal(const int64_t *nums, int64_t n) {
    for (int64_t i = 0; i < n; i++) {
        if (i % 10 == nums[i]) {
            return i;
        }
    }
    return -1;
}

int main(void) {
    int64_t nums[100];
    int64_t found = 0, total = 0, check = 0;
    for (int t = 0; t < 1000000; t++) {
        int64_t n = next_random() % 100 + 1;
        int64_t rare = next_random() % 20 + 1;
        for (int64_t i = 0; i < n; i++) {
            int64_t d = next_random() % 10;
            nums[i] = (d == i % 10 && next_random() % rare != 0) ? (d + 1) % 10 : d;
        }
        int64_t at = smallest_equal(nums, n);
        if (at >= 0) {
            found++;
        }
        total += at;
        check = (check * 31 + at + 2) % 1000000007;
    }
    printf("1000000 arrays: %lld found, sum %lld, checksum %lld\n", (long long)found, (long long)total, (long long)check);
    return 0;
}
