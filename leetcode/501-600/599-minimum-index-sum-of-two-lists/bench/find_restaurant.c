// Benchmark for #599: the ★ arm (index the first list in a hash table,
// then walk the second); see find_restaurant.kara. An open-addressing
// table hashed by FNV-1a, its keys copies of list1's strings as the Kāra
// arm's are clones, and the answer copies too, all freed by the caller.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *key;
    size_t len;
    int64_t index;
} Slot;

static char *copy(const char *s, size_t n) {
    char *t = malloc(n + 1);
    memcpy(t, s, n + 1);
    return t;
}

static uint64_t fnv(const char *s, size_t n) {
    uint64_t h = 1469598103934665603ULL;
    for (size_t k = 0; k < n; k++) {
        h ^= (unsigned char)s[k];
        h *= 1099511628211ULL;
    }
    return h;
}

// Fills `answer` with copies of the answer's strings; returns how many.
static int64_t find_restaurant(char **list1, int64_t n, char **list2, int64_t m,
                               char **answer) {
    size_t cap = 16;
    while (cap < (size_t)(2 * n)) cap *= 2;
    Slot *table = calloc(cap, sizeof(Slot));
    for (int64_t i = 0; i < n; i++) {
        size_t len = strlen(list1[i]);
        size_t h = fnv(list1[i], len) & (cap - 1);
        while (table[h].key && !(table[h].len == len && memcmp(table[h].key, list1[i], len) == 0))
            h = (h + 1) & (cap - 1);
        if (!table[h].key) {
            table[h].key = copy(list1[i], len);
            table[h].len = len;
        }
        table[h].index = i;
    }
    int64_t best = n + m;
    int64_t size = 0;
    for (int64_t j = 0; j < m; j++) {
        size_t len = strlen(list2[j]);
        size_t h = fnv(list2[j], len) & (cap - 1);
        while (table[h].key && !(table[h].len == len && memcmp(table[h].key, list2[j], len) == 0))
            h = (h + 1) & (cap - 1);
        if (table[h].key) {
            int64_t sum = table[h].index + j;
            if (sum < best) {
                best = sum;
                for (int64_t k = 0; k < size; k++) free(answer[k]);
                size = 0;
            }
            if (sum == best) answer[size++] = copy(list2[j], len);
        }
    }
    for (size_t k = 0; k < cap; k++) free(table[k].key);
    free(table);
    return size;
}

// ---- benchmark --------------------------------------------------------------

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

// Spells k in lower-case letters, base 26, the last letter the units.
static void spell(int64_t k, char *out) {
    char letters[16];
    int size = 0;
    do {
        letters[size++] = (char)('a' + k % 26);
        k /= 26;
    } while (k != 0);
    for (int i = 0; i < size; i++) out[i] = letters[size - 1 - i];
    out[size] = 0;
}

int main(void) {
    enum { COUNT = 100, ROUNDS = 100, POOL = 3000, LEN = 1000 };
    int64_t seed = 599;
    static char *pool[POOL];
    for (int k = 0; k < POOL; k++) {
        int64_t number = step(&seed) * 32768;
        number += step(&seed);
        char buf[64];
        char a[16], b[16];
        spell(k, a);
        spell(number, b);
        snprintf(buf, sizeof buf, "restaurant %s at %s", a, b);
        pool[k] = copy(buf, strlen(buf));
    }
    static int order[POOL];
    for (int k = 0; k < POOL; k++) order[k] = k;
    static char *lists[COUNT][2][LEN];
    for (int c = 0; c < COUNT; c++)
        for (int t = 0; t < 2; t++)
            for (int k = 0; k < LEN; k++) {
                int j = k + (int)(step(&seed) % (POOL - k));
                int x = order[k];
                order[k] = order[j];
                order[j] = x;
                lists[c][t][k] = copy(pool[order[k]], strlen(pool[order[k]]));
            }
    static char *answer[LEN];
    int64_t total = 0, checksum = 0;
    for (int round = 0; round < ROUNDS; round++)
        for (int g = 0; g < COUNT; g++) {
            int c = (round * 7 + g) % COUNT;
            int64_t size = find_restaurant(lists[c][0], LEN, lists[c][1], LEN, answer);
            total += size;
            for (int64_t k = 0; k < size; k++) {
                int64_t len = (int64_t)strlen(answer[k]);
                checksum = (checksum * 31 + len) % 1000000007;
                checksum = (checksum * 31 + (unsigned char)answer[k][len - 1]) % 1000000007;
                free(answer[k]);
            }
        }
    printf("%d pairs, %d rounds: total %lld, checksum %lld\n", COUNT, ROUNDS, (long long)total,
           (long long)checksum);
    return 0;
}
