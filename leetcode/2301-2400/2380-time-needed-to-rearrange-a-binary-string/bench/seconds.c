// LeetCode #2380: Time Needed to Rearrange a Binary String -- the bench,
// the ★ arm in C: one pass, each 1 after some 0 taking the larger of one
// more second than the 1 before it and the 0s before it.

#include <stdint.h>
#include <stdio.h>

static int64_t seconds_to_remove_occurrences(const char *s) {
    int64_t zeros = 0, seconds = 0;
    for (; *s; s++) {
        if (*s == '0') {
            zeros++;
        } else if (zeros > 0) {
            seconds = seconds + 1 > zeros ? seconds + 1 : zeros;
        }
    }
    return seconds;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static char strings[100][1001];

int main(void) {
    // 100 strings of 1000 digits, string s 1 with a chance of 1 + s % 10
    // in 12; pass p asks for string (s + 7 p) % 100 in turn
    int64_t seed = 2380;
    for (int64_t s = 0; s < 100; s++) {
        for (int i = 0; i < 1000; i++) {
            strings[s][i] = next_random(&seed) % 12 < 1 + s % 10 ? '1' : '0';
        }
        strings[s][1000] = 0;
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 500; p++) {
        for (int64_t s = 0; s < 100; s++) {
            check = (check * 31 + seconds_to_remove_occurrences(strings[(s + 7 * p) % 100]) + p) % 1000000007;
        }
    }
    printf("500 passes over 100 strings of 1000 digits: checksum %lld\n", (long long)check);
    return 0;
}
