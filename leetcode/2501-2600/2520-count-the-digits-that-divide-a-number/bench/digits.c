// LeetCode #2520: Count the Digits That Divide a Number -- C mirror of the
// benchmark (digits.kara): the same numbers, passes, order and checksum.
#include <stdint.h>
#include <stdio.h>

static int64_t count_digits(int64_t num) {
    int64_t rest = num, count = 0;
    while (rest > 0) {
        if (num % (rest % 10) == 0) count++;
        rest /= 10;
    }
    return count;
}

static int64_t seed = 2520;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t nums[100000];

int main(void) {
    for (int t = 0; t < 100000; t++) {
        int64_t length = next_random() % 9 + 1, num = 0;
        for (int64_t j = 0; j < length; j++) num = num * 10 + next_random() % 9 + 1;
        nums[t] = num;
    }
    const int passes = 150;
    int64_t check = 0;
    for (int p = 0; p < passes; p++) {
        int64_t start = check % 100000;
        for (int64_t i = 0; i < 100000; i++)
            check = (check * 31 + count_digits(nums[(start + i) % 100000]) + p) % 1000000007;
    }
    printf("%d passes over 100000 numbers: checksum %lld\n", passes, (long long)check);
    return 0;
}
