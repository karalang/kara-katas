// LeetCode #1554: Strings Differ by One Character -- bench: the ★ arm
// (every word entered once per place with that place blotted out) over 20
// lists of 1000 random words of 100 letters, built once, half of them with
// a pair planted that differs in one place, each asked 3 times. C mirror of differ.kara:
// the set is an open-addressing table of 2^18 slots hashed by FNV-1a,
// each pattern a fresh heap copy, all freed per call.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define CAP (1 << 18)
#define LEN 100

static uint64_t fnv(const char *s) {
    uint64_t h = 1469598103934665603ull;
    for (int i = 0; i < LEN; i++) {
        h ^= (unsigned char)s[i];
        h *= 1099511628211ull;
    }
    return h;
}

static int differ_by_one(char **dict, int n) {
    char **table = calloc(CAP, sizeof(char *));
    int found = 0;
    for (int w = 0; w < n && !found; w++) {
        for (int j = 0; j < LEN; j++) {
            char *pattern = malloc(LEN);
            memcpy(pattern, dict[w], LEN);
            pattern[j] = '*';
            uint64_t h = fnv(pattern) & (CAP - 1);
            while (table[h] && memcmp(table[h], pattern, LEN) != 0) h = (h + 1) & (CAP - 1);
            if (table[h]) {
                free(pattern);
                found = 1;
                break;
            }
            table[h] = pattern;
        }
    }
    for (int i = 0; i < CAP; i++) free(table[i]);
    free(table);
    return found;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

int main(void) {
    const char *alphabet = "abcdefghijklmnopqrstuvwxyz";
    int64_t seed = 1554;
    static char *lists[20][1000];
    for (int l = 0; l < 20; l++) {
        for (int w = 0; w < 1000; w++) {
            lists[l][w] = malloc(LEN);
            for (int i = 0; i < LEN; i++) lists[l][w][i] = alphabet[next_random(&seed) % 26];
        }
        if (l % 2 == 1) {
            int at = next_random(&seed) % 1000;
            int place = next_random(&seed) % 100;
            char letters[LEN];
            memcpy(letters, lists[l][at], LEN);
            letters[place] = letters[place] == 'a' ? 'b' : 'a';
            int twin = next_random(&seed) % 1000;
            memcpy(lists[l][twin], letters, LEN);
        }
    }
    int64_t yes = 0, check = 0;
    for (int64_t pass = 0; pass < 3; pass++) {
        for (int64_t l = 0; l < 20; l++) {
            if (differ_by_one(lists[l], 1000)) {
                yes++;
                check = mix(check, pass * 20 + l);
            }
        }
    }
    printf("3 passes over 20 lists of 1000 words of 100 letters: %lld true, checksum %lld\n",
           (long long)yes, (long long)check);
    return 0;
}
