// LeetCode #2165: Smallest Value of the Rearranged Number -- the
// benchmark's C mirror of smallest.kara: the digits from snprintf's text,
// sorted by qsort.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int rising(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int falling(const void *a, const void *b) { return rising(b, a); }

static int64_t smallest_number(int64_t num) {
    char text[24];
    int64_t digits[24];
    int n = snprintf(text, sizeof text, "%lld", (long long)llabs(num));
    for (int i = 0; i < n; i++) digits[i] = text[i] - '0';
    if (num < 0) {
        qsort(digits, (size_t)n, sizeof(int64_t), falling);
    } else {
        qsort(digits, (size_t)n, sizeof(int64_t), rising);
        for (int i = 0; i < n; i++) {
            if (digits[i] != 0) {
                int64_t t = digits[0];
                digits[0] = digits[i];
                digits[i] = t;
                break;
            }
        }
    }
    int64_t size = 0;
    for (int i = 0; i < n; i++) size = size * 10 + digits[i];
    return num < 0 ? -size : size;
}

static int64_t seed = 2165;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int64_t nums[1000];
    for (int k = 0; k < 1000; k++) {
        int64_t length = next_random() % 14 + 1;
        int64_t num = 0;
        for (int64_t i = 0; i < length; i++) num = num * 10 + next_random() % 10;
        if (next_random() % 2 == 1) num = -num;
        nums[k] = num;
    }
    int64_t check = 0;
    for (int r = 0; r < 1000; r++) {
        for (int k = 0; k < 1000; k++) {
            nums[k] = nums[k] + next_random() % 2001 - 1000;
            int64_t s = smallest_number(nums[k]);
            check = (check * 31 + s % 1000000007 + 1000000007) % 1000000007;
        }
    }
    printf("1000000 solves: checksum %lld\n", (long long)check);
    return 0;
}
