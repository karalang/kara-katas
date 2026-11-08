// LeetCode #2012: Sum of Beauty in the Array -- the ★ arm's benchmark, a
// mirror of beauty.kara. The suffix minima are allocated per call, as the
// Kāra program's are.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t sum_of_beauties(const int64_t *nums, int64_t n) {
    int64_t *min_after = malloc(n * sizeof(int64_t));
    min_after[n - 1] = nums[n - 1];
    for (int64_t i = n - 2; i >= 0; i--)
        min_after[i] = min_after[i + 1] < nums[i] ? min_after[i + 1] : nums[i];
    int64_t max_before = nums[0], total = 0;
    for (int64_t i = 1; i < n - 1; i++) {
        if (max_before < nums[i] && nums[i] < min_after[i + 1]) total += 2;
        else if (nums[i - 1] < nums[i] && nums[i] < nums[i + 1]) total += 1;
        if (nums[i] > max_before) max_before = nums[i];
    }
    free(min_after);
    return total;
}

static int64_t seed = 2012;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    static int64_t arrays[1000][2000];
    for (int a = 0; a < 1000; a++) {
        int64_t rise = a % 11;
        for (int i = 0; i < 2000; i++) {
            if (i > 0 && next_random() % 10 < rise) {
                int64_t v = arrays[a][i - 1] + next_random() % 3 + 1;
                arrays[a][i] = v < 100000 ? v : 100000;
            } else {
                arrays[a][i] = next_random() % 100000 + 1;
            }
        }
    }
    int64_t calls = 0, sum = 0, check = 0;
    for (int r = 0; r < 5; r++) {
        for (int a = 0; a < 1000; a++) {
            int64_t answer = sum_of_beauties(arrays[a], 2000);
            calls++;
            sum += answer;
            check = (check * 31 + answer) % 1000000007;
        }
    }
    printf("%lld calls: sum %lld, checksum %lld\n", (long long)calls, (long long)sum, (long long)check);
    return 0;
}
