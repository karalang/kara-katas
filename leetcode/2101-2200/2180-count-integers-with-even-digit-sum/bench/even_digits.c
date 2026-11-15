// LeetCode #2180: Count Integers With Even Digit Sum -- the benchmark's
// C mirror of even_digits.kara.

#include <stdio.h>

static long long count_even(long long num) {
    long long count = 0;
    for (long long x = 1; x <= num; x++) {
        long long total = 0;
        long long rest = x;
        while (rest > 0) {
            total += rest % 10;
            rest /= 10;
        }
        if (total % 2 == 0) count++;
    }
    return count;
}

static long long seed = 2180;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    long long check = 0;
    for (int r = 0; r < 200000; r++) {
        long long num = next_random() % 1000 + 1;
        check = (check * 31 + count_even(num)) % 1000000007;
    }
    printf("200000 solves: checksum %lld\n", check);
    return 0;
}
