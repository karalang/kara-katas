// LeetCode #2730: Find the Longest Semi-Repetitive Substring -- the bench
// (semi.kara in C): a sliding window over the bytes holding at most one
// adjacent equal pair.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t longest_semi_repetitive_substring(const char *b, int64_t n) {
    int64_t left = 0, pairs = 0, best = 1;
    for (int64_t right = 1; right < n; right++) {
        if (b[right] == b[right - 1]) pairs++;
        while (pairs > 1) {
            if (b[left] == b[left + 1]) pairs--;
            left++;
        }
        if (right - left + 1 > best) best = right - left + 1;
    }
    return best;
}

static int64_t seed = 2730;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int count = 200000, rounds = 20, n = 50;
    char *strings = malloc((size_t)count * n);
    for (int k = 0; k < count; k++) {
        int64_t digits = next_random() % 9 + 2;
        for (int i = 0; i < n; i++) strings[(size_t)k * n + i] = (char)('0' + next_random() % digits);
    }
    int64_t sum = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int k = 0; k < count; k++) {
            int64_t length = longest_semi_repetitive_substring(strings + (size_t)k * n, n);
            sum += length;
            check = (check * 31 + length + r) % 1000000007;
        }
    }
    printf("%d strings of 50 digits, %d rounds: lengths sum to %lld, checksum %lld\n", count, rounds, (long long)sum, (long long)check);
    free(strings);
    return 0;
}
