// LeetCode #2085: Count Common Words With One Occurrence -- C mirror of
// the ★ arm's benchmark (common.kara): the same 2500 pairs of lists, the
// same count of both into a hash table and walk of the first. C has no hash
// map: this one is open addressing over FNV-1a, sized to twice the list,
// each key a copy of its word.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 1000
#define SIZE 2048

static int64_t seed = 2085;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

typedef struct {
    char *key;
    int64_t count;
} Slot;

static uint64_t hash(const char *s) {
    uint64_t h = 1469598103934665603ULL;
    for (; *s; s++) h = (h ^ (unsigned char)*s) * 1099511628211ULL;
    return h;
}

static Slot *find(Slot *table, const char *s) {
    uint64_t i = hash(s) & (SIZE - 1);
    while (table[i].key && strcmp(table[i].key, s) != 0) i = (i + 1) & (SIZE - 1);
    return &table[i];
}

static Slot *counts(char **words) {
    Slot *table = calloc(SIZE, sizeof(Slot));
    for (int i = 0; i < N; i++) {
        Slot *slot = find(table, words[i]);
        if (!slot->key) slot->key = strdup(words[i]);
        slot->count++;
    }
    return table;
}

static void drop(Slot *table) {
    for (int i = 0; i < SIZE; i++) free(table[i].key);
    free(table);
}

static int64_t count_words(char **words1, char **words2) {
    Slot *one = counts(words1);
    Slot *two = counts(words2);
    int64_t n = 0;
    for (int i = 0; i < SIZE; i++) {
        if (one[i].key && one[i].count == 1 && find(two, one[i].key)->count == 1) n++;
    }
    drop(one);
    drop(two);
    return n;
}

static void random_list(char **words, const char *alphabet, int64_t letters) {
    for (int i = 0; i < N; i++) {
        int64_t len = next_random() % 4 + 1;
        words[i] = malloc(len + 1);
        for (int64_t j = 0; j < len; j++) words[i][j] = alphabet[next_random() % letters];
        words[i][len] = 0;
    }
}

int main(void) {
    const char *alphabet = "abcdefghijklmnopqrstuvwxyz";
    char *words1[N], *words2[N];
    int64_t total = 0, check = 0;
    for (int64_t t = 0; t < 2500; t++) {
        int64_t letters = 2 + t % 25;
        random_list(words1, alphabet, letters);
        random_list(words2, alphabet, letters);
        int64_t a = count_words(words1, words2);
        total += a;
        check = (check * 31 + a) % 1000000007;
        for (int i = 0; i < N; i++) {
            free(words1[i]);
            free(words2[i]);
        }
    }
    printf("2500 pairs: sum %lld, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
