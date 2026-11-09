// LeetCode #2053: Kth Distinct String in an Array -- C mirror of the ★
// arm's benchmark (distinct.kara): the same 5000 arrays, the same count
// into a hash table and walk of the array. C has no hash map: this one is
// open addressing over FNV-1a, sized to twice the array, each key a copy of
// its string.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t seed = 2053;

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

static Slot *find(Slot *table, int64_t size, const char *s) {
    uint64_t i = hash(s) & (uint64_t)(size - 1);
    while (table[i].key && strcmp(table[i].key, s) != 0) i = (i + 1) & (uint64_t)(size - 1);
    return &table[i];
}

static const char *kth_distinct(char **arr, int64_t n, int64_t k) {
    int64_t size = 2048;
    Slot *table = calloc(size, sizeof(Slot));
    for (int64_t i = 0; i < n; i++) {
        Slot *slot = find(table, size, arr[i]);
        if (!slot->key) slot->key = strdup(arr[i]);
        slot->count++;
    }
    const char *answer = "";
    int64_t left = k;
    for (int64_t i = 0; i < n; i++) {
        if (find(table, size, arr[i])->count == 1 && --left == 0) {
            answer = arr[i];
            break;
        }
    }
    for (int64_t i = 0; i < size; i++) free(table[i].key);
    free(table);
    return answer;
}

int main(void) {
    const char *alphabet = "abcdefghijklmnopqrstuvwxyz";
    char *arr[1000];
    int64_t found = 0, check = 0;
    for (int64_t t = 0; t < 5000; t++) {
        int64_t letters = 2 + t % 25;
        for (int i = 0; i < 1000; i++) {
            int64_t len = next_random() % 5 + 1;
            arr[i] = malloc(len + 1);
            for (int64_t j = 0; j < len; j++) arr[i][j] = alphabet[next_random() % letters];
            arr[i][len] = 0;
        }
        const char *answer = kth_distinct(arr, 1000, t % 1000 + 1);
        int64_t len = strlen(answer);
        if (len > 0) found++;
        for (int64_t j = 0; j < len; j++) check = (check * 31 + answer[j]) % 1000000007;
        check = (check * 31 + len + 1) % 1000000007;
        for (int i = 0; i < 1000; i++) free(arr[i]);
    }
    printf("5000 arrays: %lld answers found, checksum %lld\n", (long long)found, (long long)check);
    return 0;
}
