// LeetCode #1694: Reformat Phone Number -- the bench's C mirror: the ★ arm
// on 100000 random numbers of 100 characters, all drawn first, each
// answered 40 times.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define COUNT 100000
#define ROUNDS 40
#define LENGTH 100

// writes the answer into `out` and returns its length
static int64_t reformat_number(const char *number, int64_t n, char *out) {
    char digits[LENGTH];
    int64_t d = 0;
    for (int64_t i = 0; i < n; i++) {
        if (number[i] >= '0' && number[i] <= '9') {
            digits[d++] = number[i];
        }
    }
    int64_t len = 0, at = 0;
    while (d - at > 4) {
        memcpy(out + len, digits + at, 3);
        len += 3;
        out[len++] = '-';
        at += 3;
    }
    if (d - at == 4) {
        memcpy(out + len, digits + at, 2);
        len += 2;
        out[len++] = '-';
        memcpy(out + len, digits + at + 2, 2);
        len += 2;
    } else {
        memcpy(out + len, digits + at, (size_t)(d - at));
        len += d - at;
    }
    return len;
}

// ---- the harness ----------------------------------------------------------

static int64_t seed = 1694;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    const char *alphabet = "0123456789 -";
    char *numbers = malloc((size_t)COUNT * LENGTH);
    for (int64_t c = 0; c < COUNT; c++) {
        for (int64_t i = 0; i < LENGTH; i++) {
            int64_t pick = i < 2 ? next_random() % 10 : next_random() % 12;
            numbers[c * LENGTH + i] = alphabet[pick];
        }
    }
    char out[2 * LENGTH];
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int64_t c = 0; c < COUNT; c++) {
            int64_t len = reformat_number(numbers + c * LENGTH, LENGTH, out);
            total += len;
            check = (check * 31 + len + (uint8_t)out[len / 2] + (uint8_t)out[len - 1] + r) % 1000000007;
        }
    }
    printf("%d numbers of %d characters, %d rounds: %lld characters out, checksum %lld\n", COUNT, LENGTH, ROUNDS, (long long)total, (long long)check);
    free(numbers);
    return 0;
}
