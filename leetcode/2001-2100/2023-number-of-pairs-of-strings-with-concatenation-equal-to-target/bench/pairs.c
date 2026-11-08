// LeetCode #2023: Number of Pairs of Strings With Concatenation Equal to
// Target -- the ★ arm in C, the same algorithm and workload as pairs.kara:
// a hash table of copied strings (open addressing, FNV-1a), looked up by the
// target's two parts at every cut.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define CAP 256

typedef struct {
    char *key;
    int64_t len;
    int64_t count;
} Slot;

static uint64_t hash(const char *s, int64_t len) {
    uint64_t h = 1469598103934665603ULL;
    for (int64_t i = 0; i < len; i++) {
        h ^= (unsigned char)s[i];
        h *= 1099511628211ULL;
    }
    return h;
}

static Slot *find(Slot *table, const char *s, int64_t len) {
    uint64_t i = hash(s, len) & (CAP - 1);
    while (table[i].key && !(table[i].len == len && memcmp(table[i].key, s, len) == 0)) {
        i = (i + 1) & (CAP - 1);
    }
    return &table[i];
}

static int64_t num_of_pairs(char **nums, int64_t n, const char *target) {
    Slot table[CAP];
    memset(table, 0, sizeof table);
    for (int64_t i = 0; i < n; i++) {
        int64_t len = strlen(nums[i]);
        Slot *slot = find(table, nums[i], len);
        if (!slot->key) {
            slot->key = malloc(len);
            memcpy(slot->key, nums[i], len);
            slot->len = len;
        }
        slot->count++;
    }
    int64_t tlen = strlen(target);
    int64_t pairs = 0;
    for (int64_t k = 1; k < tlen; k++) {
        int64_t ca = find(table, target, k)->count;
        if (k * 2 == tlen && memcmp(target, target + k, k) == 0) {
            pairs += ca * (ca - 1);
        } else {
            pairs += ca * find(table, target + k, tlen - k)->count;
        }
    }
    for (int i = 0; i < CAP; i++) free(table[i].key);
    return pairs;
}

static int64_t seed = 2023;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static char *repeat(const char *block, int64_t block_len, int64_t times) {
    char *s = malloc(block_len * times + 1);
    for (int64_t t = 0; t < times; t++) memcpy(s + t * block_len, block, block_len);
    s[block_len * times] = 0;
    return s;
}

int main(void) {
    static char *lists[300][100];
    static char *targets[300];
    for (int p = 0; p < 300; p++) {
        int64_t block_len = next_random() % 3 + 1;
        char block[4];
        for (int64_t i = 0; i < block_len; i++) block[i] = (char)('1' + next_random() % 2);
        for (int i = 0; i < 100; i++) lists[p][i] = repeat(block, block_len, next_random() % (100 / block_len) + 1);
        targets[p] = repeat(block, block_len, next_random() % (100 / block_len - 1) + 2);
    }
    int64_t calls = 0, total = 0, check = 0;
    for (int r = 0; r < 20; r++) {
        for (int p = 0; p < 300; p++) {
            int64_t pairs = num_of_pairs(lists[p], 100, targets[p]);
            calls++;
            total += pairs;
            check = (check * 31 + pairs) % 1000000007;
        }
    }
    printf("%lld calls: %lld pairs, checksum %lld\n", (long long)calls, (long long)total, (long long)check);
    return 0;
}
