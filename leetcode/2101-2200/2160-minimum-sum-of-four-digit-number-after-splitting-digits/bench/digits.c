// LeetCode #2160: Minimum Sum of Four Digit Number After Splitting Digits
// -- the benchmark's C mirror of digits.kara: the digits from the
// number's text by snprintf, sorted by qsort.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int cmp(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int64_t minimum_sum(int64_t num) {
    char text[24];
    int len = snprintf(text, sizeof text, "%lld", (long long)num);
    int64_t d[24];
    for (int i = 0; i < len; i++) {
        d[i] = text[i] - '0';
    }
    qsort(d, (size_t)len, sizeof(int64_t), cmp);
    return (d[0] * 10 + d[2]) + (d[1] * 10 + d[3]);
}

int main(void) {
    int64_t total = 0, check = 0;
    for (int64_t pass = 0; pass < 200; pass++) {
        for (int64_t k = 0; k < 9000; k++) {
            int64_t num = 1000 + (k + 37 * pass) % 9000;
            int64_t sum = minimum_sum(num);
            total += sum;
            check = (check * 31 + sum + pass) % 1000000007;
        }
    }
    printf("1800000 solves: %lld in all, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
