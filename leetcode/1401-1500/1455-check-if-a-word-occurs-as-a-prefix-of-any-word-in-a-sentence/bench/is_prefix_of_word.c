// LeetCode #1455 bench mirror: the first word that starts with the search
// word, counted from 1, by a walk along the words between the spaces, C
// having no library split.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

static int32_t is_prefix_of_word(const char *sentence, const char *search_word) {
    size_t k = strlen(search_word);
    int32_t index = 1;
    const char *w = sentence;
    for (;;) {
        const char *end = strchr(w, ' ');
        size_t len = end ? (size_t)(end - w) : strlen(w);
        if (len >= k && memcmp(w, search_word, k) == 0) return index;
        if (!end) return -1;
        w = end + 1;
        index++;
    }
}

static int64_t seed = 1455;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

// a word of 1 to `longest` letters drawn from the first 4 of the alphabet
static int64_t word(int64_t longest, char *out) {
    int64_t len = 1 + next_random() % longest;
    for (int64_t i = 0; i < len; i++) out[i] = 'a' + next_random() % 4;
    out[len] = 0;
    return len;
}

static char sentences[2000][101];
static char searches[2000][5];

int main(void) {
    // 2000 sentences of 100 letters of words of 1 to 8 letters and 2000
    // search words of 1 to 4 letters, drawn once, then every search word
    // looked for in every sentence, the answers folded to a checksum
    for (int i = 0; i < 2000; i++) {
        char *s = sentences[i];
        int64_t len = word(8, s);
        for (;;) {
            char w[9];
            int64_t wl = word(8, w);
            if (len + 1 + wl > 100) break;
            s[len] = ' ';
            memcpy(s + len + 1, w, wl + 1);
            len += 1 + wl;
        }
    }
    for (int i = 0; i < 2000; i++) word(4, searches[i]);
    int64_t check = 0;
    for (int i = 0; i < 2000; i++)
        for (int j = 0; j < 2000; j++)
            check = (check * 131 + is_prefix_of_word(sentences[i], searches[j]) + 1) % 1000000007;
    printf("4 x 10^6 searches: checksum %lld\n", (long long)check);
    return 0;
}
