// Benchmark for #548: C mirror of the ★ arm (a set of left sums per
// middle cut); see split_array_with_equal_sum.kara. The set is an
// open-addressing hash table emptied after each middle cut.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define SLOTS 8192
static int64_t keys[SLOTS];
static char used[SLOTS];
static int filled[SLOTS];
static int nfilled;

static unsigned slot_of(int64_t x) {
    uint64_t h = (uint64_t)x * 0x9E3779B97F4A7C15ull;
    return (unsigned)(h >> 51);
}
static void set_insert(int64_t x) {
    unsigned s = slot_of(x);
    while (used[s]) {
        if (keys[s] == x) return;
        s = (s + 1) & (SLOTS - 1);
    }
    used[s] = 1;
    keys[s] = x;
    filled[nfilled++] = (int)s;
}
static int set_contains(int64_t x) {
    unsigned s = slot_of(x);
    while (used[s]) {
        if (keys[s] == x) return 1;
        s = (s + 1) & (SLOTS - 1);
    }
    return 0;
}
static void set_clear(void) {
    for (int t = 0; t < nfilled; t++) used[filled[t]] = 0;
    nfilled = 0;
}

static int split_array(const int64_t *nums, int n) {
    if (n < 7) return 0;
    int64_t *prefix = calloc(n + 1, sizeof(int64_t));
    for (int i = 0; i < n; i++) prefix[i + 1] = prefix[i] + nums[i];
    int found = 0;
    for (int j = 3; j < n - 3 && !found; j++) {
        for (int i = 1; i < j - 1; i++)
            if (prefix[i] == prefix[j] - prefix[i + 1]) set_insert(prefix[i]);
        for (int k = j + 2; k < n - 1; k++) {
            int64_t third = prefix[k] - prefix[j + 1];
            if (third == prefix[n] - prefix[k + 1] && set_contains(third)) {
                found = 1;
                break;
            }
        }
        set_clear();
    }
    free(prefix);
    return found;
}

static int64_t seed = 548;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    const int count = 10, n = 2000;
    int64_t *all[10];
    for (int g = 0; g < count; g++) {
        int64_t spread = 1 + g % 5 * 25;
        all[g] = malloc(n * sizeof(int64_t));
        for (int i = 0; i < n; i++) all[g][i] = next_random() % (2 * spread + 1) - spread;
    }
    int64_t yes = 0, checksum = 0;
    for (int round = 0; round < 20; round++)
        for (int g = 0; g < count; g++) {
            int i = (round * 31 + g * 7) % n;
            all[g][i] = -all[g][i];
            int64_t bit = split_array(all[g], n);
            yes += bit;
            checksum = (checksum * 31 + bit + 7 * g) % 1000000007;
        }
    printf("%d arrays, 20 rounds each: %lld can be split, checksum %lld\n", count, (long long)yes,
           (long long)checksum);
    for (int g = 0; g < count; g++) free(all[g]);
    return 0;
}
