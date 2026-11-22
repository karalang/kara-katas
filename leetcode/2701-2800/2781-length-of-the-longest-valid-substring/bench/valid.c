// LeetCode #2781: Length of the Longest Valid Substring -- the bench in
// C: the ★ arm over 10 words of 10^5 letters from a to e, each against
// 10^5 forbidden words of 8 to 10 letters, all drawn first, then each
// answered 5 times, every answer building its own set: an
// open-addressing table of copied strings, FNV-1a hashed, probed
// linearly.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define COUNT 10
#define N 100000
#define WORDS 100000
#define SLOTS (1 << 18)

static int64_t seed = 2781;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static char *random_word(int64_t n, int64_t letters) {
    char *w = malloc(n + 1);
    for (int64_t i = 0; i < n; i++) w[i] = (char)('a' + next_random() % letters);
    w[n] = 0;
    return w;
}

static uint64_t fnv(const char *s, int64_t len) {
    uint64_t h = 1469598103934665603ULL;
    for (int64_t i = 0; i < len; i++) {
        h ^= (unsigned char)s[i];
        h *= 1099511628211ULL;
    }
    return h;
}

static char *slot_key[SLOTS];
static int64_t slot_len[SLOTS];

static void insert(const char *s, int64_t len) {
    uint64_t at = fnv(s, len) & (SLOTS - 1);
    while (slot_key[at]) {
        if (slot_len[at] == len && memcmp(slot_key[at], s, len) == 0) return;
        at = (at + 1) & (SLOTS - 1);
    }
    char *copy = malloc(len);
    memcpy(copy, s, len);
    slot_key[at] = copy;
    slot_len[at] = len;
}

static int contains(const char *s, int64_t len) {
    uint64_t at = fnv(s, len) & (SLOTS - 1);
    while (slot_key[at]) {
        if (slot_len[at] == len && memcmp(slot_key[at], s, len) == 0) return 1;
        at = (at + 1) & (SLOTS - 1);
    }
    return 0;
}

static void clear(void) {
    for (int64_t i = 0; i < SLOTS; i++) {
        free(slot_key[i]);
        slot_key[i] = NULL;
    }
}

static int64_t longest_valid_substring(const char *word, int64_t n, char **forbidden, int64_t *lens, int64_t count) {
    for (int64_t k = 0; k < count; k++) insert(forbidden[k], lens[k]);
    int64_t start = 0, best = 0;
    for (int64_t j = 0; j < n; j++) {
        for (int64_t i = j; i >= start && i + 10 > j; i--) {
            if (contains(word + i, j + 1 - i)) {
                start = i + 1;
                break;
            }
        }
        if (j + 1 - start > best) best = j + 1 - start;
    }
    clear();
    return best;
}

static char *words[COUNT];
static char *forbidden[COUNT][WORDS];
static int64_t lens[COUNT][WORDS];

int main(void) {
    int rounds = 5;
    for (int c = 0; c < COUNT; c++) {
        words[c] = random_word(N, 5);
        for (int k = 0; k < WORDS; k++) {
            int64_t n = 8 + next_random() % 3;
            forbidden[c][k] = random_word(n, 5);
            lens[c][k] = n;
        }
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int c = 0; c < COUNT; c++) {
            int64_t a = longest_valid_substring(words[c], N, forbidden[c], lens[c], WORDS);
            total += a;
            check = (check * 31 + a + 1 + r) % 1000000007;
        }
    }
    printf("%d words of 10^5, %d rounds: lengths sum to %lld, checksum %lld\n", COUNT, rounds, (long long)total, (long long)check);
    return 0;
}
