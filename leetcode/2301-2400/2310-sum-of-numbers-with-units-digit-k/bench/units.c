// LeetCode #2310: Sum of Numbers With Units Digit K -- the bench, the ★
// arm in C. The least count from 1 to 10 whose multiple of k fits within
// num and leaves a multiple of 10.
#include <stdint.h>
#include <stdio.h>

static int64_t minimum_numbers(int64_t num, int64_t k) {
    if (num == 0) return 0;
    for (int64_t n = 1; n <= 10; n++)
        if (n * k <= num && (num - n * k) % 10 == 0) return n;
    return -1;
}

int main(void) {
    int64_t check = 0;
    for (int64_t p = 0; p < 300; p++)
        for (int64_t num = 0; num <= 3000; num++)
            for (int64_t k = 0; k < 10; k++) check = (check * 31 + minimum_numbers(num, k) + 1 + p) % 1000000007;
    printf("300 passes over 3001 sums and 10 digits: checksum %lld\n", (long long)check);
    return 0;
}
