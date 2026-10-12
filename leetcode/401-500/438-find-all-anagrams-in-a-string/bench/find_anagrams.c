// Benchmark for #438: mirror of find_anagrams.kara (a sliding window of
// letter counts) on 40 patterns searched in one random text of
// 1,000,000 letters.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

// Writes the starts into `starts` and returns how many there are.
static int64_t find_anagrams(const char *s, int64_t n, const char *p, int64_t m, int64_t *starts) {
    int64_t count = 0;
    if (m > n) {
        return 0;
    }
    // need[c] is p's count of c minus the window's.
    int64_t need[26] = {0};
    for (int64_t i = 0; i < m; i++) {
        need[p[i] - 'a']++;
    }
    int64_t differ = 0;
    for (int c = 0; c < 26; c++) {
        if (need[c] != 0) {
            differ++;
        }
    }
    for (int64_t i = 0; i < n; i++) {
        int enter = s[i] - 'a';
        if (need[enter] == 0) {
            differ++;
        }
        need[enter]--;
        if (need[enter] == 0) {
            differ--;
        }
        if (i >= m) {
            int leave = s[i - m] - 'a';
            if (need[leave] == 0) {
                differ++;
            }
            need[leave]++;
            if (need[leave] == 0) {
                differ--;
            }
        }
        if (i >= m - 1 && differ == 0) {
            starts[count++] = i - m + 1;
        }
    }
    return count;
}

int main(void) {
    const int64_t size = 1000000, patterns = 40;
    int64_t seed = 438;
    // Letters from 'a' to 'd', so that short patterns have many
    // anagrams in the text.
    char *text = malloc(size);
    for (int64_t i = 0; i < size; i++) {
        text[i] = (char)('a' + next_random(&seed) % 4);
    }
    int64_t *starts = malloc(size * sizeof(int64_t));
    char p[16];
    int64_t found = 0, checksum = 0;
    for (int64_t q = 0; q < patterns; q++) {
        int64_t length = 1 + next_random(&seed) % 12;
        for (int64_t i = 0; i < length; i++) {
            p[i] = (char)('a' + next_random(&seed) % 4);
        }
        int64_t count = find_anagrams(text, size, p, length, starts);
        found += count;
        for (int64_t i = 0; i < count; i++) {
            checksum = (checksum * 31 + starts[i]) % 1000000007;
        }
    }
    printf("%lld patterns in a text of %lld: %lld anagrams, checksum %lld\n",
           (long long)patterns, (long long)size, (long long)found, (long long)checksum);
    free(starts);
    free(text);
    return 0;
}
