// LeetCode #1805: Number of Different Integers in a String -- the bench in
// C: the ★ arm over 64 random words of 1000 characters built once, 20000
// calls. The set is an open-addressed table of copied runs, hashed by
// FNV-1a.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SLOTS 2048

typedef struct {
    char *text;
    size_t len;
} Run;

static int insert(Run *table, const char *text, size_t len) {
    uint64_t h = 1469598103934665603ULL;
    for (size_t i = 0; i < len; i++) h = (h ^ (unsigned char)text[i]) * 1099511628211ULL;
    size_t slot = h & (SLOTS - 1);
    while (table[slot].text) {
        if (table[slot].len == len && memcmp(table[slot].text, text, len) == 0) return 0;
        slot = (slot + 1) & (SLOTS - 1);
    }
    table[slot].text = malloc(len + 1);
    memcpy(table[slot].text, text, len);
    table[slot].len = len;
    return 1;
}

static int32_t num_different_integers(const char *word, size_t n) {
    static Run table[SLOTS];
    char run[1001];
    size_t run_len = 0;
    int in_run = 0;
    int32_t count = 0;
    memset(table, 0, sizeof table);
    for (size_t i = 0; i < n; i++) {
        char c = word[i];
        if (c >= '0' && c <= '9') {
            in_run = 1;
            if (!(run_len == 0 && c == '0')) run[run_len++] = c;
        } else if (in_run) {
            count += insert(table, run, run_len);
            run_len = 0;
            in_run = 0;
        }
    }
    if (in_run) count += insert(table, run, run_len);
    for (size_t s = 0; s < SLOTS; s++) free(table[s].text);
    return count;
}

static int64_t seed = 1805;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    static char words[64][1000];
    for (int w = 0; w < 64; w++)
        for (int i = 0; i < 1000; i++) {
            if (next_random() % 2 == 0)
                words[w][i] = (char)('0' + next_random() % 4);
            else
                words[w][i] = (char)(97 + next_random() % 26);
        }
    int64_t check = 0;
    for (int64_t call = 0; call < 20000; call++)
        check = (check * 31 + num_different_integers(words[(check + call) % 64], 1000)) % 1000000007;
    printf("20000 calls over 64 words of 1000 characters: checksum %lld\n", (long long)check);
    return 0;
}
