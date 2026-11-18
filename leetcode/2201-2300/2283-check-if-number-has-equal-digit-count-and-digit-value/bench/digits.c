// LeetCode #2283: Check if Number Has Equal Digit Count and Digit Value
// -- the bench, the ★ arm. Each string is a NUL-terminated array of at
// most 10 digits.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static bool digit_count(const char *num) {
    int64_t counts[10] = {0};
    int64_t n = (int64_t)strlen(num);
    for (int64_t k = 0; k < n; k++) counts[num[k] - '0']++;
    for (int64_t i = 0; i < n; i++) {
        if (counts[i] != num[i] - '0') return false;
    }
    return true;
}

// ---- bench harness ---------------------------------------------------------

static int64_t seed = 2283;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    static const char *known[7] = {"1210",     "2020",      "21200",     "3211000",
                                   "42101000", "521001000", "6210001000"};
    char(*nums)[11] = malloc(100000 * sizeof *nums);
    for (int k = 0; k < 100000; k++) {
        if (k % 8 == 0) {
            strcpy(nums[k], known[next_random() % 7]);
        } else {
            int64_t n = next_random() % 10 + 1;
            int64_t high = (n < 9 ? n : 9) + 1;
            for (int64_t j = 0; j < n; j++) nums[k][j] = (char)('0' + next_random() % high);
            nums[k][n] = '\0';
        }
    }
    int64_t check = 0;
    for (int t = 0; t < 100; t++) {
        int64_t held = 0;
        for (int k = 0; k < 100000; k++) {
            if (digit_count(nums[k])) held++;
        }
        check = (check * 31 + held) % 1000000007;
    }
    free(nums);
    printf("100 passes over 10^5 strings: checksum %lld\n", (long long)check);
    return 0;
}
