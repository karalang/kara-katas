// LeetCode #2744: Find Maximum Number of String Pairs -- the bench
// (pairs.kara in C): the words seen kept in a small open-addressing hash
// set of strings, as the other languages keep theirs, each word's
// reverse built and looked for.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SLOTS 128

static uint64_t hash_word(const char *w) {
    uint64_t h = 1469598103934665603ULL;
    for (; *w; w++) h = (h ^ (unsigned char)*w) * 1099511628211ULL;
    return h;
}

static int64_t maximum_number_of_string_pairs(char words[][3], int64_t n) {
    char *slots[SLOTS];
    memset(slots, 0, sizeof(slots));
    int64_t pairs = 0;
    for (int64_t i = 0; i < n; i++) {
        char *reversed = malloc(3);
        reversed[0] = words[i][1];
        reversed[1] = words[i][0];
        reversed[2] = 0;
        uint64_t h = hash_word(reversed) % SLOTS;
        while (slots[h]) {
            if (strcmp(slots[h], reversed) == 0) {
                pairs++;
                break;
            }
            h = (h + 1) % SLOTS;
        }
        free(reversed);
        char *copy = malloc(3);
        memcpy(copy, words[i], 3);
        h = hash_word(copy) % SLOTS;
        while (slots[h]) h = (h + 1) % SLOTS;
        slots[h] = copy;
    }
    for (int i = 0; i < SLOTS; i++) free(slots[i]);
    return pairs;
}

static int64_t seed = 2744;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t count = 20000, rounds = 10;
    char (*lists)[50][3] = malloc(sizeof(char[50][3]) * count);
    for (int64_t c = 0; c < count; c++) {
        int64_t len = 0;
        while (len < 50) {
            char w[3] = {(char)('a' + next_random() % 8), 0, 0};
            w[1] = (char)('a' + next_random() % 8);
            int seen = 0;
            for (int64_t i = 0; i < len; i++) seen |= strcmp(lists[c][i], w) == 0;
            if (!seen) memcpy(lists[c][len++], w, 3);
        }
    }
    int64_t sum = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t c = 0; c < count; c++) {
            int64_t pairs = maximum_number_of_string_pairs(lists[c], 50);
            sum += pairs;
            check = (check * 31 + pairs + r) % 1000000007;
        }
    }
    printf("%lld lists of 50 words, %lld rounds: pairs sum to %lld, checksum %lld\n",
           (long long)count, (long long)rounds, (long long)sum, (long long)check);
    free(lists);
    return 0;
}
