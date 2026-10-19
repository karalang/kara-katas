// LeetCode 763 — Partition Labels: benchmark, the ★ arm in C.
// 100,000 random strings of 500 letters.
#include <stdint.h>
#include <stdio.h>

// Writes the part sizes of s[0..n) into sizes; returns how many.
static int partition_labels(const char *s, int n, int64_t *sizes) {
    int64_t last[26] = {0};
    for (int i = 0; i < n; i++) last[s[i] - 'a'] = i;
    int count = 0;
    int64_t start = 0, end = 0;
    for (int i = 0; i < n; i++) {
        if (last[s[i] - 'a'] > end) end = last[s[i] - 'a'];
        if (i == end) {
            sizes[count++] = end - start + 1;
            start = i + 1;
        }
    }
    return count;
}

static int64_t seed = 763;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int rounds = 100000;
    int64_t parts = 0, check = 0;
    char s[500];
    int64_t sizes[500];
    for (int r = 0; r < rounds; r++) {
        int64_t width = 1 + next_random() % 4;
        for (int i = 0; i < 500; i++) {
            int64_t k = i * 26 / 500 + next_random() % width;
            s[i] = (char)('a' + (k < 25 ? k : 25));
        }
        int count = partition_labels(s, 500, sizes);
        parts += count;
        for (int p = 0; p < count; p++) check = (check * 31 + sizes[p]) % 1000000007;
    }
    printf("%d strings of 500 letters: %lld parts, checksum %lld\n", rounds, (long long)parts, (long long)check);
    return 0;
}
