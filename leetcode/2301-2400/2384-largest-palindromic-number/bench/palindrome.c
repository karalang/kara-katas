// LeetCode #2384: Largest Palindromic Number -- the bench, the ★ arm in C:
// the digits counted, the left half from 9 down with no 0 leading, the
// largest digit left over in the middle, the half reversed after it.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// The answer is written into a fresh allocation, as the other languages'
// String is; the caller frees it.
static char *largest_palindromic(const char *num, int64_t n, int64_t *len) {
    int64_t count[10] = {0};
    for (int64_t i = 0; i < n; i++) {
        count[num[i] - '0']++;
    }
    char *half = malloc(n / 2 + 1);
    int64_t h = 0;
    for (int d = 9; d >= 0; d--) {
        if (d == 0 && h == 0) {
            break;
        }
        for (int64_t k = 0; k < count[d] / 2; k++) {
            half[h++] = (char)('0' + d);
        }
    }
    char *out = malloc(2 * h + 2);
    memcpy(out, half, h);
    int64_t m = h;
    for (int d = 9; d >= 0; d--) {
        if (count[d] % 2 == 1) {
            out[m++] = (char)('0' + d);
            break;
        }
    }
    if (m == 0) {
        out[m++] = '0';
    } else {
        for (int64_t i = h - 1; i >= 0; i--) {
            out[m++] = half[i];
        }
    }
    free(half);
    out[m] = 0;
    *len = m;
    return out;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static char strings[100][10001];

int main(void) {
    // 100 strings of 10^4 digits, string s's below 1 + s % 10, each a 0
    // with a chance of s % 7 in 10; each pass folds every answer's length
    // and middle digit
    int64_t seed = 2384;
    for (int64_t s = 0; s < 100; s++) {
        for (int i = 0; i < 10000; i++) {
            if (next_random(&seed) % 10 < s % 7) {
                strings[s][i] = '0';
            } else {
                strings[s][i] = (char)('0' + next_random(&seed) % (1 + s % 10));
            }
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 200; p++) {
        for (int64_t s = 0; s < 100; s++) {
            int64_t len;
            char *answer = largest_palindromic(strings[s], 10000, &len);
            check = (check * 31 + len + (unsigned char)answer[len / 2] + p) % 1000000007;
            free(answer);
        }
    }
    printf("200 passes over 100 strings of 10^4 digits: checksum %lld\n", (long long)check);
    return 0;
}
