// LeetCode 804 -- Unique Morse Code Words: the bench, mirroring
// unique_morse.kara with the same set of strings: a hash set with open
// addressing, each code built in a string of its own.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static const char *CODES[26] = {".-",   "-...", "-.-.", "-..", ".",   "..-.", "--.",  "....", "..",
                                ".---", "-.-",  ".-..", "--",  "-.",  "---",  ".--.", "--.-", ".-.",
                                "...",  "-",    "..-",  "...-", ".--", "-..-", "-.--", "--.."};

static int64_t seed = 804;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

// The word written in Morse code, its letters' codes run together, in a
// new string.
static char *morse(const char *word) {
    size_t cap = 8, len = 0;
    char *out = malloc(cap);
    for (const char *p = word; *p; p++) {
        const char *code = CODES[*p - 97];
        size_t n = strlen(code);
        if (len + n + 1 > cap) {
            while (len + n + 1 > cap) {
                cap *= 2;
            }
            out = realloc(out, cap);
        }
        memcpy(out + len, code, n);
        len += n;
    }
    out[len] = 0;
    return out;
}

static uint64_t hash(const char *s) {
    uint64_t h = 1469598103934665603ULL;
    for (; *s; s++) {
        h = (h ^ (unsigned char)*s) * 1099511628211ULL;
    }
    return h;
}

static int64_t unique_morse_representations(char **words, int64_t n) {
    // A table of 256 slots, more than twice the 100 words.
    char *slots[256] = {0};
    int64_t count = 0;
    for (int64_t i = 0; i < n; i++) {
        char *code = morse(words[i]);
        uint64_t at = hash(code) & 255;
        while (slots[at] != NULL && strcmp(slots[at], code) != 0) {
            at = (at + 1) & 255;
        }
        if (slots[at] == NULL) {
            slots[at] = code;
            count++;
        } else {
            free(code);
        }
    }
    for (int i = 0; i < 256; i++) {
        free(slots[i]);
    }
    return count;
}

int main(void) {
    const char *letters = "abcdefghijklmnopqrstuvwxyz";
    const char *short_ = "etianm";
    char *lists[64][100];
    for (int l = 0; l < 64; l++) {
        for (int w = 0; w < 100; w++) {
            int64_t length = 1 + next_random() % 12;
            int few = next_random() % 2 == 0;
            char *word = malloc((size_t)length + 1);
            for (int64_t k = 0; k < length; k++) {
                word[k] = few ? short_[next_random() % 6] : letters[next_random() % 26];
            }
            word[length] = 0;
            lists[l][w] = word;
        }
    }
    int64_t rounds = 100000;
    int64_t total = 0;
    int64_t check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t k = unique_morse_representations(lists[r % 64], 100);
        total += k;
        check = (check * 131 + k) % 1000000007;
    }
    printf("%lld rounds of 100 words: %lld codes in all, checksum %lld\n", (long long)rounds, (long long)total,
           (long long)check);
    return 0;
}
