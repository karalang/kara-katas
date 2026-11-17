// LeetCode #2227: Encrypt and Decrypt Strings -- the benchmark's C
// mirror of encrypter.kara. C has no map of its own: the values are
// looked up in a table of 256 indexed by the character, and the counts
// of the dictionary's encryptions sit in an open-addressing hash table
// of strings.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SLOTS 256 /* a power of two, over twice the 100 dictionary words */

typedef struct {
    const char *table[256];
    char *keys[SLOTS];
    int64_t counts[SLOTS];
} Encrypter;

static uint64_t hash_of(const char *s) {
    uint64_t h = 1469598103934665603ull;
    for (; *s; s++) h = (h ^ (unsigned char)*s) * 1099511628211ull;
    return h;
}

static uint64_t find(const Encrypter *e, const char *key) {
    uint64_t s = hash_of(key) & (SLOTS - 1);
    while (e->keys[s] && strcmp(e->keys[s], key) != 0) s = (s + 1) & (SLOTS - 1);
    return s;
}

// "" (a fresh empty string) when a letter is no key; the caller frees it
static char *encrypt(const Encrypter *e, const char *word1) {
    size_t n = strlen(word1);
    char *secret = malloc(2 * n + 1);
    size_t at = 0;
    for (size_t i = 0; i < n; i++) {
        const char *value = e->table[(unsigned char)word1[i]];
        if (!value) {
            secret[0] = 0;
            return secret;
        }
        memcpy(secret + at, value, 2);
        at += 2;
    }
    secret[at] = 0;
    return secret;
}

static int64_t decrypt(const Encrypter *e, const char *word2) {
    uint64_t s = find(e, word2);
    return e->keys[s] ? e->counts[s] : 0;
}

static void build(Encrypter *e, const char *keys, char values[][3], int m, char **dictionary, int words) {
    memset(e, 0, sizeof *e);
    for (int i = 0; i < m; i++) e->table[(unsigned char)keys[i]] = values[i];
    for (int w = 0; w < words; w++) {
        char *secret = encrypt(e, dictionary[w]);
        if (secret[0]) {
            uint64_t s = find(e, secret);
            if (!e->keys[s]) {
                e->keys[s] = secret;
                e->counts[s] = 0;
            } else {
                free(secret);
            }
            e->counts[s]++;
        } else {
            free(secret);
        }
    }
}

static void release(Encrypter *e) {
    for (int s = 0; s < SLOTS; s++) free(e->keys[s]);
}

static int64_t seed = 2227;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static char *draw_word(int64_t length, int64_t letters) {
    char *word = malloc((size_t)length + 1);
    for (int64_t i = 0; i < length; i++) word[i] = (char)(97 + next_random() % letters);
    word[length] = 0;
    return word;
}

int main(void) {
    char keys[26];
    char values[26][3];
    for (int i = 0; i < 26; i++) {
        keys[i] = (char)(97 + i);
        char *v = draw_word(2, 3);
        memcpy(values[i], v, 3);
        free(v);
    }
    char *dictionary[100];
    for (int i = 0; i < 100; i++) dictionary[i] = draw_word(100, 26);
    char *words[200];
    for (int i = 0; i < 200; i++) {
        if (i % 2 == 0) {
            int64_t length = next_random() % 2000 + 1;
            words[i] = draw_word(length, 26);
        } else if (i % 4 == 1) {
            const char *plain = dictionary[next_random() % 100];
            size_t n = strlen(plain);
            words[i] = malloc(2 * n + 1);
            for (size_t j = 0; j < n; j++) memcpy(words[i] + 2 * j, values[plain[j] - 97], 2);
            words[i][2 * n] = 0;
        } else {
            words[i] = draw_word(200, 3);
        }
    }
    static Encrypter e;
    int64_t check = 0;
    for (int r = 0; r < 500; r++) {
        // punch: one dictionary word drawn again before each round
        int64_t at = next_random() % 100;
        free(dictionary[at]);
        dictionary[at] = draw_word(100, 26);
        build(&e, keys, values, 26, dictionary, 100);
        for (int i = 0; i < 200; i++) {
            if (i % 2 == 0) {
                char *secret = encrypt(&e, words[i]);
                int64_t n = (int64_t)strlen(secret);
                check = (check * 31 + n + (unsigned char)secret[n / 2]) % 1000000007;
                free(secret);
            } else {
                check = (check * 31 + decrypt(&e, words[i])) % 1000000007;
            }
        }
        release(&e);
    }
    printf("500 rounds of 200 calls: checksum %lld\n", (long long)check);
    for (int i = 0; i < 100; i++) free(dictionary[i]);
    for (int i = 0; i < 200; i++) free(words[i]);
    return 0;
}
