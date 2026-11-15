// LeetCode #2135: Count Words Obtained After Adding a Letter -- the
// benchmark, the same algorithm as words.kara; the set of start masks is
// an open-addressing hash table, C having none of its own.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 50000
#define SLOTS 131072  /* a power of two, over twice N */

typedef struct {
    char text[8];
    int len;
} Word;

static int64_t letters(const Word *w) {
    int64_t mask = 0;
    for (int i = 0; i < w->len; i++) mask |= (int64_t)1 << (w->text[i] - 97);
    return mask;
}

static uint64_t slot_of(int64_t key) {
    uint64_t x = (uint64_t)key * 0x9E3779B97F4A7C15ull;
    return (x ^ (x >> 29)) & (SLOTS - 1);
}

static int64_t table[SLOTS];

static int64_t word_count(const Word *starts, const Word *targets) {
    for (int i = 0; i < SLOTS; i++) table[i] = -1;
    for (int i = 0; i < N; i++) {
        int64_t m = letters(&starts[i]);
        uint64_t s = slot_of(m);
        while (table[s] != -1 && table[s] != m) s = (s + 1) & (SLOTS - 1);
        table[s] = m;
    }
    int64_t count = 0;
    for (int i = 0; i < N; i++) {
        int64_t mask = letters(&targets[i]);
        for (int j = 0; j < targets[i].len; j++) {
            int64_t want = mask ^ ((int64_t)1 << (targets[i].text[j] - 97));
            uint64_t s = slot_of(want);
            int found = 0;
            while (table[s] != -1) {
                if (table[s] == want) {
                    found = 1;
                    break;
                }
                s = (s + 1) & (SLOTS - 1);
            }
            if (found) {
                count++;
                break;
            }
        }
    }
    return count;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static void word(Word *out, int64_t len, int64_t k, int64_t *seed) {
    char letters_[26];
    for (int i = 0; i < k; i++) letters_[i] = (char)('a' + i);
    for (int64_t i = 0; i < len; i++) {
        int64_t j = i + next_random(seed) % (k - i);
        char t = letters_[i];
        letters_[i] = letters_[j];
        letters_[j] = t;
        out->text[i] = letters_[i];
    }
    out->len = (int)len;
}

int main(void) {
    int64_t seed = 2135;
    Word *starts[4], *targets[4];
    for (int p = 0; p < 4; p++) {
        starts[p] = malloc(N * sizeof(Word));
        targets[p] = malloc(N * sizeof(Word));
        for (int i = 0; i < N; i++) word(&starts[p][i], next_random(&seed) % 6 + 1, 12, &seed);
        for (int i = 0; i < N; i++) word(&targets[p][i], next_random(&seed) % 6 + 1, 12, &seed);
    }
    int64_t total = 0, check = 0;
    for (int64_t round = 0; round < 25; round++) {
        for (int p = 0; p < 4; p++) {
            int64_t hi = next_random(&seed);
            int64_t a = (hi * 32768 + next_random(&seed)) % N;
            word(&starts[p][a], next_random(&seed) % 6 + 1, 12, &seed);
            hi = next_random(&seed);
            int64_t b = (hi * 32768 + next_random(&seed)) % N;
            word(&targets[p][b], next_random(&seed) % 6 + 1, 12, &seed);
            int64_t count = word_count(starts[p], targets[p]);
            total += count;
            check = (check * 31 + count + round) % 1000000007;
        }
    }
    printf("100 solves: %lld words in all, checksum %lld\n", (long long)total, (long long)check);
    for (int p = 0; p < 4; p++) {
        free(starts[p]);
        free(targets[p]);
    }
    return 0;
}
