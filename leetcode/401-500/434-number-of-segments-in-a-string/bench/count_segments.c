// Benchmark for #434: mirror of count_segments.kara (counting starts)
// on 10,000 windows of one random text of 1,000,000 characters.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t count_segments(const char *s, int64_t n) {
    int64_t count = 0;
    for (int64_t i = 0; i < n; i++) {
        if (s[i] != ' ' && (i == 0 || s[i - 1] == ' ')) {
            count++;
        }
    }
    return count;
}

int main(void) {
    const int64_t size = 1000000;
    const int64_t windows = 10000;
    int64_t seed = 434;
    const char *letters = "abcdefghijklmnopqrstuvwxyz";
    char *text = malloc(size);
    int64_t len = 0;
    // Words of 1 to 8 letters between runs of 1 to 3 spaces.
    while (len < size) {
        int64_t word = 1 + next_random(&seed) % 8;
        for (int64_t k = 0; k < word; k++) {
            if (len < size) {
                text[len++] = letters[next_random(&seed) % 26];
            }
        }
        int64_t gap = 1 + next_random(&seed) % 3;
        for (int64_t k = 0; k < gap; k++) {
            if (len < size) {
                text[len++] = ' ';
            }
        }
    }
    int64_t total = 0;
    int64_t checksum = 0;
    for (int64_t w = 0; w < windows; w++) {
        int64_t length = next_random(&seed) % 100001;
        int64_t start = next_random(&seed) % (size - length + 1);
        int64_t n = count_segments(text + start, length);
        total += n;
        checksum = (checksum * 31 + n) % 1000000007;
    }
    printf("%lld windows of a text of %lld: %lld segments, checksum %lld\n",
           (long long)windows, (long long)size, (long long)total, (long long)checksum);
    free(text);
    return 0;
}
