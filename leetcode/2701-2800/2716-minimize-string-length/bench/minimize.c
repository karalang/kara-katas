// LeetCode #2716: Minimize String Length -- the bench (minimize.kara in
// C): the distinct letters of each string counted by a hash set, open
// addressing over 64 slots with a multiplicative hash, built afresh for
// each string.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SLOTS 64

static int64_t minimized_string_length(const char *s, int64_t n) {
    uint32_t slot[SLOTS];
    memset(slot, 0, sizeof slot);
    int64_t size = 0;
    for (int64_t i = 0; i < n; i++) {
        uint32_t c = (unsigned char)s[i];
        uint32_t h = (c * 2654435769u) >> 26;
        while (slot[h] != 0 && slot[h] != c) h = (h + 1) & (SLOTS - 1);
        if (slot[h] == 0) {
            slot[h] = c;
            size++;
        }
    }
    return size;
}

static int64_t seed = 2716;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int count = 100000, rounds = 10, n = 100;
    char *strings = malloc((size_t)count * n);
    for (int k = 0; k < count; k++) {
        int64_t letters = next_random() % 26 + 1;
        for (int i = 0; i < n; i++) strings[(size_t)k * n + i] = (char)('a' + next_random() % letters);
    }
    int64_t sum = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int k = 0; k < count; k++) {
            int64_t length = minimized_string_length(strings + (size_t)k * n, n);
            sum += length;
            check = (check * 31 + length + r) % 1000000007;
        }
    }
    printf("%d strings of 100 letters, %d rounds: lengths sum to %lld, checksum %lld\n", count, rounds, (long long)sum, (long long)check);
    free(strings);
    return 0;
}
