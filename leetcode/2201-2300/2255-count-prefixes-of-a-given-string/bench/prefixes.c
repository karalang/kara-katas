// LeetCode #2255: Count Prefixes of a Given String -- the benchmark's C
// mirror of prefixes.kara: each word tested as a beginning of s (no longer
// than s, and `memcmp` equal to s's first bytes), the ones that hold
// counted. Each word is made as the other languages make it: its letters
// written into a buffer of its own, one allocation per word.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *bytes;
    int64_t length;
} Word;

static int64_t count_prefixes(const Word *words, int n, Word s) {
    int64_t count = 0;
    for (int i = 0; i < n; i++)
        if (words[i].length <= s.length && memcmp(words[i].bytes, s.bytes, (size_t)words[i].length) == 0) count++;
    return count;
}

static int64_t seed = 2255;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static Word random_word(int64_t longest, int64_t letters) {
    int64_t length = next_random() % longest + 1;
    char *bytes = malloc((size_t)length);
    for (int64_t i = 0; i < length; i++) bytes[i] = (char)('a' + next_random() % letters);
    return (Word){bytes, length};
}

int main(void) {
    static Word words[1000];
    int64_t check = 0;
    for (int c = 0; c < 500; c++) {
        int64_t letters = c % 5 + 1;
        for (int i = 0; i < 1000; i++) words[i] = random_word(10, letters);
        Word s = random_word(10, letters);
        check = (check * 31 + count_prefixes(words, 1000, s) + 1) % 1000000007;
        for (int i = 0; i < 1000; i++) free(words[i].bytes);
        free(s.bytes);
    }
    printf("500 cases of 1000 words: checksum %lld\n", (long long)check);
    return 0;
}
