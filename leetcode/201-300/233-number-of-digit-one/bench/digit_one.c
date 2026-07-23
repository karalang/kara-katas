#include <stdio.h>

static long count_digit_one(long n) {
    if (n < 0) return 0;
    long count = 0;
    long pos = 1;
    while (pos <= n) {
        long high = n / (pos * 10);
        long cur = (n / pos) % 10;
        long low = n % pos;
        if (cur == 0) {
            count += high * pos;
        } else if (cur == 1) {
            count += high * pos + low + 1;
        } else {
            count += (high + 1) * pos;
        }
        pos *= 10;
    }
    return count;
}

int main(void) {
    long limit = 6000000;
    long sink = 0;
    for (long i = 0; i < limit; i++) {
        sink += count_digit_one(i);
    }
    printf("%ld\n", sink);
    return 0;
}
