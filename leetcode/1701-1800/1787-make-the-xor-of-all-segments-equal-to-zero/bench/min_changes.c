// LeetCode #1787: Make the XOR of All Segments Equal to Zero -- the bench in
// C, mirroring min_changes.kara: a DP over the k groups of positions, each
// group's counts in a small open-addressing hash table.
#include <limits.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define SLOTS 2048

static int32_t keys[SLOTS], counts[SLOTS], used[SLOTS];
static int filled[SLOTS], nfilled;

static void count_add(int32_t key) {
    uint32_t h = ((uint32_t)key * 2654435761u) & (SLOTS - 1);
    while (used[h] && keys[h] != key) h = (h + 1) & (SLOTS - 1);
    if (!used[h]) { used[h] = 1; keys[h] = key; counts[h] = 0; filled[nfilled++] = (int)h; }
    counts[h]++;
}

static int32_t min_changes(const int32_t *nums, int n, int32_t k) {
    int32_t best[1024], next[1024];
    for (int x = 0; x < 1024; x++) best[x] = INT_MAX / 2;
    best[0] = 0;
    for (int32_t g = 0; g < k; g++) {
        for (int f = 0; f < nfilled; f++) used[filled[f]] = 0;
        nfilled = 0;
        int32_t size = 0;
        for (int i = g; i < n; i += k) { count_add(nums[i]); size++; }
        int32_t low = best[0];
        for (int x = 1; x < 1024; x++) if (best[x] < low) low = best[x];
        int32_t floor = low + size;
        for (int x = 0; x < 1024; x++) {
            next[x] = floor;
            for (int f = 0; f < nfilled; f++) {
                int h = filled[f];
                int32_t here = best[x ^ keys[h]] + size - counts[h];
                if (here < next[x]) next[x] = here;
            }
        }
        for (int x = 0; x < 1024; x++) best[x] = next[x];
    }
    return best[0];
}

static int64_t seed = 1787;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int32_t *lists = malloc(sizeof(int32_t) * 100 * 600);
    for (int l = 0; l < 100; l++)
        for (int i = 0; i < 600; i++) lists[l * 600 + i] = (int32_t)(next_random() % 1024);
    int64_t check = 0;
    for (int64_t call = 0; call < 300; call++) {
        const int32_t *nums = lists + ((check + call) % 100) * 600;
        int64_t k = 1 + (check * 7 + call) % 600;
        check = (check * 31 + min_changes(nums, 600, (int32_t)k)) % 1000000007;
    }
    printf("300 calls over 100 lists: checksum %lld\n", (long long)check);
    free(lists);
    return 0;
}
