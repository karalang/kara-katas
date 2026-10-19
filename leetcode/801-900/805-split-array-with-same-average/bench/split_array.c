// LeetCode 805 -- Split Array With Same Average: the bench, mirroring
// split_array.kara with the same sums by size. C has no set, so each
// size's sums go in a hash set of its own: open addressing on a table
// that doubles when half full.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t seed = 805;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

typedef struct {
    int64_t *slots;  // -1 for an empty slot; sums are never negative
    int64_t cap;
    int64_t len;
} IntSet;

static void set_init(IntSet *s) {
    s->cap = 16;
    s->len = 0;
    s->slots = malloc((size_t)s->cap * sizeof(int64_t));
    for (int64_t i = 0; i < s->cap; i++) {
        s->slots[i] = -1;
    }
}

static uint64_t mix(int64_t x) {
    uint64_t h = (uint64_t)x * 0x9E3779B97F4A7C15ULL;
    return h ^ (h >> 29);
}

static void set_insert(IntSet *s, int64_t x);

static void set_grow(IntSet *s) {
    int64_t *old = s->slots;
    int64_t old_cap = s->cap;
    s->cap *= 2;
    s->len = 0;
    s->slots = malloc((size_t)s->cap * sizeof(int64_t));
    for (int64_t i = 0; i < s->cap; i++) {
        s->slots[i] = -1;
    }
    for (int64_t i = 0; i < old_cap; i++) {
        if (old[i] >= 0) {
            set_insert(s, old[i]);
        }
    }
    free(old);
}

static void set_insert(IntSet *s, int64_t x) {
    if (2 * (s->len + 1) > s->cap) {
        set_grow(s);
    }
    uint64_t at = mix(x) & (uint64_t)(s->cap - 1);
    while (s->slots[at] >= 0) {
        if (s->slots[at] == x) {
            return;
        }
        at = (at + 1) & (uint64_t)(s->cap - 1);
    }
    s->slots[at] = x;
    s->len++;
}

static int set_contains(const IntSet *s, int64_t x) {
    uint64_t at = mix(x) & (uint64_t)(s->cap - 1);
    while (s->slots[at] >= 0) {
        if (s->slots[at] == x) {
            return 1;
        }
        at = (at + 1) & (uint64_t)(s->cap - 1);
    }
    return 0;
}

static int split_array_same_average(const int64_t *nums, int64_t n) {
    int64_t total = 0;
    for (int64_t i = 0; i < n; i++) {
        total += nums[i];
    }
    int64_t half = n / 2;
    IntSet *sums = malloc((size_t)(half + 1) * sizeof(IntSet));
    for (int64_t k = 0; k <= half; k++) {
        set_init(&sums[k]);
    }
    set_insert(&sums[0], 0);
    int64_t *before = NULL;
    int64_t before_cap = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t x = nums[i];
        for (int64_t k = half; k >= 1; k--) {
            // The sums for k - 1 numbers, taken before row k changes.
            if (before_cap < sums[k - 1].len) {
                before_cap = sums[k - 1].len;
                before = realloc(before, (size_t)before_cap * sizeof(int64_t));
            }
            int64_t m = 0;
            for (int64_t j = 0; j < sums[k - 1].cap; j++) {
                if (sums[k - 1].slots[j] >= 0) {
                    before[m++] = sums[k - 1].slots[j];
                }
            }
            for (int64_t j = 0; j < m; j++) {
                set_insert(&sums[k], before[j] + x);
            }
        }
    }
    int found = 0;
    for (int64_t k = 1; k <= half; k++) {
        if (total * k % n == 0 && set_contains(&sums[k], total * k / n)) {
            found = 1;
            break;
        }
    }
    free(before);
    for (int64_t k = 0; k <= half; k++) {
        free(sums[k].slots);
    }
    free(sums);
    return found;
}

int main(void) {
    int64_t arrays[16][30];
    for (int a = 0; a < 16; a++) {
        int64_t sum = 0;
        for (int i = 0; i < 29; i++) {
            arrays[a][i] = next_random() % 300;
            sum += arrays[a][i];
        }
        arrays[a][29] = a % 2 == 0 ? next_random() % 300 : (31 - sum % 30) % 30 + 30 * (next_random() % 9);
    }
    int64_t rounds = 400;
    int64_t yes = 0;
    int64_t check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int can = split_array_same_average(arrays[r % 16], 30);
        if (can) {
            yes++;
        }
        check = (check * 131 + (can ? 1 : 2)) % 1000000007;
    }
    printf("%lld rounds of 30 numbers: %lld can be split, checksum %lld\n", (long long)rounds, (long long)yes,
           (long long)check);
    return 0;
}
