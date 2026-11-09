// Benchmark: LeetCode #1085 Sum of Digits in the Minimum Number -- the ★
// arm. Mirrors sum_of_digits.kara, .rs, .py and go-seq/.
#include <stdint.h>
#include <stdio.h>

static int64_t sum_of_digits(const int64_t *nums, int n) {
    int64_t least = nums[0];
    for (int i = 0; i < n; i++)
        if (nums[i] < least) least = nums[i];
    int64_t sum = 0;
    while (least > 0) {
        sum += least % 10;
        least /= 10;
    }
    return sum % 2 == 0 ? 1 : 0;
}

static int64_t seed = 1085;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t arrays[2000][100];

int main(void) {
    int64_t rounds = 5000;
    for (int t = 0; t < 2000; t++) {
        int64_t low = next_random() % 100 + 1;
        for (int j = 0; j < 100; j++) arrays[t][j] = low + next_random() % (101 - low);
    }
    int64_t ones = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t i = 0; i < 2000; i++) {
            int64_t a = sum_of_digits(arrays[(r * 7 + i) % 2000], 100);
            ones += a;
            check = (check * 31 + a + i) % 1000000007;
        }
    }
    printf("%lld rounds over 2000 arrays of 100 values: %lld answer 1, checksum %lld\n", (long long)rounds,
           (long long)ones, (long long)check);
    return 0;
}
