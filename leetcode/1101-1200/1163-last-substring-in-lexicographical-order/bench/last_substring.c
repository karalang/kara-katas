// LeetCode #1163: Last Substring in Lexicographical Order -- C mirror of the
// Kāra ★ arm: two pointers over the bytes, the answer copied out.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 400000

static char *last_substring(const char *b, int64_t n, int64_t *len) {
    int64_t i = 0, j = 1, k = 0;
    while (j + k < n) {
        if (b[i + k] == b[j + k]) {
            k += 1;
        } else if (b[i + k] > b[j + k]) {
            j = j + k + 1;
            k = 0;
        } else {
            i = i + k + 1 > j ? i + k + 1 : j;
            j = i + 1;
            k = 0;
        }
    }
    *len = n - i;
    char *out = malloc(n - i + 1);
    memcpy(out, b + i, n - i);
    out[n - i] = 0;
    return out;
}

static int64_t seed = 1163;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static void make(char *b, int kind) {
    char block[7];
    for (int i = 0; i < 7; i++) block[i] = 'a' + next_random() % 26;
    for (int64_t i = 0; i < N; i++) {
        if (kind == 0) b[i] = 'a' + next_random() % 26;
        else if (kind == 1) b[i] = 'a' + next_random() % 2;
        else if (kind == 2) b[i] = next_random() % 1000 == 0 ? 'a' + next_random() % 26 : block[i % 7];
        else b[i] = next_random() % 10 == 0 ? 'y' : 'z';
    }
}

static char texts[8][N];

int main(void) {
    for (int k = 0; k < 8; k++) make(texts[k], k % 4);
    int64_t total = 0, check = 0;
    for (int r = 0; r < 150; r++)
        for (int k = 0; k < 8; k++) {
            int64_t from = next_random() % (N / 2);
            int64_t len;
            char *got = last_substring(texts[k] + from, N - from, &len);
            total += len;
            check = (check * 31 + (N - from - len) * 7 + len) % 1000000007;
            free(got);
        }
    printf("150 rounds over 8 strings of 4 * 10^5 letters: total %lld, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
