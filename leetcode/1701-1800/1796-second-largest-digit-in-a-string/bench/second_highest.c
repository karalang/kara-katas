// LeetCode #1796: Second Largest Digit in a String -- the bench in C: the ★
// arm over 1000 random strings of 100 characters built once, 1000000 calls.
#include <stdint.h>
#include <stdio.h>

static int32_t second_highest(const char *s) {
    int32_t first = -1, second = -1;
    for (; *s; s++) {
        if (*s >= '0' && *s <= '9') {
            int32_t d = *s - '0';
            if (d > first) {
                second = first;
                first = d;
            } else if (d < first && d > second) {
                second = d;
            }
        }
    }
    return second;
}

static int64_t seed = 1796;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static char texts[1000][101];
    for (int t = 0; t < 1000; t++) {
        int64_t digits = 1 + next_random() % 9;
        for (int x = 0; x < 100; x++) {
            if (next_random() % 10 < digits) {
                texts[t][x] = (char)('0' + next_random() % 10);
            } else {
                texts[t][x] = "abcdef"[next_random() % 6];
            }
        }
        texts[t][100] = 0;
    }
    int64_t check = 0;
    for (int64_t call = 0; call < 1000000; call++) {
        check = (check * 31 + second_highest(texts[(check + call) % 1000]) + 1) % 1000000007;
    }
    printf("1000000 calls over 1000 strings: checksum %lld\n", (long long)check);
    return 0;
}
