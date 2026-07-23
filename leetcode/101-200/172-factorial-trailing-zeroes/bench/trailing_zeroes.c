#include <stdio.h>

static long trailing_zeroes(long n) {
    long count = 0;
    long m = n / 5;
    while (m > 0) {
        count += m;
        m /= 5;
    }
    return count;
}

int main(void) {
    long limit = 35000000;
    long sink = 0;
    for (long i = 0; i < limit; i++) {
        sink += trailing_zeroes(i);
    }
    printf("%ld\n", sink);
    return 0;
}
