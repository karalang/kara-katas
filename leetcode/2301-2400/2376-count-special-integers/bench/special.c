// LeetCode #2376: Count Special Integers -- the bench, the ★ arm in C: the
// shorter numbers counted by length, then n's own length place by place,
// each place adding its smaller unused digits times the arrangements of
// the places after it. The digits and the used flags are allocated in
// each call, as the other languages' are.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t arrangements(int64_t free_, int64_t places) {
    int64_t ways = 1;
    for (int64_t k = 0; k < places; k++) {
        ways *= free_ - k;
    }
    return ways;
}

static int64_t count_special_numbers(int64_t n) {
    char text[24];
    int64_t len = snprintf(text, sizeof text, "%lld", (long long)n);
    int64_t *digits = malloc(len * sizeof(int64_t));
    for (int64_t i = 0; i < len; i++) {
        digits[i] = text[i] - '0';
    }
    int64_t count = 0;
    for (int64_t l = 1; l < len; l++) {
        count += 9 * arrangements(9, l - 1);
    }
    char *used = calloc(10, 1);
    int whole = 1;
    for (int64_t i = 0; i < len; i++) {
        int64_t low = i == 0 ? 1 : 0;
        for (int64_t d = low; d < digits[i]; d++) {
            if (!used[d]) {
                count += arrangements(9 - i, len - 1 - i);
            }
        }
        if (used[digits[i]]) {
            whole = 0;
            break;
        }
        used[digits[i]] = 1;
    }
    free(used);
    free(digits);
    return count + whole;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    // 10^5 values of 1 to 10 digits, at most 2 * 10^9
    int64_t seed = 2376;
    int64_t *values = malloc(100000 * sizeof(int64_t));
    for (int i = 0; i < 100000; i++) {
        int64_t digits = 1 + next_random(&seed) % 10;
        int64_t top = 1;
        for (int64_t k = 0; k < digits; k++) {
            top *= 10;
        }
        int64_t high = next_random(&seed);
        int64_t r = high * 32768 + next_random(&seed);
        int64_t cap = top < 2000000001 ? top : 2000000001;
        values[i] = 1 + r % (cap - 1);
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 100; p++) {
        for (int i = 0; i < 100000; i++) {
            check = (check * 31 + count_special_numbers(values[i]) + p) % 1000000007;
        }
    }
    printf("100 passes over 10^5 values: checksum %lld\n", (long long)check);
    free(values);
    return 0;
}
