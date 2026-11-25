// LeetCode #1363 bench -- C: the digits counted, the sum's residue put
// right by dropping the smallest one or two digits that do it.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 10000

// writes the answer into out (room for n + 1 bytes), returns its length
static size_t largest_multiple_of_three(const int32_t *digits, size_t n, char *out) {
    int64_t count[10] = {0};
    int64_t sum = 0;
    for (size_t i = 0; i < n; i++) {
        count[digits[i]] += 1;
        sum += digits[i];
    }
    int64_t r = sum % 3;
    if (r != 0) {
        int dropped = 0;
        for (int64_t d = r; d < 10; d += 3) {
            if (count[d] > 0) {
                count[d] -= 1;
                dropped = 1;
                break;
            }
        }
        int left = dropped ? 0 : 2;
        for (int64_t d = 3 - r; d < 10; d += 3) {
            while (left > 0 && count[d] > 0) {
                count[d] -= 1;
                left -= 1;
            }
        }
    }
    size_t len = 0;
    for (int d = 9; d >= 0; d--)
        for (int64_t k = 0; k < count[d]; k++) out[len++] = (char)('0' + d);
    out[len] = 0;
    if (len > 0 && out[0] == '0') {
        out[0] = '0';
        out[1] = 0;
        len = 1;
    }
    return len;
}

static int64_t seed = 1363;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    // 20 arrays of 10^4 digits, the constraints' most, built once; then
    // 10^4 rounds, each setting one digit of one array, both drawn from
    // the checksum so far, and folding the answer's length and three of
    // its digits into the checksum
    static int32_t arrays[20][N];
    static char out[N + 1];
    for (int k = 0; k < 20; k++)
        for (int i = 0; i < N; i++) arrays[k][i] = (int32_t)(next_random() % 10);
    int64_t check = 0;
    for (int64_t r = 0; r < 10000; r++) {
        int64_t k = check % 20;
        arrays[k][(check / 20) % N] = (int32_t)((check / 200000) % 10);
        size_t n = largest_multiple_of_three(arrays[k], N, out);
        int64_t picks = n == 0 ? 0 : (int64_t)out[0] * 7 + (int64_t)out[n / 2] * 11 + (int64_t)out[n - 1] * 13;
        check = (check * 31 + (int64_t)n + picks + r) % 1000000007;
    }
    printf("10000 rounds over 20 arrays of 10^4 digits: checksum %lld\n", (long long)check);
    return 0;
}
