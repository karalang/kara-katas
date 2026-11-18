// LeetCode #2259: Remove Digit From Number to Maximize Result -- C mirror
// of the ★ arm: the first occurrence followed by a larger digit, else the
// last occurrence. Same workload and checksum as remove.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t seed = 2259;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

// writes the number without the chosen digit into out, returns its length
static size_t remove_digit(const char *number, size_t len, char digit, char *out) {
    size_t last = 0;
    for (size_t i = 0; i < len; i++) {
        if (number[i] == digit) {
            last = i;
            if (i + 1 < len && number[i + 1] > digit) break;
        }
    }
    memcpy(out, number, last);
    memcpy(out + last, number + last + 1, len - last - 1);
    return len - 1;
}

int main(void) {
    enum { POOL = 1000000, LEN = 100 };
    char *pool = malloc(POOL);
    for (int i = 0; i < POOL; i++) pool[i] = (char)('1' + next_random() % 9);
    char number[LEN], out[LEN];
    int64_t check = 0;
    for (int t = 0; t < 1000000; t++) {
        int64_t hi = next_random();
        int64_t at = (hi * 32768 + next_random()) % (POOL - LEN);
        memcpy(number, pool + at, LEN);
        size_t n = remove_digit(number, LEN, number[50], out);
        for (size_t k = 0; k < n; k++) check = (check * 131 + (unsigned char)out[k]) % 1000000007;
    }
    printf("10^6 numbers of 100 digits: checksum %lld\n", (long long)check);
    free(pool);
    return 0;
}
