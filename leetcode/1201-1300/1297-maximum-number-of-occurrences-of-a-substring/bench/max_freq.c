// LeetCode #1297 bench: the ★ arm (one window of minSize letters slid along
// the string, each with few enough distinct letters counted by its text) over
// 10 strings of 10^5 letters over the first 2 to 6 letters, built once; then
// 20 passes, each setting one letter of every string and its limits from the
// checksum so far, answering it, and folding the answer into the checksum.
// C has no map: the counts are an open-addressing table, fresh per call, keyed
// by where the window starts, hashed by FNV-1a over its letters and compared
// with memcmp.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static uint64_t hash_text(const uint8_t *p, int64_t len) {
    uint64_t h = 1469598103934665603ULL;
    for (int64_t i = 0; i < len; i++) {
        h ^= p[i];
        h *= 1099511628211ULL;
    }
    return h;
}

static int64_t max_freq(const uint8_t *s, int64_t n, int64_t max_letters, int64_t min_size,
                        int64_t max_size) {
    (void)max_size;
    int64_t letters[26] = {0};
    int64_t distinct = 0;
    int64_t cap = 16;
    while (cap < 2 * n) cap *= 2;
    int64_t *starts = malloc(sizeof(int64_t) * cap);
    int64_t *counts = malloc(sizeof(int64_t) * cap);
    for (int64_t j = 0; j < cap; j++) starts[j] = -1;
    int64_t best = 0;
    for (int64_t i = 0; i < n; i++) {
        int add = s[i] - 97;
        if (letters[add] == 0) distinct++;
        letters[add]++;
        if (i >= min_size) {
            int gone = s[i - min_size] - 97;
            letters[gone]--;
            if (letters[gone] == 0) distinct--;
        }
        if (i + 1 >= min_size && distinct <= max_letters) {
            int64_t start = i + 1 - min_size;
            uint64_t slot = hash_text(s + start, min_size) & (uint64_t)(cap - 1);
            while (starts[slot] >= 0 && memcmp(s + starts[slot], s + start, min_size) != 0)
                slot = (slot + 1) & (uint64_t)(cap - 1);
            if (starts[slot] < 0) {
                starts[slot] = start;
                counts[slot] = 0;
            }
            int64_t times = ++counts[slot];
            if (times > best) best = times;
        }
    }
    free(starts);
    free(counts);
    return best;
}

static int64_t seed = 1297;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    uint8_t *texts[10];
    for (int64_t t = 0; t < 10; t++) {
        int64_t alphabet = 2 + t % 5;
        texts[t] = malloc(100000);
        for (int64_t j = 0; j < 100000; j++) texts[t][j] = (uint8_t)(97 + next_random() % alphabet);
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 20; p++) {
        for (int64_t t = 0; t < 10; t++) {
            texts[t][check % 100000] = (uint8_t)(97 + check % (2 + t % 5));
            uint8_t *s = malloc(100000);
            memcpy(s, texts[t], 100000);
            int64_t min_size = 1 + check % 26;
            int64_t max_letters = 1 + (check / 26) % 26;
            check = (check * 31 + max_freq(s, 100000, max_letters, min_size, min_size) + p) % 1000000007;
            free(s);
        }
    }
    printf("20 passes over 10 strings of 10^5: checksum %lld\n", (long long)check);
    for (int t = 0; t < 10; t++) free(texts[t]);
    return 0;
}
