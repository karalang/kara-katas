// LeetCode #1323 bench, C mirror of the Kāra bench: the ★ arm (the number
// written out, its first 6 turned to a 9, and the text read back) on the 30
// numbers the constraints allow; 100000 passes over all 30, each pass
// starting at a place chosen by the checksum so far and folding every
// answer plus the pass into it. Each call writes the number into a fresh
// buffer, a `malloc`, as the Kāra arm makes fresh strings.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int32_t maximum69_number(int32_t num) {
    char *text = malloc(16);
    snprintf(text, 16, "%d", num);
    for (char *p = text; *p; p++) {
        if (*p == '6') {
            *p = '9';
            break;
        }
    }
    int32_t got = (int32_t)strtol(text, NULL, 10);
    free(text);
    return got;
}

int main(void) {
    int32_t nums[30];
    int count = 0;
    for (int digits = 1; digits <= 4; digits++) {
        for (int pattern = 0; pattern < 1 << digits; pattern++) {
            int32_t num = 0;
            for (int k = 0; k < digits; k++) num = num * 10 + (((pattern >> k) & 1) == 1 ? 9 : 6);
            nums[count++] = num;
        }
    }
    int64_t check = 0;
    for (int64_t pass = 0; pass < 100000; pass++) {
        int64_t start = check % 30;
        for (int64_t k = 0; k < 30; k++) {
            int64_t got = maximum69_number(nums[(start + k) % 30]);
            check = (check * 31 + got + pass) % 1000000007;
        }
    }
    printf("100000 passes over the 30 numbers: checksum %lld\n", (long long)check);
    return 0;
}
