#include <stdio.h>

static long col_checksum(long n) {
    long x = n, acc = 0;
    while (x > 0) {
        x -= 1; // bijective base-26: shift to 0-based digit
        acc += 65 + (x % 26); // 'A' = 65
        x /= 26;
    }
    return acc;
}

int main(void) {
    long limit = 50000000, sink = 0;
    for (long n = 1; n <= limit; n++) {
        sink += col_checksum(n);
    }
    printf("%ld\n", sink);
    return 0;
}
