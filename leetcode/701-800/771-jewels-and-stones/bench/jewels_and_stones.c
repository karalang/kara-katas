// LeetCode 771 — Jewels and Stones: benchmark, the ★ arm in C.
// 256 random pairs of 50 jewels and 50 stones, built once; ROUNDS rounds
// each count the next pair. The set is a small open-addressing hash set
// of letters with FNV-1a over the letter's four bytes.
#include <stdio.h>
#include <stdint.h>
#include <string.h>

#define ROUNDS 1000000
#define SLOTS 128

typedef struct {
    uint32_t keys[SLOTS];
    uint8_t used[SLOTS];
} Set;

static uint32_t hash(uint32_t c) {
    uint32_t h = 2166136261u;
    for (int i = 0; i < 4; i++) h = (h ^ ((c >> (8 * i)) & 255)) * 16777619u;
    return h;
}

static void set_insert(Set *s, uint32_t c) {
    uint32_t i = hash(c) & (SLOTS - 1);
    while (s->used[i] && s->keys[i] != c) i = (i + 1) & (SLOTS - 1);
    s->used[i] = 1;
    s->keys[i] = c;
}

static int set_contains(const Set *s, uint32_t c) {
    uint32_t i = hash(c) & (SLOTS - 1);
    while (s->used[i]) {
        if (s->keys[i] == c) return 1;
        i = (i + 1) & (SLOTS - 1);
    }
    return 0;
}

static int64_t num_jewels_in_stones(const char *jewels, const char *stones) {
    Set kinds;
    memset(kinds.used, 0, sizeof kinds.used);
    for (const char *p = jewels; *p; p++) set_insert(&kinds, (unsigned char)*p);
    int64_t count = 0;
    for (const char *p = stones; *p; p++)
        if (set_contains(&kinds, (unsigned char)*p)) count += 1;
    return count;
}

static int64_t seed = 771;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static void random_letters(char *out, int n, int64_t kinds) {
    for (int i = 0; i < n; i++) {
        int64_t k = next_random() % kinds;
        int64_t base = k % 2 == 0 ? 97 : 65;
        out[i] = (char)(base + k / 2);
    }
    out[n] = 0;
}

static char jewels[256][51], stones[256][51];

int main(void) {
    for (int i = 0; i < 256; i++) {
        random_letters(jewels[i], 50, 52);
        random_letters(stones[i], 50, 52);
    }
    int64_t total = 0, check = 0;
    for (int64_t round = 0; round < ROUNDS; round++) {
        int k = (int)(round % 256);
        int64_t count = num_jewels_in_stones(jewels[k], stones[k]);
        total += count;
        check = (check * 31 + count) % 1000000007;
    }
    printf("%d rounds of 50 jewels and 50 stones: %lld jewels in all, checksum %lld\n",
           ROUNDS, (long long)total, (long long)check);
    return 0;
}
