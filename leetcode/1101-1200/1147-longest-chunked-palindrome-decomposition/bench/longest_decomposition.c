// LeetCode #1147: Longest Chunked Palindrome Decomposition -- the C mirror
// of the ★ arm: greedy from both ends, the shortest equal chunks taken
// off (compared with memcmp), the middle one more.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

static int64_t longest_decomposition(const char *t, int64_t n) {
    int64_t i = 0, j = n, k = 0;
    while (i < j) {
        int64_t size = 1;
        while (2 * size <= j - i && memcmp(t + i, t + j - size, size) != 0) size++;
        if (2 * size > j - i) return k + 1;
        k += 2;
        i += size;
        j -= size;
    }
    return k;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static void text(int64_t *seed, char *b) {
    int64_t size = 1 + next_random(seed) % 4;
    char unit[4];
    for (int64_t u = 0; u < size; u++) unit[u] = (char)('a' + next_random(seed) % 2);
    for (int64_t i = 0; i < 1000; i++) b[i] = unit[i % size];
    int64_t at = next_random(seed) % 1000;
    b[at] = (char)('a' + next_random(seed) % 2);
}

int main(void) {
    static char texts[20][1000];
    int64_t seed = 1147, total = 0, check = 0;
    for (int t = 0; t < 20; t++) text(&seed, texts[t]);
    for (int64_t r = 0; r < 20000; r++) {
        text(&seed, texts[r % 20]);
        for (int t = 0; t < 20; t++) {
            int64_t k = longest_decomposition(texts[t], 1000);
            total += k;
            check = (check * 31 + k) % 1000000007;
        }
    }
    printf("20000 rounds over 20 texts of 1000 letters: chunks total %lld, checksum %lld\n",
           (long long)total, (long long)check);
    return 0;
}
