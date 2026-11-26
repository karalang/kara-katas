// LeetCode #1449 Form Largest Integer With Digits That Add up to Target: the
// bench, a mirror of largest_number.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// the most digits each cost from 0 to target buys exactly, -1 when it buys
// none; then the digits taken from 9 down, each while what is left still
// buys one digit fewer. The answer goes in a fresh string; "0" when none.
static char *largest_number(const int *cost, int target) {
    int64_t *most = malloc(sizeof(int64_t) * (size_t)(target + 1));
    for (int t = 0; t <= target; t++) most[t] = -1;
    most[0] = 0;
    for (int t = 1; t <= target; t++) {
        for (int i = 0; i < 9; i++) {
            int c = cost[i];
            if (c <= t && most[t - c] >= 0 && most[t - c] + 1 > most[t]) most[t] = most[t - c] + 1;
        }
    }
    char *digits;
    if (most[target] < 0) {
        digits = malloc(2);
        digits[0] = '0';
        digits[1] = 0;
    } else {
        digits = malloc((size_t)most[target] + 1);
        size_t len = 0;
        int left = target;
        for (int d = 8; d >= 0; d--) {
            int c = cost[d];
            while (c <= left && most[left - c] == most[left] - 1) {
                digits[len++] = (char)('1' + d);
                left -= c;
            }
        }
        digits[len] = 0;
    }
    free(most);
    return digits;
}

int main(void) {
    // 5000 cases with the constraints' most target, 5000, each with nine
    // costs drawn from 1 to 50, each answer's digits folded to a checksum
    int64_t seed = 1449;
    int64_t check = 0;
    for (int r = 0; r < 5000; r++) {
        int cost[9];
        for (int i = 0; i < 9; i++) {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            cost[i] = (int)(1 + seed / 65536 % 50);
        }
        char *digits = largest_number(cost, 5000);
        for (char *p = digits; *p; p++) check = (check * 131 + (unsigned char)*p) % 1000000007;
        free(digits);
    }
    printf("5000 targets of 5000: checksum %lld\n", (long long)check);
    return 0;
}
