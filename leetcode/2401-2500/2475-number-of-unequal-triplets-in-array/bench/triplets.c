// LeetCode #2475: Number of Unequal Triplets in Array -- the bench, the ★
// arm in C: the values counted, and each value of count `c` the middle of
// `left * c * right` triplets. C has no hash map, so the counts are kept
// in an open-addressing table of 256 slots keyed by the value, walked in
// slot order and emptied after every list.
#include <stdint.h>
#include <stdio.h>

#define CAP 256

typedef struct {
    int64_t key, count;
} Slot;

static Slot table[CAP];

static Slot *find(int64_t key) {
    uint64_t h = ((uint64_t)key * 0x9E3779B97F4A7C15ULL) >> 56;
    while (table[h].key != 0 && table[h].key != key) h = (h + 1) & (CAP - 1);
    return &table[h];
}

static int64_t unequal_triplets(const int64_t *nums, int64_t n) {
    for (int64_t i = 0; i < n; i++) {
        Slot *s = find(nums[i]);
        s->key = nums[i];
        s->count++;
    }
    int64_t left = 0, total = 0;
    for (int i = 0; i < CAP; i++) {
        if (table[i].key == 0) continue;
        int64_t c = table[i].count;
        total += left * c * (n - left - c);
        left += c;
        table[i].key = 0;
        table[i].count = 0;
    }
    return total;
}

// ---- bench harness ---------------------------------------------------------

static int64_t seed = 2475;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t lists[2000][100];

int main(void) {
    // 2000 lists of 100 values from 1 to 50 built once; then 600 passes,
    // each setting one value of every list from the checksum so far, then
    // answering it, folding the count plus the pass into the checksum
    for (int a = 0; a < 2000; a++)
        for (int i = 0; i < 100; i++) lists[a][i] = 1 + next_random() % 50;
    int64_t check = 0;
    for (int64_t p = 0; p < 600; p++) {
        for (int64_t a = 0; a < 2000; a++) {
            lists[a][(check + a) % 100] = 1 + check % 50;
            check = (check * 31 + unequal_triplets(lists[a], 100) + p) % 1000000007;
        }
    }
    printf("600 passes over 2000 lists of 100: checksum %lld\n", (long long)check);
    return 0;
}
