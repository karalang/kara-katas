#include <stdio.h>

static long reverse_bits(long n) {
    long result = 0;
    long x = n;
    for (long i = 0; i < 32; i++) {
        result = (result << 1) | (x & 1);
        x >>= 1;
    }
    return result;
}

int main(void) {
    long count = 8000000;
    long state = 12345;
    long sink = 0;
    for (long i = 0; i < count; i++) {
        state = (state * 1103515245 + 12345) & 2147483647;
        sink += reverse_bits(state);
    }
    printf("%ld\n", sink);
    return 0;
}
