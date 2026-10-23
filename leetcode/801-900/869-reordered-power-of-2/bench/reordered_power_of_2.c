// LeetCode #869: Reordered Power of 2 -- C mirror of the bench program
// (the ★ arm, digit counts), with the counts in arrays on the stack.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

static void digit_counts(int64_t x, int64_t counts[10]) {
    memset(counts, 0, 10 * sizeof(int64_t));
    for (int64_t rest = x; rest > 0; rest /= 10) counts[rest % 10]++;
}

static int reordered_power_of_2(int64_t n) {
    int64_t want[10], got[10];
    digit_counts(n, want);
    int64_t power = 1;
    for (int k = 0; k < 30; k++) {
        digit_counts(power, got);
        if (memcmp(got, want, sizeof want) == 0) return 1;
        power *= 2;
    }
    return 0;
}

int main(void) {
    int64_t limit = 1000000;
    int64_t count = 0;
    int64_t check = 0;
    for (int64_t n = 1; n <= limit; n++) {
        if (reordered_power_of_2(n)) {
            count++;
            check = (check * 31 + n) % 1000000007;
        }
    }
    printf("n from 1 to %lld: %lld true, checksum %lld\n", (long long)limit, (long long)count,
           (long long)check);
    return 0;
}
