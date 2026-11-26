// LeetCode #1780: Check if Number is a Sum of Powers of Three -- the bench in
// C, mirroring check_powers_of_three.kara: base-3 digits read off from the
// lowest, on every n from 1 to 10^7, five rounds over.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

static bool check_powers_of_three(int n) {
    int rest = n;
    while (rest > 0) {
        if (rest % 3 == 2) return false;
        rest /= 3;
    }
    return true;
}

int main(void) {
    int64_t count = 0, check = 0;
    for (int64_t round = 0; round < 5; round++) {
        for (int n = 1; n < 10000001; n++) {
            if (check_powers_of_three(n)) {
                count += 1;
                check = (check * 31 + n + round) % 1000000007;
            }
        }
    }
    printf("5 rounds of 1 to 10000000: %lld sums, checksum %lld\n", (long long)count, (long long)check);
    return 0;
}
