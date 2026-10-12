// Benchmark for #424: mirror of character_replacement.kara (a window
// that never shrinks).
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t character_replacement(const char *s, int64_t n, int64_t k) {
    int64_t count[26] = {0};
    int64_t best = 0, left = 0;
    for (int64_t right = 0; right < n; right++) {
        int64_t c = s[right] - 'A';
        count[c]++;
        if (count[c] > best) best = count[c];
        if (right - left + 1 - best > k) {
            count[s[left] - 'A']--;
            left++;
        }
    }
    return n - left;
}

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(int argc, char **argv) {
    int64_t calls = argc > 1 ? atoll(argv[1]) : 3000;
    int64_t size = 1000000, seed = 424, len = 0;
    char *text = malloc(size);
    while (len < size) {
        char letter = (char)('A' + step(&seed) % 5);
        int64_t run = 1 + step(&seed) % 8;
        for (int64_t i = 0; i < run; i++) {
            if (len < size) text[len++] = letter;
        }
    }
    int64_t total = 0, checksum = 0;
    for (int64_t c = 0; c < calls; c++) {
        int64_t length = 10000 + step(&seed) * 3 % 90000;
        int64_t start = step(&seed) * 30 % (size - length);
        int64_t k = step(&seed) % 50;
        int64_t answer = character_replacement(text + start, length, k);
        total += answer;
        checksum = (checksum * 31 + answer) % 1000000007;
    }
    printf("%lld calls: total %lld, checksum %lld\n", (long long)calls, (long long)total, (long long)checksum);
    return 0;
}
