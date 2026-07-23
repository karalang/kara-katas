#include <stdio.h>

static int is_power_of_two(long n) {
    if (n <= 0) return 0;
    return (n & (n - 1)) == 0;
}

int main(void) {
    long n = 130000000;
    long mask = 1023;
    long state = 12345;
    long sink = 0;
    for (long i = 0; i < n; i++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long v = state & mask;
        if (is_power_of_two(v)) sink++;
    }
    printf("%ld\n", sink);
    return 0;
}
