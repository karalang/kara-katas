// LeetCode #2231: Largest Number After Digit Swaps by Parity -- the
// benchmark's C mirror of parity.kara: the number written out with
// snprintf, each parity's digits sorted by qsort and taken from the
// largest down into that parity's places.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int by_value(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int64_t largest_integer(int64_t num) {
    char text[24];
    int n = snprintf(text, sizeof text, "%lld", (long long)num);
    int64_t digits[24], odd[24], even[24];
    int no = 0, ne = 0;
    for (int i = 0; i < n; i++) {
        digits[i] = text[i] - 48;
        if (digits[i] % 2 == 1) odd[no++] = digits[i];
        else even[ne++] = digits[i];
    }
    qsort(odd, (size_t)no, sizeof(int64_t), by_value);
    qsort(even, (size_t)ne, sizeof(int64_t), by_value);
    int64_t largest = 0;
    for (int i = 0; i < n; i++) {
        int64_t next = digits[i] % 2 == 1 ? odd[--no] : even[--ne];
        largest = largest * 10 + next;
    }
    return largest;
}

static int64_t seed = 2231;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide_random(void) {
    int64_t high = next_random();
    return high * 32768 + next_random();
}

int main(void) {
    int64_t *nums = malloc(sizeof(int64_t) * 100000);
    for (int i = 0; i < 100000; i++) nums[i] = wide_random() % 1000000000 + 1;
    int64_t check = 0;
    for (int r = 0; r < 20; r++) {
        // punch: one num drawn again before each pass over all of them
        int64_t at = wide_random() % 100000;
        nums[at] = wide_random() % 1000000000 + 1;
        for (int i = 0; i < 100000; i++) check = (check * 31 + largest_integer(nums[i])) % 1000000007;
    }
    printf("20 passes over 10^5 nums: checksum %lld\n", (long long)check);
    free(nums);
    return 0;
}
