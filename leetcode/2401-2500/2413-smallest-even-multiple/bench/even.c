// LeetCode #2413: Smallest Even Multiple -- the bench, the ★ arm in C: n
// when n is even, and 2 n when it is odd.

#include <stdint.h>
#include <stdio.h>

static int64_t smallest_even_multiple(int64_t n) { return n % 2 == 0 ? n : 2 * n; }

int main(void) {
    int64_t check = 0;
    for (int64_t p = 0; p < 200000; p++)
        for (int64_t n = 1; n <= 150; n++) check = (check * 31 + smallest_even_multiple(n) + p) % 1000000007;
    printf("200000 passes over n from 1 to 150: checksum %lld\n", (long long)check);
    return 0;
}
