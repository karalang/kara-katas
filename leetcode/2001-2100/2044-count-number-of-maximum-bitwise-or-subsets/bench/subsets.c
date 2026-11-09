// LeetCode #2044: Count Number of Maximum Bitwise-OR Subsets -- the ★ arm
// in C, the same algorithm and workload as subsets.kara: the target is the
// OR of every value, and a take-or-skip search counts the subsets that
// reach it.
#include <stdint.h>
#include <stdio.h>

static int64_t count_from(const int64_t *nums, int64_t n, int64_t i, int64_t acc, int64_t target) {
    if (i == n) return acc == target ? 1 : 0;
    return count_from(nums, n, i + 1, acc | nums[i], target) + count_from(nums, n, i + 1, acc, target);
}

static int64_t count_max_or_subsets(const int64_t *nums, int64_t n) {
    int64_t target = 0;
    for (int64_t i = 0; i < n; i++) target |= nums[i];
    return count_from(nums, n, 0, 0, target);
}

static int64_t seed = 2044;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int64_t arrays[2000][16];
    const int64_t tops[4] = {100000, 1024, 16, 2};
    for (int r = 0; r < 2000; r++)
        for (int i = 0; i < 16; i++) arrays[r][i] = next_random() % tops[r % 4] + 1;
    int64_t calls = 0, sum = 0, check = 0;
    for (int r = 0; r < 2000; r++) {
        int64_t answer = count_max_or_subsets(arrays[r], 16);
        calls++;
        sum += answer;
        check = (check * 31 + answer) % 1000000007;
    }
    printf("%lld calls: sum %lld, checksum %lld\n", (long long)calls, (long long)sum, (long long)check);
    return 0;
}
