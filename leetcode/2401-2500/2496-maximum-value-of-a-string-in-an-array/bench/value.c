// LeetCode #2496: Maximum Value of a String in an Array -- C mirror of the
// benchmark (value.kara): the same lists, passes and checksum; each string
// a NUL-ended array of 10 bytes, the checksum written with snprintf.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

static int64_t seed = 2496;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static char lists[2000][100][10];

static int64_t maximum_value(char (*strs)[10], int count) {
    int64_t best = 0;
    for (int i = 0; i < count; i++) {
        int64_t number = 0;
        int digits = 1;
        int64_t length = 0;
        for (const char *c = strs[i]; *c; c++, length++) {
            if (*c >= '0' && *c <= '9') {
                number = number * 10 + (*c - '0');
            } else {
                digits = 0;
            }
        }
        int64_t worth = digits ? number : length;
        if (worth > best) best = worth;
    }
    return best;
}

int main(void) {
    const int64_t passes = 90;
    for (int l = 0; l < 2000; l++) {
        for (int i = 0; i < 100; i++) {
            int64_t length = next_random() % 9 + 1;
            for (int64_t j = 0; j < length; j++) {
                int64_t k = next_random();
                lists[l][i][j] = k % 2 == 0 ? (char)('0' + k / 2 % 10) : (char)('a' + k / 2 % 26);
            }
            lists[l][i][length] = 0;
        }
    }
    int64_t check = 0;
    char was[10];
    for (int64_t p = 0; p < passes; p++) {
        for (int l = 0; l < 2000; l++) {
            int64_t at = check % 100;
            memcpy(was, lists[l][at], 10);
            snprintf(lists[l][at], 10, "%lld", (long long)(check % 1000000000));
            check = (check * 31 + maximum_value(lists[l], 100) + p) % 1000000007;
            memcpy(lists[l][at], was, 10);
        }
    }
    printf("%lld passes over 2000 lists of 100: checksum %lld\n", (long long)passes, (long long)check);
    return 0;
}
