// LeetCode #2255: Count Prefixes of a Given String -- the benchmark's C
// mirror of prefixes.kara: each word tested as a beginning of s (no longer
// than s, and `memcmp` equal to s's first bytes), the ones that hold
// counted.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

static char words[1000][11];
static int64_t lengths[1000];
static char s[11];
static int64_t s_length;

static int64_t count_prefixes(int n) {
    int64_t count = 0;
    for (int i = 0; i < n; i++)
        if (lengths[i] <= s_length && memcmp(words[i], s, (size_t)lengths[i]) == 0) count++;
    return count;
}

static int64_t seed = 2255;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t random_word(char *out, int64_t longest, int64_t letters) {
    int64_t length = next_random() % longest + 1;
    for (int64_t i = 0; i < length; i++) out[i] = (char)('a' + next_random() % letters);
    out[length] = 0;
    return length;
}

int main(void) {
    int64_t check = 0;
    for (int c = 0; c < 500; c++) {
        int64_t letters = c % 5 + 1;
        for (int i = 0; i < 1000; i++) lengths[i] = random_word(words[i], 10, letters);
        s_length = random_word(s, 10, letters);
        check = (check * 31 + count_prefixes(1000) + 1) % 1000000007;
    }
    printf("500 cases of 1000 words: checksum %lld\n", (long long)check);
    return 0;
}
