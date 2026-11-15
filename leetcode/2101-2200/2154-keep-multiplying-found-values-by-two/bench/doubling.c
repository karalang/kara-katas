// LeetCode #2154: Keep Multiplying Found Values by Two -- the benchmark's
// C mirror of doubling.kara, over a pointer and a length, the numbers
// collected into an open-addressing hash set.

#include <stdio.h>
#include <stdlib.h>

#define CAP 4096

static long long slot_of(long long x) {
    unsigned long long h = (unsigned long long)x * 0x9E3779B97F4A7C15ULL;
    return (long long)(h >> 52);
}

static long long find_final_value(const long long *nums, long long n, long long original) {
    long long *table = calloc(CAP, sizeof(long long));
    for (long long i = 0; i < n; i++) {
        long long s = slot_of(nums[i]);
        while (table[s] != 0 && table[s] != nums[i]) s = (s + 1) & (CAP - 1);
        table[s] = nums[i];
    }
    long long value = original;
    for (;;) {
        long long s = slot_of(value);
        while (table[s] != 0 && table[s] != value) s = (s + 1) & (CAP - 1);
        if (table[s] != value) break;
        value *= 2;
    }
    free(table);
    return value;
}

static long long seed = 2154;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    long long *row = malloc(400000 * sizeof(long long));
    for (int i = 0; i < 400000; i++) row[i] = next_random() % 1000 + 1;
    long long check = 0;
    for (int r = 0; r < 20000; r++) {
        long long a = next_random();
        long long b = next_random();
        long long start = (a * 32768 + b) % 399001;
        long long original = next_random() % 1000 + 1;
        long long value = find_final_value(row + start, 1000, original);
        check = (check * 31 + value) % 1000000007;
    }
    printf("20000 solves: checksum %lld\n", check);
    free(row);
    return 0;
}
