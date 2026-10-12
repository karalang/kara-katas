// Benchmark for #409: mirror of longest_palindrome.kara (letter counts).
// A slice is a pointer into the text and a length, as a Str is.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t longest_palindrome(const unsigned char *s, int64_t n) {
    int64_t counts[128];
    memset(counts, 0, sizeof counts);
    for (int64_t i = 0; i < n; i++) {
        counts[s[i]] += 1;
    }
    int64_t length = 0;
    int odd = 0;
    for (int i = 0; i < 128; i++) {
        length += counts[i] / 2 * 2;
        if (counts[i] % 2 == 1) {
            odd = 1;
        }
    }
    return odd ? length + 1 : length;
}

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(int argc, char **argv) {
    int64_t queries = argc > 1 ? atoll(argv[1]) : 300000;
    int64_t size = 2000000, seed = 409;
    const char *letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    unsigned char *text = malloc(size);
    for (int64_t i = 0; i < size; i++) {
        text[i] = (unsigned char)letters[step(&seed) % 52];
    }
    int64_t total = 0, checksum = 0;
    for (int64_t q = 0; q < queries; q++) {
        int64_t len = 1000 + step(&seed) % 1001;
        int64_t hi = step(&seed);
        int64_t lo = step(&seed);
        int64_t start = (hi * 32768 + lo) % (size - len + 1);
        int64_t answer = longest_palindrome(text + start, len);
        total += answer;
        checksum = (checksum * 31 + answer) % 1000000007;
    }
    printf("%lld slices of a %lld-letter text: total %lld, checksum %lld\n", (long long)queries, (long long)size, (long long)total, (long long)checksum);
    free(text);
    return 0;
}
