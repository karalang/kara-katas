#include <stdio.h>

static long sq_digit_sum(long n) {
    long total = 0;
    long x = n;
    while (x > 0) {
        long d = x % 10;
        total += d * d;
        x /= 10;
    }
    return total;
}

static int is_happy(long n) {
    long slow = n;
    long fast = sq_digit_sum(n);
    while (fast != 1 && slow != fast) {
        slow = sq_digit_sum(slow);
        fast = sq_digit_sum(sq_digit_sum(fast));
    }
    return fast == 1;
}

int main(void) {
    long limit = 4000000;
    long sink = 0;
    for (long i = 1; i < limit; i++) {
        if (is_happy(i)) {
            sink += 1;
        }
    }
    printf("%ld\n", sink);
    return 0;
}
